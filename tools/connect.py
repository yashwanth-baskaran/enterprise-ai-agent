"""
tools/connect.py
Establish and test connection to the business system API.
Reads credentials from .env — never hardcode secrets here.
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

URL  = os.getenv("BUSINESS_SYSTEM_URL")
DB   = os.getenv("BUSINESS_SYSTEM_DB")
USER = os.getenv("BUSINESS_SYSTEM_USER")
KEY  = os.getenv("BUSINESS_SYSTEM_API_KEY")


def call(endpoint: str, method: str, params: list) -> dict:
    """Make a JSON-RPC call to the business system."""
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "id": 1,
        "params": {
            "service": endpoint,
            "method": method,
            "args": params,
        },
    }
    response = requests.post(
        f"{URL}/web/dataset/call_kw",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    if "error" in result:
        raise RuntimeError(result["error"]["data"]["message"])
    return result.get("result")


def test_connection() -> bool:
    """Quick connectivity check. Returns True if credentials work."""
    try:
        uid = requests.post(
            f"{URL}/web/dataset/call_kw",
            json={
                "jsonrpc": "2.0",
                "method": "call",
                "id": 1,
                "params": {
                    "service": "common",
                    "method": "authenticate",
                    "args": [DB, USER, KEY, {}],
                },
            },
            timeout=10,
        ).json().get("result")
        return isinstance(uid, int) and uid > 0
    except Exception as e:
        print(f"Connection failed: {e}")
        return False


if __name__ == "__main__":
    ok = test_connection()
    print("✓ Connected" if ok else "✗ Connection failed — check .env")
