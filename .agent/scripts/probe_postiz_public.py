import requests
import os
from dotenv import load_dotenv

load_dotenv(".env.local")
API_KEY = os.getenv("POSTIZ_API_KEY") or "ee43aef274f762c5408c4be2525b7cc8b1cbd336444d8f8da0e9a84c3e527320"
FULL_URL = "https://posts.eltonjose.com.br"

def try_request(url):
    print(f"🔍 Checking {url}...")
    headers = {
        "Authorization": API_KEY, # No 'Bearer' per docs
        "Content-Type": "application/json"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            print("   ✅ SUCCESS")
            print(f"   Response: {resp.text[:200]}")
            return True
    except Exception as e:
        print(f"   Error: {e}")
    return False

# Potential Base URLs
base_urls = [
    f"{FULL_URL}/api/public/v1",
    f"{FULL_URL}/public/v1",
    f"{FULL_URL}/api/v1",
]

found = False
for base in base_urls:
    if try_request(f"{base}/integrations"):
        found = True
        break

if not found:
    print("❌ Could not find valid Public API endpoint.")
