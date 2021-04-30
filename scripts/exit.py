"""Gracefully exit from Matic ... now in Python.

Script for withdrawing an ERC20 asset from Matic Mainnet back to Ethereum.
This is a two part script, the first portion requires you to burn an ERC20 asset
on the Matic Network, and then after the burn is checkpointed on Ethereum mainnet,
collect the ERC20 asset.
"""
from brownie import accounts
from brownie.project import load as load_project

# MUST SET VARIABLES BEFORE BURNING ON MATIC
MSG_SENDER = accounts.add()
MATIC_ERC20_ASSET_ADDR = ""
BURN_AMOUNT = 0


def burn_asset_on_matic():
    ChildERC20 = load_project("maticnetwork/pos-portal@1.5.2").ChildERC20
    asset = ChildERC20.at(MATIC_ERC20_ASSET_ADDR)
    tx = asset.withdraw(BURN_AMOUNT, {"from": MSG_SENDER})
    print("Burn transaction has been sent.")
    print(f"Visit https://explorer-mainnet.maticvigil.com/tx/{tx.txid} for confirmation")
