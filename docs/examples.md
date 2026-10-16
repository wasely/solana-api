# Solana RPC examples in Python

## Check your RPC node

```sh
python solana.py status
```

Returns health, software version, and the confirmed slot. These are separate requests, not an atomic snapshot. Failure in any request exits with an error.

## Read a SOL balance

```sh
python solana.py balance 11111111111111111111111111111111
```

The example address is the System Program. Substitute a wallet's public address. `lamports` is an integer; `sol` is an exact decimal string. Wrapped SOL and SPL tokens are not included.

## Read token mint supply

```sh
python solana.py supply So11111111111111111111111111111111111111112
```

This uses the wrapped SOL mint as an example. The native mint can report zero supply even when wrapped SOL accounts exist; this is not a total for wrapped SOL balances. Use the mint address of your target SPL token to inspect its reported supply.

Prefer `amount` and `decimals` when exact arithmetic matters. `uiAmount` is a floating-point convenience value. Mint supply is not circulating supply or market cap.

## Read from Python

```python
from solana import balance, token_supply, status

wallet = balance("11111111111111111111111111111111")
print(wallet["lamports"])
print(wallet["sol"])
```

Run from the repository directory. These examples do not require a pip package.

## Switch networks

Set `SOLANA_RPC_URL` before running a command. See the [configuration instructions](../README.md#choose-a-cluster-or-rpc-provider) for PowerShell and POSIX shells.

[Back to README](../README.md)
