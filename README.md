# solana-api — Python Solana RPC examples

A small, dependency-free Python CLI for reading SOL balances, SPL token supply, and RPC node status through the Solana JSON-RPC API.

Independent example project, not an official Solana SDK. Read-only: no wallet signing, transfers, or trading.

## Quick start

Requires Python 3.11 or newer and Git. Uses only the Python standard library; no pip install or API key is required for the public RPC endpoint.

```sh
git clone https://github.com/wasely/solana-api.git
cd solana-api
python solana.py status
python solana.py balance 11111111111111111111111111111111
python solana.py supply So11111111111111111111111111111111111111112
```

The included addresses are public program/mint examples, not personal wallets. Replace them with the addresses you want to inspect.

## What it does

- `status`: node health, software version, and confirmed slot.
- `balance ADDRESS`: native SOL balance as integer lamports and an exact decimal string.
- `supply MINT`: token supply, including the provider's raw amount and decimals.
- Importable Python functions and JSON CLI output.

## Choose a cluster or RPC provider

Defaults to Solana mainnet at `https://api.mainnet-beta.solana.com`.
Use `SOLANA_RPC_URL` for devnet or your own provider.

PowerShell:

```powershell
$env:SOLANA_RPC_URL = "https://api.devnet.solana.com"
```

macOS / Linux:

```sh
export SOLANA_RPC_URL="https://api.devnet.solana.com"
```

Run the quick-start commands after setting the variable. Devnet and mainnet have separate data. Public endpoints may return HTTP 403 or 429; wait before retrying or configure your own RPC provider. Requests time out after 15 seconds. The tool does not automatically retry.

Provider URLs can contain API keys. Keep them in your local environment, not in commits. These scripts do not load `.env` files automatically. They never need a seed phrase or private key.

## Use from Python

Run from this repository directory:

```python
from solana import balance, token_supply, status

print(balance("11111111111111111111111111111111"))
print(status())
```

## Limits

The `supply` command requires a token mint address, not a wallet or token account. It returns the mint's reported supply, not circulating supply, price, or market cap. Native SOL balances do not include wrapped SOL or other tokens. Values depend on your chosen cluster.

Reads use confirmed commitment, so recent data can change. Address validation checks base58 and decoded length; it does not prove an account exists. The transport reports HTTP, network, JSON, and JSON-RPC errors without echoing provider response text or URLs.

## Tests

```sh
python -m unittest discover -v
```

Ten offline tests cover the tool's behavior, address validation, exact balance formatting, malformed JSON-RPC responses, and HTTP/network errors. Live read-only examples were also checked against Solana devnet on 2026-10-15. Live results change and are not part of the offline test suite.

## References

- [Solana JSON-RPC reference](https://solana.com/docs/rpc/http)
- [getBalance](https://solana.com/docs/rpc/http/getbalance)
- [getTokenSupply](https://solana.com/docs/rpc/http/gettokensupply)
