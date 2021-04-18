import pytest

# pools


@pytest.fixture(scope="module")
def underlying_decimals(pool_data):
    # number of decimal places for each underlying coin in the active pool
    return [i.get("decimals", i.get("wrapped_decimals")) for i in pool_data["coins"]]


@pytest.fixture(scope="module")
def wrapped_decimals(pool_data):
    # number of decimal places for each wrapped coin in the active pool
    yield [i.get("wrapped_decimals", i.get("decimals")) for i in pool_data["coins"]]


@pytest.fixture(scope="module")
def base_amount(pool_data):
    try:
        amount = pool_data["testing"]["initial_amount"]
    except KeyError:
        amount = 1000000

    yield amount


@pytest.fixture(scope="module")
def initial_amounts(wrapped_decimals, base_amount):
    # 1e6 of each coin - used to make an even initial deposit in many test setups
    yield [10 ** i * base_amount for i in wrapped_decimals]


@pytest.fixture(scope="module")
def initial_amounts_underlying(underlying_decimals, base_amount, n_coins):
    return [10 ** i * base_amount for i in underlying_decimals]


@pytest.fixture(scope="module")
def n_coins(pool_data):
    yield len(pool_data["coins"])
