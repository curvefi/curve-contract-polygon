from collections import defaultdict


class _State:
    """RewardStream.vy encapsulated state."""

    def __init__(self, owner: str, distributor: str, duration: int) -> None:
        # public getters in contract
        self.owner = owner
        self.distributor = distributor

        # time when reward distribtuion period finishes
        self.period_finish = 0
        # rate at which the reward is distributed (per block)
        self.reward_rate = 0
        # duration of the reward period (in seconds)
        self.reward_duration = duration
        # epoch time of last state changing update
        self.last_update_time = 0
        # the total amount of rewards a receiver is to receive
        self.reward_per_receiver_total = 0
        # total number of receivers
        self.receiver_count = 0
        # whether a receiver is approved to get rewards
        self.reward_receivers = defaultdict(bool)

        # private storage in contract
        # how much reward tokens a receiver has been sent
        self._reward_paid = defaultdict(int)

    def _update_per_receiver_total(self, timestamp: int) -> int:
        """Globally update the total amount received per receiver.

        This function updates the `self.reward_per_receiver_total` variable in the 4
        external function calls `add_receiver`, `remove_receiver`, `get_reward`,
        and `notify_reward_amount`.

        Note:
            For users that get added mid-distribution period, this function will
            set their `reward_paid` variable to the current `reward_per_receiver_total`,
            and then update the global `reward_per_receiver_total` var. This effectively
            makes it so rewards are distributed equally from the point onwards which a
            user is added.
        """
        total = self.reward_per_receiver_total
        count = self.receiver_count
        if count == 0:
            return total

        last_time = min(timestamp, self.period_finish)
        total += (last_time - self.last_update_time) * self.reward_rate / count
        self.reward_per_receiver_total = total
        self.last_update_time = last_time

        return total

    def add_receiver(self, receiver: str, msg_sender: str, timestamp: int):
        """Add a new receiver."""
        assert msg_sender == self.owner, "dev: only owner"
        assert self.reward_receivers[receiver] is False, "dev: receiver is active"

        total = self._update_per_receiver_total(timestamp)
        self.reward_receivers[receiver] = True
        self.receiver_count += 1
        self._reward_paid[receiver] = total

    def remove_receiver(self, receiver: str, msg_sender: str, timestamp: int):
        """Remove a receiver, pay out their reward"""
        assert msg_sender == self.owner, "dev: only owner"
        assert self.reward_receivers[receiver] is True, "dev: receiver is inactive"

        total = self._update_per_receiver_total(timestamp)
        self.reward_receivers[receiver] = False
        self.receiver_count -= 1
        amount = total - self._reward_paid[receiver]
        if amount > 0:
            # send ERC20 reward token to `msg_sender`
            pass
        self._reward_paid[receiver] = 0

    def get_reward(self, msg_sender: str, timestamp: int):
        """Get rewards if any are available"""
        assert self.reward_receivers[msg_sender] is True, "dev: caller is not receiver"

        total = self._update_per_receiver_total(timestamp)
        amount = total - self._reward_paid[msg_sender]
        if amount > 0:
            # transfer `amount` of ERC20 tokens to `msg_sender`
            # update the total amount paid out to `msg_sender`
            self._reward_paid[msg_sender] = total

    def notify_reward_amount(self, amount: int, timestamp: int, msg_sender: str):
        """Add rewards to the contract for distribution."""
        assert msg_sender == self.distributor, "dev: only distributor"

        self._update_per_receiver_total(timestamp)
        if timestamp >= self.period_finish:
            # the reward distribution period has passed
            self.reward_rate = amount / self.reward_duration
        else:
            # reward distribution period currently in progress
            remaining_rewards = (self.period_finish - timestamp) * self.reward_rate
            self.reward_rate = remaining_rewards / self.reward_duration

        self.last_update_time = timestamp
        # extend our reward duration period
        self.period_finish = timestamp + self.reward_duration

    def set_reward_duration(self, duration: int, timestamp: int, msg_sender: str):
        """Adjust the reward distribution duration."""
        assert msg_sender == self.owner, "dev: only owner"
        assert timestamp > self.period_finish, "dev: reward period currently active"

        self.reward_duration = duration
