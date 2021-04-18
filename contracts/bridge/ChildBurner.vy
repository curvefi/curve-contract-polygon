# @version 0.2.12

interface BridgeToken:
    def withdraw(_amount: uint256): nonpayable
    def balanceOf(_user: address) -> uint256: view


owner: public(address)
future_owner: public(address)


@external
def __init__():
    self.owner = msg.sender


@external
def withdraw(_token: address):
    assert msg.sender == self.owner
    amount: uint256 = BridgeToken(_token).balanceOf(self)
    BridgeToken(_token).withdraw(amount)


@external
def commit_transfer_ownership(_owner: address):
    assert msg.sender == self.owner
    self.future_owner = _owner


@external
def accept_transfer_ownership():
    assert msg.sender == self.future_owner
    self.owner = self.future_owner
