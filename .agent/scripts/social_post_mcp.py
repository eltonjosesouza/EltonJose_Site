import requests
import json
import sys
import time
from pathlib import Path

# Configuration
API_KEY = "ee43aef274f762c5408c4be2525b7cc8b1cbd336444d8f8da0e9a84c3e527320"
URL = f"https://posts.eltonjose.com.br/api/mcp/{API_KEY}"

def post_posts(post_dir):
    schedule_path = Path(post_dir) / "social_schedule_base64.json"
    if not schedule_path.exists():
        print(f"❌ Schedule file not found: {schedule_path}")
        return

    print(f"📂 Reading schedule from {schedule_path}...")
    with open(schedule_path, "r") as f:
        schedule = json.load(f)

    print(f"📝 Found {len(schedule)} items in schedule.")

    # 1. Initialize Session
    print("🚀 Initializing MCP Session...")
    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "python-script", "version": "1.0"}
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    session_id = None
    try:
        # stream=True is critical for SSE
        with requests.post(URL, json=init_payload, headers=headers, stream=True) as resp:
            if resp.status_code != 200:
                print(f"❌ Initialize failed: {resp.status_code} {resp.text}")
                return

            session_id = resp.headers.get("mcp-session-id")
            if not session_id:
                print("❌ No session ID in headers")
                return

            print(f"✅ Session Established: {session_id}")

    except Exception as e:
        print(f"❌ Msg: {e}")
        return

    headers["mcp-session-id"] = session_id

    # 2. Loop through posts
    for i, item in enumerate(schedule):
        print(f"\n📤 Sending Post {i+1}/{len(schedule)}...")

        # Inject defaults if missing
        if "isPremium" not in item:
            item["isPremium"] = False
        if "shortLink" not in item:
            item["shortLink"] = False

        # We need a new ID for each request
        req_id = i + 2

        # MCP Tool Call Payload
        tool_payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {
                "name": "integrationSchedulePostTool",
                "arguments": {
                    "socialPost": [item] # Wrap item in array
                }
            }
        }

        try:
            # stream=True again
            with requests.post(URL, json=tool_payload, headers=headers, stream=True) as post_resp:
                if post_resp.status_code == 200:
                    # Parse SSE stream for the response with matching ID
                    success = False
                    for line in post_resp.iter_lines():
                        if not line: continue
                        decoded_line = line.decode('utf-8')

                        if decoded_line.startswith("data: "):
                            data_str = decoded_line[6:]
                            try:
                                data = json.loads(data_str)
                                if data.get("id") == req_id:
                                    if "result" in data:
                                        res = data["result"]
                                        print(f"   ✅ Tool Result: {json.dumps(res)[:200]}...")
                                        success = True
                                        break
                                    elif "error" in data:
                                        print(f"   ❌ Tool Error: {data['error']['message']}")
                                        success = True
                                        break
                            except:
                                pass
                    if not success:
                        print("   ⚠️ No matching JSON-RPC response found in stream.")
                else:
                    print(f"   ❌ HTTP Error: {post_resp.status_code} {post_resp.text}")

        except Exception as e:
            print(f"   ❌ Exception: {e}")

        time.sleep(1)

    print("\n🏁 Done.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python social_post_mcp.py <post_dir>")
        sys.exit(1)

    post_posts(sys.argv[1])
