import pytest

# shared logic for pool and base_pool setup fixtures


def _mint(acct, wrapped_coins, wrapped_amounts, underlying_coins, underlying_amounts):
    for coin, amount in zip(wrapped_coins, wrapped_amounts):
        coin._mint_for_testing(acct, amount, {"from": acct})

    for coin, amount in zip(underlying_coins, underlying_amounts):
        if coin in wrapped_coins:
            continue
        coin._mint_for_testing(acct, amount, {"from": acct})


def _approve(owner, spender, *coins):
    for coin in set(x for i in coins for x in i):
        coin.approve(spender, 2 ** 256 - 1, {"from": owner})


# pool setup fixtures


@pytest.fixture(scope="module")
def add_initial_liquidity(
    alice, mint_alice, approve_alice, underlying_coins, swap, initial_amounts
):
    # mint (10**7 * precision) of each coin in the pool
    swap.add_liquidity(initial_amounts, 0, {"from": alice})


@pytest.fixture(scope="module")
def mint_bob(bob, underlying_coins, wrapped_coins, initial_amounts, initial_amounts_underlying):
    _mint(bob, wrapped_coins, initial_amounts, underlying_coins, initial_amounts_underlying)


@pytest.fixture(scope="module")
def approve_bob(bob, swap, underlying_coins, wrapped_coins):
    _approve(bob, swap, underlying_coins, wrapped_coins)


@pytest.fixture(scope="module")
def mint_alice(alice, underlying_coins, wrapped_coins, initial_amounts, initial_amounts_underlying):
    _mint(
        alice, wrapped_coins, initial_amounts, underlying_coins, initial_amounts_underlying,
    )


@pytest.fixture(scope="module")
def approve_alice(alice, swap, underlying_coins, wrapped_coins):
    _approve(alice, swap, underlying_coins, wrapped_coins)


@pytest.fixture(scope="module")
def approve_zap(alice, bob, zap, pool_token, underlying_coins):
    for underlying in underlying_coins:
        underlying.approve(zap, 2 ** 256 - 1, {"from": alice})
        underlying.approve(zap, 2 ** 256 - 1, {"from": bob})

    pool_token.approve(zap, 2 ** 256 - 1, {"from": alice})
    pool_token.approve(zap, 2 ** 256 - 1, {"from": bob})
