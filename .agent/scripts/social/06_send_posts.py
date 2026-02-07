import sys
import json
import time
import os
from pathlib import Path
from datetime import datetime, timedelta

# Import Client
try:
    from . import postiz_client as client_module
    PostizClient = client_module.PostizClient
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("PostizClient", str(Path(__file__).parent / "06_postiz_client.py"))
    client_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(client_mod)
    PostizClient = client_mod.PostizClient

def convert_tags_to_api_format(raw_tags):
    """Convert tags from string array or dict array to API format"""
    api_tags = []
    for tag in raw_tags:
        if isinstance(tag, str):
            api_tags.append({"value": tag.lower().replace(" ", "-"), "label": tag})
        elif isinstance(tag, dict) and "value" in tag:
            api_tags.append(tag)
    return api_tags

def process_schedule(post_dir):
    schedule_path = Path(post_dir) / "social_schedule.json"
    if not schedule_path.exists():
        print(f"❌ Schedule file not found: {schedule_path}")
        return

    print(f"📂 Reading schedule...")
    with open(schedule_path, "r") as f:
        schedule = json.load(f)

    client = PostizClient()
    integrations_map = client.get_integrations()
    print(f"ℹ️  Found {len(integrations_map)} integrations.")

    for i, item in enumerate(schedule):
        print(f"\n📝 Processing Post {i+1}/{len(schedule)}...")

        # Detect format: new model format or legacy format
        is_model_format = "posts" in item and "postsAndComments" not in item

        if is_model_format:
            # New model format: item already has the API structure
            integration_id = item["posts"][0]["integration"]["id"]
            content = item["posts"][0]["value"][0]["content"]
            local_images = item["posts"][0]["value"][0].get("image", [])
            api_settings = item["posts"][0].get("settings", {})

            # Check if Instagram Story with multiple images
            is_instagram_story = (
                api_settings.get("__type") == "instagram" and
                api_settings.get("post_type") == "story"
            )

            if is_instagram_story and len(local_images) > 1:
                # Send each story image as separate post with 1min interval
                print(f"   📸 Instagram Story with {len(local_images)} images - sending as separate posts...")
                base_time = datetime.fromisoformat(item.get("date", "").replace("Z", "+00:00"))

                for img_idx, img in enumerate(local_images):
                    local_path = img.get("path", "")
                    real_path = Path(local_path)
                    if not real_path.exists():
                        real_path = Path(post_dir) / Path(local_path).name
                    if not real_path.exists():
                        real_path = Path(os.getcwd()) / local_path

                    uploaded = client.upload_media(str(real_path))
                    if not uploaded:
                        print(f"   ⚠️ Skipping image {local_path} due to upload failure.")
                        continue

                    # Calculate time with 1min interval
                    post_time = base_time + timedelta(minutes=img_idx)
                    time_str = post_time.strftime("%Y-%m-%dT%H:%M:%SZ")

                    print(f"   🚀 Sending Story {img_idx+1}/{len(local_images)} at {time_str} (repeats for 2 days)...")

                    # Calculate end date (2 days after start)
                    end_time = post_time + timedelta(days=2)
                    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

                    # Get tags from item and convert to API format
                    api_tags = convert_tags_to_api_format(item.get("tags", []))

                    # Build payload for single-image story with repeat
                    payload = {
                        "type": item.get("type", "now"),
                        "date": time_str,
                        "shortLink": item.get("shortLink", False),
                        "tags": api_tags,
                        "posts": [{
                            "integration": {"id": integration_id},
                            "value": [{
                                "content": content,
                                "image": [uploaded]
                            }],
                            "settings": api_settings
                        }],
                        "repeat": {
                            "frequency": "daily",
                            "interval": 1,
                            "endDate": end_time_str
                        }
                    }

                    result = client.create_post(payload)
                    if result:
                        print(f"   ✅ Story {img_idx+1} created successfully")
                    else:
                        print(f"   ❌ Failed to create story {img_idx+1}")

                    if img_idx < len(local_images) - 1:
                        time.sleep(5)

                continue  # Skip normal processing

            # Normal processing for non-story or single-image story
            api_images = []
            for img in local_images:
                local_path = img.get("path", "")
                real_path = Path(local_path)
                if not real_path.exists():
                    real_path = Path(post_dir) / Path(local_path).name
                if not real_path.exists():
                    real_path = Path(os.getcwd()) / local_path

                uploaded = client.upload_media(str(real_path))
                if uploaded:
                    api_images.append(uploaded)
                else:
                    print(f"   ⚠️ Skipping image {local_path} due to upload failure.")

            # Build payload maintaining model structure
            payload = {
                "type": item.get("type", "now"),
                "date": item.get("date"),
                "shortLink": item.get("shortLink", False),
                "tags": convert_tags_to_api_format(item.get("tags", [])),
                "posts": [{
                    "integration": {"id": integration_id},
                    "value": [{
                        "content": content,
                        "image": api_images
                    }],
                    "settings": api_settings
                }]
            }

        else:
            # Legacy format: convert to API format
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
                real_path = Path(local_path)
                if not real_path.exists():
                    real_path = Path(post_dir) / Path(local_path).name
                if not real_path.exists():
                    real_path = Path(os.getcwd()) / local_path

                uploaded = client.upload_media(str(real_path))
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
            if platform:
                api_settings["__type"] = platform
                if platform == "instagram":
                    media_type = settings_kv.get("media_type")
                    if str(media_type).lower() == "story":
                        api_settings["post_type"] = "story"
                        print("   ℹ️  Enforcing Instagram Story format.")
                    else:
                        api_settings["post_type"] = "post"
                elif platform == "facebook":
                    url = settings_kv.get("url")
                    if url:
                        api_settings["url"] = url
                        print(f"   ℹ️  Adding URL to Facebook post: {url}")

            payload = {
                "type": item.get("type", "now"),
                "date": item.get("date"),
                "shortLink": item.get("shortLink", False),
                "tags": convert_tags_to_api_format(item.get("tags", [])),
                "posts": [{
                    "integration": {"id": integration_id},
                    "value": [{
                        "content": content,
                        "image": api_images
                    }],
                    "settings": api_settings
                }]
            }

        result = client.create_post(payload)
        if result:
            print(f"   ✅ Post created successfully: {result}")
        else:
            print(f"   ❌ Failed to create post")
            print(f"   Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        print("   ⏳ Sleeping 30s...")
        time.sleep(30)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 06_send_posts.py <post_dir>")
        sys.exit(1)
    process_schedule(sys.argv[1])
