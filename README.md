# curve-contract-polygon
Curve.fi exchange implementation for Polygon.

## Testing and Development

### Dependencies

* [python3](https://www.python.org/downloads/release/python-368/) from version 3.6 to 3.8, python3-dev
* [brownie](https://github.com/iamdefinitelyahuman/brownie) - tested with version [1.14.5](https://github.com/eth-brownie/brownie/releases/tag/v1.14.5)
* [ganache-cli](https://github.com/trufflesuite/ganache-cli) - tested with version [6.12.1](https://github.com/trufflesuite/ganache-cli/releases/tag/v6.12.1)

## Setup

1. To get started, first create and initialize a Python [virtual environment](https://docs.python.org/3/library/venv.html).

2. clone the repo and install the developer dependencies:

    ```bash
    git clone https://github.com/curvefi/curve-contract-polygon.git
    cd curve-contract-polygon
    pip install -r requirements.txt
    ```

3. Add Polygon to your local brownie networks:

    ```bash
    brownie network import network-config.yaml
    ```

### Running the Tests

Testing is done against a forked mainnet. To run the entire suite:

```bash
brownie test
```

To run tests on a specific pool:

```bash
brownie test --pool <POOL NAME>
```

Valid pool names are the names of the subdirectories within [`contracts/pools`](contracts/pools).

You can optionally include the `--coverage` flag to view a coverage report upon completion of the tests.

## License

(c) Curve.Fi, 2021 - [All rights reserved](LICENSE).
