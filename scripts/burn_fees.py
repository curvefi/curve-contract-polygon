from brownie import ABurner, ChildBurner, StableSwapAave, accounts, history, interface


def main():
    deployer = accounts.load("curve-deploy")
    admin = interface.ProxyAdmin("0x7EAfd3cd937628b9671d5f8B9c823f4AAc914808")

    # withdraw admin fees to the burner
    swap = StableSwapAave.at("0x445FE580eF8d70FF569aB36e80c647af338db351")
    admin.execute(
        swap, swap.withdraw_admin_fees.encode_input(), {"from": deployer, "required_confs": 3}
    )

    # burn - unwrap aTokens to underlying assets, swap for USDC and transfer to the bridge
    burner = ABurner.at("0xA237034249290De2B07988Ac64b96f22c0E76fE0")
    for i in range(3):
        burner.burn(swap.coins(i), {"from": deployer, "required_confs": 0})
    history.wait()

    # send USDC over the bridge
    usdc = interface.BridgeToken("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
    bridge = ChildBurner.at("0x4473243A61b5193670D1324872368d015081822f")
    amount = usdc.balanceOf(bridge)
    tx = admin.execute(bridge, bridge.withdraw.encode_input(usdc), {"from": deployer})

    print(f"Burning phase 1 complete!\nAmount: {amount/1e6:,.2f} USDC\nBridge txid: {tx.txid}")
    print("\nUse `brownie run exit --network mainnet` to claim on ETH once the checkpoint is added")
