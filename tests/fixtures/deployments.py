import pytest


@pytest.fixture(scope="module")
def swap(
    project,
    alice,
    underlying_coins,
    wrapped_coins,
    pool_token,
    pool_data,
):
    deployer = getattr(project, pool_data["swap_contract"])

    abi = next(i["inputs"] for i in deployer.abi if i["type"] == "constructor")

    args = {
        "_coins": wrapped_coins,
        "_underlying_coins": underlying_coins,
        "_pool_token": pool_token,
        "_A": 360 * 2,
        "_fee": 0,
        "_admin_fee": 0,
        "_offpeg_fee_multiplier": 0,
        "_owner": alice,
    }
    deployment_args = [args[i["name"]] for i in abi] + [({"from": alice})]

    contract = deployer.deploy(*deployment_args)
    pool_token.set_minter(contract, {"from": alice})

    return contract
