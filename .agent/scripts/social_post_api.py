import requests
import json
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(".env.local")
API_KEY = os.getenv("POSTIZ_API_KEY") or "ee43aef274f762c5408c4be2525b7cc8b1cbd336444d8f8da0e9a84c3e527320"
BASE_URL = "https://posts.eltonjose.com.br/api/public/v1"

def request_with_retry(method, url, headers, json=None, files=None, max_retries=5):
    """
    Executes a request with exponential backoff on 429.
    Returns the response object or None if failed after retries.
    """
    delay = 60 # Start with 60s
    for attempt in range(max_retries + 1):
        try:
            if method == "POST":
                resp = requests.post(url, headers=headers, json=json, files=files)
            elif method == "GET":
                resp = requests.get(url, headers=headers)
            else:
                return None

            if resp.status_code == 429:
                if attempt < max_retries:
                    print(f"   ⚠️ Hit Rate Limit (429). Sleeping {delay}s before retry {attempt+1}/{max_retries}...")
                    time.sleep(delay)
                    delay *= 2 # Exponential backoff
                    continue
                else:
                     print("   ❌ Max retries reached for 429.")
                     return resp

            # If not 429, valid response (success or other error)
            return resp

        except Exception as e:
            print(f"   ❌ Exception in request: {e}")
            return None
    return None

def get_integrations_map():
    url = f"{BASE_URL}/integrations"
    headers = {"Authorization": API_KEY}
    resp = request_with_retry("GET", url, headers)

    if resp and resp.status_code == 200:
        data = resp.json()
        return {i["id"]: i["identifier"] for i in data}
    else:
        print(f"❌ Failed to fetch integrations: {resp.status_code if resp else 'Err'}")
        return {}

def upload_media(file_path):
    url = f"{BASE_URL}/upload"
    headers = {"Authorization": API_KEY}
    path_obj = Path(file_path)

    # Validation
    if not path_obj.exists():
        print(f"   ⚠️ File not found: {file_path}")
        return None

    print(f"   📤 Uploading {path_obj.name}...")

    # We need to re-open file for each retry in request_with_retry if we were passing file handle directly.
    # But requests files arg consumes the handle. So we need to handle retries here or pass a way to open.
    # tailored retry logic for upload:

    delay = 60
    for attempt in range(5):
        try:
            with open(file_path, "rb") as f:
                files = {"file": (path_obj.name, f, "image/jpeg")}
                resp = requests.post(url, headers=headers, files=files)

            if resp.status_code == 429:
                print(f"   ⚠️ Hit Rate Limit (429). Sleeping {delay}s before retry {attempt+1}/5...")
                time.sleep(delay)
                delay *= 2
                continue

            if resp.status_code == 201:
                data = resp.json()
                print("   ✅ Uploaded.")
                # Success - Sleep 10s to be safe
                time.sleep(10)
                return {"id": data.get("id"), "path": data.get("path")}
            else:
                print(f"   ❌ Upload Failed: {resp.status_code} {resp.text}")
                return None

        except Exception as e:
            print(f"   ❌ Exception upload: {e}")
            return None

    return None

def process_schedule(post_dir):
    schedule_path = Path(post_dir) / "social_schedule.json"
    if not schedule_path.exists():
        print(f"❌ Schedule file not found: {schedule_path}")
        return

    print(f"📂 Reading schedule...")
    with open(schedule_path, "r") as f:
        schedule = json.load(f)

    # 1. Fetch Integrations
    integrations_map = get_integrations_map()
    print(f"ℹ️  Found {len(integrations_map)} integrations.")

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    for i, item in enumerate(schedule):
        print(f"\n📝 Processing Post {i+1}/{len(schedule)}...")

        # Safe Access
        pc_list = item.get("postsAndComments", [])
        if not pc_list:
            print("   ⚠️ No postsAndComments content found.")
            continue

        post_data = pc_list[0]
        content = post_data.get("content", "")
        local_attachments = post_data.get("attachments", [])

        # Upload Attachments
        api_images = []
        for local_path in local_attachments:
            # Resolving path logic
            real_path = Path(local_path)
            if not real_path.exists():
                 real_path = Path(post_dir) / Path(local_path).name
            if not real_path.exists():
                 real_path = Path(os.getcwd()) / local_path

            uploaded = upload_media(str(real_path))
            if uploaded:
                api_images.append(uploaded)
            else:
                print(f"   ⚠️ Skipping attachment {local_path} due to upload failure.")

        # Settings Logic
        integration_id = item.get("integrationId")
        platform = integrations_map.get(integration_id)

        json_settings_list = item.get("settings", [])
        settings_kv = {}
        if isinstance(json_settings_list, list):
             for s in json_settings_list:
                 if isinstance(s, dict) and "key" in s and "value" in s:
                     settings_kv[s["key"]] = s["value"]

        api_settings = {}
        api_settings = {}
        if platform:
            api_settings["__type"] = platform

            # Platform Specifics
            if platform == "instagram":
                media_type = settings_kv.get("media_type")
                if media_type == "STORY":
                     api_settings["post_type"] = "story"
                     print("   ℹ️  Enforcing Instagram Story format.")
                else:
                     api_settings["post_type"] = "post"
            elif platform == "facebook":
                 # Facebook API doesn't explicitly document 'story' in public docs samples.
                 # If user wants story, we can try passing it, but likely it defaults to feed.
                 url = settings_kv.get("url")
                 if url:
                     api_settings["url"] = url
                     print(f"   ℹ️  Adding URL to Facebook post: {url}")

        payload = {
            "type": item.get("type", "now"),
            "date": item.get("date"),
            "shortLink": item.get("shortLink", False),
            "tags": [],
            "posts": [
                {
                    "integration": { "id": integration_id },
                    "value": [
                        {
                            "content": content,
                            "image": api_images
                        }
                    ],
                    "settings": api_settings
                }
            ]
        }

        print("   🚀 Sending Payload...")
        post_url = f"{BASE_URL}/posts"

        resp = request_with_retry("POST", post_url, headers, json=payload)

        if resp:
            if resp.status_code == 201:
                res_data = resp.json()
                if isinstance(res_data, list):
                     ids = [x.get('id') for x in res_data]
                     print(f"   ✅ SUCCESS! Created Post IDs: {ids}")
                else:
                     print(f"   ✅ SUCCESS! Created Post ID: {res_data.get('id')}")
            else:
                print(f"   ❌ FAILED: {resp.status_code} {resp.text}")

        # Sleep after post
        print("   ⏳ Sleeping 30s...")
        time.sleep(30)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python social_post_api.py <post_dir>")
        sys.exit(1)

    process_schedule(sys.argv[1])
