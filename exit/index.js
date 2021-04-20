require('dotenv').config();
const Web3 = require('web3');
const MaticPOSClient = require('@maticnetwork/maticjs').MaticPOSClient;
const Tx = require('ethereumjs-tx').Transaction;


const parentProvider = process.env.PARENT_PROVIDER;
const maticProvider = process.env.MATIC_PROVIDER;
const senderPrivateKey = process.env.PRIVATE_KEY;
const rootChainManagerAddress = process.env.ROOT_CHAIN_MANAGER;

const web3 = new Web3(parentProvider);
const maticPOSClient = new MaticPOSClient({
    network: "testnet",
    version: "mumbai",
    parentProvider,
    maticProvider,
});
const senderAddress = web3.eth.accounts.privateKeyToAccount(senderPrivateKey).address;
const burnTxHash =  process.argv[2];


(async (burnTxHash, rootChainManagerAddress, senderAddress, senderPrivateKey) => {
    const exitCallData = await maticPOSClient
        .exitERC20(burnTxHash, { from: senderAddress, encodeAbi: true });

    let gasPrice = await web3.eth.getGasPrice();
    gasPrice = Number(gasPrice).toString(16);

    senderPrivateKey = new Buffer.from(senderPrivateKey, 'hex');
    const txCount = await web3.eth.getTransactionCount(senderAddress);
    const rawTx = {
        nonce: '0x0' + txCount,
        gasPrice: '0x' + gasPrice,
        gasLimit: '0x271000',
        value: '0x00',
        to: rootChainManagerAddress,
        data: exitCallData.data,
    };
    const tx = new Tx(rawTx, { 'chain': 'goerli' });
    tx.sign(senderPrivateKey);
    const serializedTx = tx.serialize();

    web3.eth.sendSignedTransaction('0x' + serializedTx.toString('hex'));

    console.log('Sent tx to the ethereum network');
})(burnTxHash, rootChainManagerAddress, senderAddress, senderPrivateKey);
