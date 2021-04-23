import pytest
from brownie import ETH_ADDRESS, Contract, interface
from brownie.convert import to_bytes

# public fixtures - these can be used when testing


@pytest.fixture(scope="module")
def pool_token(project, alice, pool_data):
    name = pool_data["name"]
    deployer = getattr(project, pool_data["lp_contract"])
    args = [f"Curve {name} LP Token", f"{name}CRV", 18, 0][: len(deployer.deploy.abi["inputs"])]
    return deployer.deploy(*args, {"from": alice})


@pytest.fixture(scope="module")
def wrapped_coins(project, alice, pool_data, underlying_coins):
    coins = []

    for i, data in enumerate(pool_data["coins"]):
        if not data.get("wrapped_decimals"):
            coins.append(underlying_coins[i])
        else:
            coins.append(_MintableTestToken(data["wrapped_address"], data["wrapped_interface"]))
    return coins


@pytest.fixture(scope="module")
def underlying_coins(alice, project, pool_data):
    coins = []

    for data in pool_data["coins"]:
        if data.get("underlying_address") == ETH_ADDRESS:
            coins.append(ETH_ADDRESS)
        else:
            coins.append(
                _MintableTestToken(
                    data.get("underlying_address", data.get("wrapped_address")),
                    data.get("underlying_interface", data.get("wrapped_interface")),
                )
            )

    return coins


class _MintableTestToken(Contract):
    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi("PolygonToken", address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if hasattr(self, "getRoleMember"):
            role = "0x8f4f2da22e8ac8f11e15f9fc141cddbb5deea8800186560abb6e68c5496619a9"
            minter = self.getRoleMember(role, 0)
            amount = to_bytes(amount, "bytes32")
            self.deposit(target, amount, {"from": minter})
        elif hasattr(self, "POOL"):
            token = _MintableTestToken(self.UNDERLYING_ASSET_ADDRESS(), "BridgeToken")
            lending_pool = interface.AaveLendingPool(self.POOL())
            token._mint_for_testing(target, amount)
            token.approve(lending_pool, amount, {"from": target})
            lending_pool.deposit(token, amount, target, 0, {"from": target})
        else:
            raise ValueError("Unsupported Token")
