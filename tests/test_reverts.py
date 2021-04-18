import itertools

import brownie
import pytest


@pytest.fixture(scope="module", autouse=True)
def setup(mint_alice, approve_alice, mint_bob, approve_bob, set_fees):
    set_fees(4000000, 5000000000, include_meta=True)


def test_insufficient_balances(
    chain,
    alice,
    bob,
    charlie,
    swap,
    n_coins,
    wrapped_decimals,
    underlying_decimals,
    wrapped_coins,
    underlying_coins,
    initial_amounts,
):
    # attempt to deposit more funds than user has
    for idx in range(n_coins):
        amounts = [i // 2 for i in initial_amounts]
        amounts[idx] = int(wrapped_coins[idx].balanceOf(alice) * 1.01)
        with brownie.reverts():
            swap.add_liquidity(amounts, 0, {"from": alice})

    # add liquidity balanced
    amounts = [i // 2 for i in initial_amounts]
    swap.add_liquidity(amounts, 0, {"from": alice})

    # attempt to perform swaps between coins with insufficient funds
    for send, recv in itertools.permutations(range(n_coins), 2):
        amount = initial_amounts[send] // 4
        with brownie.reverts():
            swap.exchange(send, recv, amount, 0, {"from": charlie})

    # attempt to perform swaps between coins with insufficient funds
    if hasattr(swap, "exchange_underlying"):
        for send, recv in itertools.permutations(range(n_coins), 2):
            assert underlying_coins[send].balanceOf(charlie) == 0
            amount = initial_amounts[send] // 4
            with brownie.reverts():
                swap.exchange_underlying(send, recv, amount, 0, {"from": charlie})

    # remove liquidity balanced
    with brownie.reverts():
        swap.remove_liquidity(10 ** 18, [0] * n_coins, {"from": charlie})

    # remove liquidity imbalanced
    for idx in range(n_coins):
        amounts = [10 ** wrapped_decimals[i] for i in range(n_coins)]
        amounts[idx] = wrapped_coins[idx].balanceOf(swap) + 1
        with brownie.reverts():
            swap.remove_liquidity_imbalance(amounts, 2 ** 256 - 1, {"from": charlie})

    for idx in range(n_coins):
        with brownie.reverts():
            swap.remove_liquidity_one_coin(10 ** wrapped_decimals[idx], idx, 0, {"from": charlie})
