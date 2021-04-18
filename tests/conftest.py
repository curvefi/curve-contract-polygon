import json

import pytest
from brownie.project.main import get_loaded_projects

# functions in wrapped methods are renamed to simplify common tests

pytest_plugins = [
    "fixtures.accounts",
    "fixtures.coins",
    "fixtures.deployments",
    "fixtures.functions",
    "fixtures.pooldata",
    "fixtures.setup",
]

_pooldata = {}


def pytest_addoption(parser):
    parser.addoption("--pool", help="comma-separated list of pools to target")


def pytest_sessionstart():
    # load `pooldata.json` for each pool
    project = get_loaded_projects()[0]
    for path in [i for i in project._path.glob("contracts/pools/*") if i.is_dir()]:
        with path.joinpath("pooldata.json").open() as fp:
            _pooldata[path.name] = json.load(fp)
            _pooldata[path.name].update(
                name=path.name, swap_contract=next(i.stem for i in path.glob("StableSwap*"))
            )


def pytest_generate_tests(metafunc):
    if "pool_data" in metafunc.fixturenames:
        # parametrize `pool_data`
        if metafunc.config.getoption("pool"):
            params = metafunc.config.getoption("pool").split(",")
        else:
            params = list(_pooldata)
        metafunc.parametrize("pool_data", params, indirect=True, scope="session")


# isolation setup


@pytest.fixture(autouse=True)
def isolation_setup(fn_isolation):
    pass


# main parametrized fixture, used to pass data about each pool into the other fixtures


@pytest.fixture(scope="module")
def pool_data(request):
    return _pooldata[request.param]


@pytest.fixture(scope="session")
def project():
    yield get_loaded_projects()[0]
