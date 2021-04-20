# Exit script

### Dependencies

[node](https://nodejs.org/en/) version 12.13

## Setup

1. To get started, first run the command:
    
    ```bash
    npm install
    ```
    
2. Then create .env file with the following constants:

    ```bash
    PARENT_PROVIDER = https://goerli.infura.io/v3/<API_KEY> # testnet
    MATIC_PROVIDER = https://rpc-mumbai.matic.today # testnet
    PRIVATE_KEY = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ROOT_CHAIN_MANAGER = 0x0000000000000000000000000000000000000000
    ```
    

## Running the script

To run the script:

```bash
node index.js <tx_id>
```
