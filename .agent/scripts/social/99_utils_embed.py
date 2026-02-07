import sys
import json
import base64
import mimetypes
from pathlib import Path

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"

def file_to_data_uri(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"⚠️ Warning: File not found: {file_path}")
        return None

    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        mime = get_mime_type(file_path)
        return f"data:{mime};base64,{encoded}"
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None

def embed_base64(post_dir):
    target_dir = Path(post_dir)
    input_path = target_dir / "social_schedule.json"
    output_path = target_dir / "social_schedule_base64.json"

    if not input_path.exists():
        print(f"❌ Error: {input_path} not found.")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        schedule = json.load(f)

    processed_count = 0
    for item in schedule:
        if "postsAndComments" in item:
            for post in item["postsAndComments"]:
                if "attachments" in post:
                    new_attachments = []
                    for att in post["attachments"]:
                        if att.startswith("http") or att.startswith("data:"):
                            new_attachments.append(att)
                        else:
                            # Assume local path
                            data_uri = file_to_data_uri(att)
                            if data_uri:
                                new_attachments.append(data_uri)
                                processed_count += 1
                            else:
                                # Keep original if failed? Or skip?
                                # Better to keep original and let tool fail if it must, or skip?
                                # User might fix path. Let's keep original for debug?
                                # Actually, if remote, original path is useless.
                                # But if we return None, it might break index.
                                # Let's skip if failed.
                                pass
                    post["attachments"] = new_attachments

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated Base64 Schedule: {output_path}")
    print(f"📸 Processed {processed_count} images.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python embed_base64_schedule.py <post_directory>")
        sys.exit(1)

    post_dir = sys.argv[1]
    embed_base64(post_dir)
