"""Read Solana balances, token supply, and RPC node status."""
import argparse
import json
from rpc import RpcError, rpc, sol, validate_address


def balance(address):
    validate_address(address)
    result = rpc("getBalance", [address, {"commitment": "confirmed"}])
    return {"address": address, "slot": result["context"]["slot"],
            "lamports": result["value"], "sol": sol(result["value"])}


def token_supply(mint):
    validate_address(mint)
    return rpc("getTokenSupply", [mint, {"commitment": "confirmed"}])


def status():
    return {"health": rpc("getHealth"), "version": rpc("getVersion"),
            "slot": rpc("getSlot", [{"commitment": "confirmed"}])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="RPC health, software version, and slot")
    commands.add_parser("balance", help="Native SOL balance").add_argument("address")
    commands.add_parser("supply", help="SPL token mint supply").add_argument("mint")
    args = parser.parse_args()
    try:
        if args.command == "balance":
            result = balance(args.address)
        elif args.command == "supply":
            result = token_supply(args.mint)
        else:
            result = status()
        print(json.dumps(result, indent=2))
    except (ValueError, RpcError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
