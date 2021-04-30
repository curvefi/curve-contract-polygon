"""Fetch Matic Network contract deployment data."""
import json
from pathlib import Path

import requests

# Endpoint for retrieving matic data
DATA_URI = "https://static.matic.network/network/{network}/{version}/index.json"


def fetch_deployment_data(network: str, version: str, force_fetch: bool = True) -> dict:
    """Fetch matic deployment data with the side effect of writing to disk.

    Args:
        network: The network name of interest, e.g. 'mainnet' or 'testnet'
        version: The network version of interest e.g. 'v1' or 'mumbai'
    """
    path = Path(__file__).parent.parent.joinpath(f"{network}-{version}.json")

    if not force_fetch and path.exists():
        try:
            with path.open() as fp:
                return json.load(fp)
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    print("Fetching matic deployment data...")

    URL = DATA_URI.format(network=network, version=version)
    data = requests.get(URL).json()

    with path.open("w") as fp:
        json.dump(data, fp, sort_keys=True, indent=2)

    print(f"Matic deployment data saved at {path.as_posix()}")
    return data


def main():
    return fetch_deployment_data("mainnet", "v1")
