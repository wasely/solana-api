"""Small read-only Solana JSON-RPC transport; Python standard library only."""
import json
import os
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

DEFAULT_RPC = "https://api.mainnet-beta.solana.com"
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


class RpcError(RuntimeError):
    pass


def validate_address(address):
    if not isinstance(address, str) or not 32 <= len(address) <= 44:
        raise ValueError("Address must be a base58-encoded 32-byte Solana public key.")
    value = 0
    for char in address:
        if char not in ALPHABET:
            raise ValueError("Address contains an invalid base58 character.")
        value = value * 58 + ALPHABET.index(char)
    leading = len(address) - len(address.lstrip("1"))
    if leading + (value.bit_length() + 7) // 8 != 32:
        raise ValueError("Address must decode to exactly 32 bytes.")
    return address


def sol(lamports):
    if type(lamports) is not int or lamports < 0:
        raise RpcError("RPC returned an invalid lamport balance.")
    return f"{lamports // 1_000_000_000}.{lamports % 1_000_000_000:09d}"


def rpc(method, params=None, endpoint=None):
    endpoint = endpoint or os.environ.get("SOLANA_RPC_URL") or DEFAULT_RPC
    parsed = urlsplit(endpoint)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("SOLANA_RPC_URL must be an HTTP or HTTPS URL.")
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method,
                       "params": [] if params is None else params}).encode()
    request = Request(endpoint, data=body, headers={"Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=15) as response:
            data = json.load(response)
    except HTTPError as exc:
        hint = " Try your own RPC provider or wait before retrying." if exc.code in (403, 429) else ""
        raise RpcError(f"RPC HTTP {exc.code}.{hint}") from None
    except (URLError, TimeoutError, socket.timeout, OSError):
        raise RpcError("RPC network request failed. Check connectivity and SOLANA_RPC_URL.") from None
    except (ValueError, UnicodeError):
        raise RpcError("RPC returned invalid JSON.") from None
    if not isinstance(data, dict) or data.get("jsonrpc") != "2.0" or data.get("id") != 1:
        raise RpcError("RPC returned an invalid response envelope.")
    if data.get("error") is not None:
        error = data["error"]
        code = error.get("code") if isinstance(error, dict) else None
        safe_code = code if type(code) is int else "unknown"
        raise RpcError(f"RPC error {safe_code}. Check parameters and provider documentation.")
    if "result" not in data:
        raise RpcError("RPC response has no result.")
    return data["result"]
