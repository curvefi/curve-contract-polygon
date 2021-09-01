from brownie import Contract, accounts, history


def main():
    deploy = accounts.load("curve-deploy")
    admin = Contract("0x7EAfd3cd937628b9671d5f8B9c823f4AAc914808")

    # withdraw admin fees to the burners
    swap = Contract("0x445FE580eF8d70FF569aB36e80c647af338db351")
    swap_btc = Contract("0xC2d95EEF97Ec6C17551d45e77B590dc1F9117C67")
    admin.execute(
        swap,
        swap.withdraw_admin_fees.encode_input(),
        {"from": deploy, "gas_price": "20 gwei", "required_confs": 0},
    )
    admin.execute(
        swap_btc,
        swap_btc.withdraw_admin_fees.encode_input(),
        {"from": deploy, "gas_price": "20 gwei", "required_confs": 0},
    )
    history.wait()

    # burn am3CRV fees
    burner = Contract("0xA237034249290De2B07988Ac64b96f22c0E76fE0")
    for i in range(3):
        try:
            burner.burn(
                swap.coins(i),
                {"from": deploy, "gas_price": "20 gwei", "gas_limit": 2000000, "required_confs": 0},
            )
        except Exception:
            pass

    # burn renBTC fees
    burner = Contract("0x5109abc063164d49c148a7ae970f631febbda4fa")
    for i in range(2):
        try:
            burner.burn(
                swap_btc.coins(i),
                {"from": deploy, "gas_price": "20 gwei", "gas_limit": 2000000, "required_confs": 0},
            )
        except Exception:
            pass

    history.wait()

    # send USDC over the bridge
    usdc = Contract("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
    bridge = Contract("0x4473243A61b5193670D1324872368d015081822f")
    amount = usdc.balanceOf(bridge)
    tx = admin.execute(
        bridge, bridge.withdraw.encode_input(usdc), {"from": deploy, "gas_price": "20 gwei"}
    )

    print(f"Burning phase 1 complete!\nAmount: {amount/1e6:,.2f} USDC\nBridge txid: {tx.txid}")
    print("\nUse `brownie run exit --network mainnet` to claim on ETH once the checkpoint is added")
