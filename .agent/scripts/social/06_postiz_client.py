import requests
import os
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(".env.local")

class PostizClient:
    def __init__(self):
        self.api_key = os.getenv("POSTIZ_API_KEY") or "ee43aef274f762c5408c4be2525b7cc8b1cbd336444d8f8da0e9a84c3e527320"
        self.base_url = "https://posts.eltonjose.com.br/api/public/v1"
        self.cache_file = ".agent/social_uploads_cache.json"

    def _request_with_retry(self, method, url, headers, json_data=None, files=None, max_retries=5):
        delay = 60
        for attempt in range(max_retries + 1):
            try:
                if method == "POST":
                    if json_data:
                        print(f"   📤 POST {url} with payload: {json.dumps(json_data, indent=2)[:200]}...")
                    resp = requests.post(url, headers=headers, json=json_data, files=files, timeout=30)
                elif method == "GET":
                    resp = requests.get(url, headers=headers, timeout=30)
                else:
                    return None

                print(f"   📥 Response: {resp.status_code} {resp.text[:200]}")

                if resp.status_code == 429:
                    if attempt < max_retries:
                        print(f"   ⚠️ Hit Rate Limit (429). Sleeping {delay}s before retry {attempt+1}/{max_retries}...")
                        time.sleep(delay)
                        delay *= 2
                        continue
                    else:
                        print("   ❌ Max retries reached for 429.")
                        return resp
                return resp
            except Exception as e:
                print(f"   ❌ Exception in request: {e}")
                import traceback
                traceback.print_exc()
                return None
        return None

    def get_integrations(self):
        url = f"{self.base_url}/integrations"
        headers = {"Authorization": self.api_key}
        resp = self._request_with_retry("GET", url, headers)
        if resp and resp.status_code == 200:
            data = resp.json()
            return {i["id"]: i["identifier"] for i in data}
        print(f"❌ Failed to fetch integrations: {resp.status_code if resp else 'Err'}")
        return {}

    def _calculate_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_cache(self, cache_data):
        try:
            with open(self.cache_file, "w") as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save cache: {e}")

    def upload_media(self, file_path):
        url = f"{self.base_url}/upload"
        headers = {"Authorization": self.api_key}
        path_obj = Path(file_path)

        if not path_obj.exists():
            print(f"   ⚠️ File not found: {file_path}")
            return None

        file_hash = self._calculate_md5(file_path)
        cache = self._load_cache()
        if file_hash in cache:
            print(f"   ♻️  Skipping upload (Found in cache): {path_obj.name}")
            return cache[file_hash]

        print(f"   📤 Uploading {path_obj.name}...")
        delay = 60
        for attempt in range(5):
            try:
                with open(file_path, "rb") as f:
                    timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
                    unique_filename = f"{timestamp_str}-{path_obj.name}"
                    files = {"file": (unique_filename, f, "image/jpeg")}
                    resp = requests.post(url, headers=headers, files=files)

                if resp.status_code == 429:
                    print(f"   ⚠️ Hit Rate Limit (429). Sleeping {delay}s before retry...")
                    time.sleep(delay)
                    delay *= 2
                    continue

                if resp.status_code == 201:
                    data = resp.json()
                    print("   ✅ Uploaded.")
                    uploaded_data = {"id": data.get("id"), "path": data.get("path")}
                    cache[file_hash] = uploaded_data
                    self._save_cache(cache)
                    time.sleep(10)
                    return uploaded_data
                else:
                    print(f"   ❌ Upload Failed: {resp.status_code} {resp.text}")
                    return None
            except Exception as e:
                print(f"   ❌ Exception upload: {e}")
                return None
        return None

    def create_post(self, payload):
        url = f"{self.base_url}/posts"
        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
        print("   🚀 Sending Payload...")
        resp = self._request_with_retry("POST", url, headers, json_data=payload)

        if resp:
            if resp.status_code == 201:
                res_data = resp.json()
                if isinstance(res_data, list):
                     ids = [x.get('id') for x in res_data]
                     print(f"   ✅ SUCCESS! Created Post IDs: {ids}")
                     return ids
                else:
                     print(f"   ✅ SUCCESS! Created Post ID: {res_data.get('id')}")
                     return res_data.get('id')
            else:
                print(f"   ❌ FAILED: {resp.status_code} {resp.text}")
        else:
            print(f"   ❌ FAILED: No response from API (connection error)")
        return None
