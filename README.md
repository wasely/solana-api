# solana-api

**From [BLIX](https://blixvip.com) · [Explore the Solana trading terminal →](https://blixvip.com)**

**Query Solana RPC with Python. No dependencies.**

![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white) ![Dependencies: standard library](https://img.shields.io/badge/dependencies-standard_library-334155?style=flat-square) ![Mode: read only](https://img.shields.io/badge/mode-read_only-0F766E?style=flat-square)

Read native SOL balances, SPL token mint supply, and RPC node status with a small CLI or importable Python functions.

[Quick start](#quick-start) · [Examples](docs/examples.md) · [Python usage](#use-from-python) · [FAQ](#frequently-asked-questions)

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

## At a glance

| Task | Command |
| --- | --- |
| Inspect node health | `python solana.py status` |
| Read native SOL | `python solana.py balance ADDRESS` |
| Read SPL token supply | `python solana.py supply MINT` |

Replace uppercase placeholders with actual addresses or signatures.

## Example output

Example devnet balance response. Live values depend on the address, cluster, and time.

```json
{
  "address": "11111111111111111111111111111111",
  "slot": 511592641,
  "lamports": 1,
  "sol": "0.000000001"
}
```

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

## Frequently asked questions

### Do I need a Solana API key?

Not for the default public endpoint. For higher usage, configure your provider's URL with `SOLANA_RPC_URL`.

### How do I convert lamports to SOL?

1 SOL equals 1,000,000,000 lamports. The balance command returns both the integer amount and an exact decimal string.

### Is token supply the same as circulating supply?

No. `getTokenSupply` returns the mint's on-chain supply. It does not classify locked tokens, calculate market cap, or return a token price.

## Related tools

| Repository | Use it for |
| --- | --- |
| [axiom-api](https://github.com/wasely/axiom-api) | Recent Solana wallet transaction signatures |
| [fomo-api](https://github.com/wasely/fomo-api) | Native SOL balance snapshots for a watchlist |
| [solana-api](https://github.com/wasely/solana-api) | RPC health, balances, and token supply |

Each project is an independent, read-only tool. Axiom and Fomo accounts are not connected.

## References

- [Solana JSON-RPC reference](https://solana.com/docs/rpc/http)
- [getBalance](https://solana.com/docs/rpc/http/getbalance)
- [getTokenSupply](https://solana.com/docs/rpc/http/gettokensupply)
