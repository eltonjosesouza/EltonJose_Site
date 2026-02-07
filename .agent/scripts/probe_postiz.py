import requests
import os
import dotenv

dotenv.load_dotenv(".env.local")

API_URL = "https://posts.eltonjose.com.br"
API_KEY = os.getenv("POSTIZ_API_KEY")

if not API_KEY:
    print("❌ POSTIZ_API_KEY not found in .env.local")
    exit(1)


def try_request(url, headers_variant, name):
    try:
        resp = requests.get(url, headers=headers_variant, timeout=5)
        print(f"[{name}] GET {url}: {resp.status_code}")
        if resp.status_code == 200:
            print(f"   ✅ SUCCESS with {name}!")
            return True
    except Exception as e:
        print(f"[{name}] GET {url}: Error {e}")
    return False

# Test variations
variations = [
    ("Bearer", {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}),
    ("No-Bearer", {"Authorization": API_KEY, "Content-Type": "application/json"}),
    ("X-API-KEY", {"X-API-KEY": API_KEY, "Content-Type": "application/json"}),
    ("x-api-key (lower)", {"x-api-key": API_KEY, "Content-Type": "application/json"}),
    ("apikey", {"apikey": API_KEY, "Content-Type": "application/json"}),
]

print(f"🔍 Probing {API_URL} with key {API_KEY[:4]}...***")

target_endpoint = "/api/integrations"
url = f"{API_URL}{target_endpoint}"

for name, headers in variations:
    if try_request(url, headers, name):
        break

# Also try query param
url_query = f"{API_URL}{target_endpoint}?apiKey={API_KEY}"
try_request(url_query, {"Content-Type": "application/json"}, "Query Param")

