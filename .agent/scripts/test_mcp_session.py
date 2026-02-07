import requests
import json
import os
import sys

URL = "https://posts.eltonjose.com.br/api/mcp/ee43aef274f762c5408c4be2525b7cc8b1cbd336444d8f8da0e9a84c3e527320"

def test_session():
    # 1. Initialize
    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    print("🚀 Sending Initialize...")
    try:
        resp = requests.post(URL, json=init_payload, headers=headers, stream=True)
        print(f"Init Status: {resp.status_code}")

        session_id = resp.headers.get("mcp-session-id")
        print(f"Session ID: {session_id}")

        if not session_id:
            print("❌ No session ID returned")
            return

        # 2. List Tools
        tools_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        # Add session ID to headers
        headers["mcp-session-id"] = session_id

        # We need a NEW request. The previous one is a stream (potentially).
        # But we can just fire a new POST.
        print("🛠 Sending Tools List...")
        resp2 = requests.post(URL, json=tools_payload, headers=headers)
        print(f"Tools Status: {resp2.status_code}")
        print(f"Tools Response: {resp2.text[:500]}") # Print first 500 chars

        # Also try query param in case header fails
        if resp2.status_code != 200:
            print("Trying query param...")
            resp3 = requests.post(f"{URL}?sessionId={session_id}", json=tools_payload, headers={"Content-Type": "application/json"})
            print(f"Tools (Query) Status: {resp3.status_code}")
            print(f"Tools (Query) Response: {resp3.text[:500]}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_session()
