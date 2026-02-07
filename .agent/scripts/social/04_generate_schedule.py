import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

# Path to models directory
MODELS_DIR = Path(__file__).parent / "models"

def load_model(model_name):
    """Load a model template from the models directory."""
    model_path = MODELS_DIR / model_name
    if model_path.exists():
        with open(model_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_env_file(filepath):
    """Simple .env file parser to avoid external dependencies."""
    env_vars = {}
    if not os.path.exists(filepath):
        return env_vars

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                # Remove quotes if present
                value = value.strip().strip("'").strip('"')
                env_vars[key.strip()] = value
    # print(f"Loaded keys from {filepath}: {list(env_vars.keys())}") # Debug
    return env_vars

def get_env_vars():
    """Load env vars from .env and .env.local, favoring .env.local."""
    project_root = Path(os.getcwd())
    env_vars = {}

    # Load .env first
    env_vars.update(load_env_file(project_root / '.env'))

    # Load .env.local (overrides)
    env_vars.update(load_env_file(project_root / '.env.local'))

    return env_vars

def parse_mdx_frontmatter(mdx_path):
    """Parses MDX frontmatter to extract publishedAt date."""
    published_at = None
    try:
        with open(mdx_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'publishedAt:\s*["\']?(\d{4}-\d{2}-\d{2})["\']?', content)
            if match:
                published_at = match.group(1)
    except Exception as e:
        print(f"Error reading MDX: {e}")
    return published_at

def get_social_data(post_dir):
    """Reads social.json."""
    social_path = Path(post_dir) / "social.json"
    if social_path.exists():
        try:
            with open(social_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading social.json: {e}")
    return {}

def find_images(post_dir):
    """Finds generated social media images."""
    social_media_dir = Path(post_dir) / "social-media"
    images = {
        "story_cover": None,
        "story_tweets": [],
        "feed_title": None,
        "feed_summary": None
    }

    if not social_media_dir.exists():
        return images

    # Helper to find latest file by pattern
    def find_latest(pattern):
        files = list(social_media_dir.glob(pattern))
        if not files: return None
        # Sort by name (which acts as sort by timestamp due to prefix)
        files.sort(key=lambda x: x.name, reverse=True)
        return str(files[0].absolute())

    # Find Story Cover
    images["story_cover"] = find_latest("*story-cover.jpg")

    # Determine Active Timestamp from found assets
    latest_timestamp = None
    ref_file = images["story_cover"] or images["feed_title"]
    if ref_file:
        # Expected format: YYYYMMDDHHMMSS-name.jpg
        # We can extract the first 14 chars of the filename
        fname = Path(ref_file).name
        if len(fname) > 14 and fname[:14].isdigit():
            latest_timestamp = fname[:14]

    # Find Story Tweets
    if latest_timestamp:
        # Strict matching if we found a timestamp
        tweets = sorted(list(social_media_dir.glob(f"{latest_timestamp}-story-tweet-*.jpg")))
    else:
        # Fallback to finding all and hoping for the best (or taking the latest batch if clean)
        # Better fallback: Group by timestamp and take latest group?
        # For now, let's just take all if no timestamp found (unlikely if 03 ran)
        tweets = sorted(list(social_media_dir.glob("*story-tweet-*.jpg")))
        # If we have multiple timestamps, this is risky.
        # Let's try to infer timestamp from the tweets themselves if ref_file was missing
        if tweets and not latest_timestamp:
             # Extract timestamps
             timestamps = set()
             for t in tweets:
                 if len(t.name) > 14 and t.name[:14].isdigit():
                     timestamps.add(t.name[:14])
             if timestamps:
                 latest = sorted(list(timestamps))[-1]
                 tweets = sorted(list(social_media_dir.glob(f"{latest}-story-tweet-*.jpg")))

    images["story_tweets"] = [str(t.absolute()) for t in tweets]

    # Find Feed Posts
    images["feed_title"] = find_latest("*feed-post-1-title.jpg")
    images["feed_summary"] = find_latest("*feed-post-2-summary-short.jpg")

    return images

def linen_text_format(text):
    """Formats text for social media (basic HTML p tags if required by tool)."""
    if not text: return ""

    formatted = ""
    for line in text.split('\n'):
        if line.strip():
            formatted += f"<p>{line.strip()}</p>"
    return formatted

def convert_to_image_format(attachments):
    """Converts attachment paths to Facebook image format with id and path."""
    images = []
    for i, path in enumerate(attachments):
        if path:
            # Generate a simple id based on index and filename
            filename = Path(path).stem
            image_id = f"img-{filename[:20]}"
            images.append({
                "id": image_id,
                "path": path
            })
    return images

def generate_schedule(post_dir):
    target_dir = Path(post_dir)
    mdx_path = target_dir / "index.mdx"

    if not mdx_path.exists():
        print(f"❌ Error: index.mdx not found in {target_dir}")
        return

    # Extract post slug from directory name
    post_slug = target_dir.name
    site_url = "https://www.eltonjose.com.br"
    post_url = f"{site_url}/blogs/{post_slug}"

    # Load Env Vars
    env_vars = get_env_vars()
    linkedin_id = env_vars.get('POSTIZ_LINKEDIN_ID')
    instagram_id = env_vars.get('POSTIZ_INSTAGRAM_ID')
    facebook_id = env_vars.get('POSTIZ_FACEBOOK_ID')

    if not any([linkedin_id, instagram_id, facebook_id]):
        print("⚠️ Warning: No POSTIZ_* IDs found in .env or .env.local")

    # 1. Get Date
    date_str = parse_mdx_frontmatter(mdx_path)
    if not date_str:
        print("⚠️ Warning: Could not find 'publishedAt' in MDX. Using tomorrow's date.")
        date_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"📅 Published Date: {date_str}")

    # 2. Get Content
    social_data = get_social_data(target_dir)
    summary_prof = social_data.get('promotion', {}).get('summary_professional', '')

    linkedin_text = summary_prof
    feed_text = summary_prof

    # 3. Get Images
    images = find_images(target_dir)

    # 4. Construct Schedule using Models as templates
    schedule = []

    # --- LinkedIn (10:00 AM) ---
    if linkedin_id:
        linkedin_attachments = []
        if images['feed_title']: linkedin_attachments.append(images['feed_title'])
        if images['feed_summary']: linkedin_attachments.append(images['feed_summary'])

        if linkedin_attachments and linkedin_text:
            # Load LinkedIn model template
            linkedin_model = load_model("linkedin-post.json")
            if linkedin_model:
                linkedin_post = linkedin_model.copy()
                linkedin_post["type"] = "schedule"
                linkedin_post["date"] = f"{date_str}T10:00:00Z"
                linkedin_post["posts"][0]["integration"]["id"] = linkedin_id
                linkedin_post["posts"][0]["value"][0]["content"] = linen_text_format(linkedin_text)
                # Map attachments to model image format
                model_images = []
                for i, path in enumerate(linkedin_attachments):
                    model_images.append({
                        "id": f"img-linkedin-{i}",
                        "path": path
                    })
                linkedin_post["posts"][0]["value"][0]["image"] = model_images
                schedule.append(linkedin_post)
                print("✅ Added LinkedIn schedule (using model template)")
            else:
                # Fallback to old format if model not found
                schedule.append({
                    "integrationId": linkedin_id,
                    "type": "schedule",
                    "date": f"{date_str}T10:00:00Z",
                    "postsAndComments": [
                        {
                            "content": linen_text_format(linkedin_text),
                            "attachments": linkedin_attachments
                        }
                    ],
                    "settings": []
                })
                print("✅ Added LinkedIn schedule (fallback format)")
        else:
            print("⚠️ Skipping LinkedIn: Missing text or feed images.")
    else:
        print("ℹ️ Skipping LinkedIn: POSTIZ_LINKEDIN_ID not set.")

    # --- Instagram Stories (09:00 AM) ---
    story_attachments = []
    if images['story_cover']: story_attachments.append(images['story_cover'])
    story_attachments.extend(images['story_tweets'])

    if story_attachments:
        if instagram_id:
            # Load Instagram Story model template
            story_model = load_model("instagram-story.json")
            if story_model:
                story_post = story_model.copy()
                story_post["type"] = "schedule"
                story_post["date"] = f"{date_str}T09:00:00Z"
                story_post["posts"][0]["integration"]["id"] = instagram_id
                # Map attachments to model image format
                model_images = []
                for i, path in enumerate(story_attachments):
                    model_images.append({
                        "id": f"img-story-{i}",
                        "path": path
                    })
                story_post["posts"][0]["value"][0]["image"] = model_images
                schedule.append(story_post)
                print("✅ Added Instagram Story schedule (using model template)")
            else:
                # Fallback to old format
                schedule.append({
                    "integrationId": instagram_id,
                    "type": "schedule",
                    "date": f"{date_str}T09:00:00Z",
                    "postsAndComments": [
                        {
                            "content": "Novo post! Veja o link na bio.",
                            "attachments": story_attachments
                        }
                    ],
                    "settings": [{"key": "media_type", "value": "story"}]
                })
                print("✅ Added Instagram Story schedule (fallback format)")
        else:
            print("ℹ️ Skipping Instagram Story: POSTIZ_INSTAGRAM_ID not set.")
    else:
        print("⚠️ Skipping Stories: Missing story images.")

    # --- Instagram/Facebook Feed (22:00 PM same day) ---
    feed_attachments = []
    if images['feed_title']: feed_attachments.append(images['feed_title'])
    if images['feed_summary']: feed_attachments.append(images['feed_summary'])

    if feed_attachments and feed_text:
        # Instagram Feed
        if instagram_id:
            ig_model = load_model("instagram-post.json")
            if ig_model:
                ig_post = ig_model.copy()
                ig_post["type"] = "schedule"
                ig_post["date"] = f"{date_str}T22:00:00Z"
                ig_post["posts"][0]["integration"]["id"] = instagram_id
                ig_post["posts"][0]["value"][0]["content"] = linen_text_format(feed_text)
                # Map attachments to model image format
                model_images = []
                for i, path in enumerate(feed_attachments):
                    model_images.append({
                        "id": f"img-ig-feed-{i}",
                        "path": path
                    })
                ig_post["posts"][0]["value"][0]["image"] = model_images
                schedule.append(ig_post)
                print("✅ Added Instagram Feed schedule (using model template)")
            else:
                # Fallback to old format
                ig_feed_images = convert_to_image_format(feed_attachments)
                schedule.append({
                    "integrationId": instagram_id,
                    "type": "schedule",
                    "date": f"{date_str}T22:00:00Z",
                    "postsAndComments": [
                        {
                            "content": linen_text_format(feed_text),
                            "image": ig_feed_images
                        }
                    ],
                    "settings": []
                })
                print("✅ Added Instagram Feed schedule (fallback format)")

        # Facebook Feed
        if facebook_id:
            fb_model = load_model("facebook-json.json")
            if fb_model:
                fb_post = fb_model.copy()
                fb_post["type"] = "schedule"
                fb_post["date"] = f"{date_str}T22:00:00Z"
                fb_post["posts"][0]["integration"]["id"] = facebook_id
                fb_post["posts"][0]["value"][0]["content"] = linen_text_format(feed_text)
                # Map attachments to model image format
                model_images = []
                for i, path in enumerate(feed_attachments):
                    model_images.append({
                        "id": f"img-fb-feed-{i}",
                        "path": path
                    })
                fb_post["posts"][0]["value"][0]["image"] = model_images
                fb_post["posts"][0]["settings"]["url"] = post_url
                schedule.append(fb_post)
                print("✅ Added Facebook Feed schedule (using model template)")
            else:
                # Fallback to old format
                fb_feed_images = convert_to_image_format(feed_attachments)
                schedule.append({
                    "integrationId": facebook_id,
                    "type": "schedule",
                    "date": f"{date_str}T22:00:00Z",
                    "postsAndComments": [
                        {
                            "content": linen_text_format(feed_text),
                            "image": fb_feed_images
                        }
                    ],
                    "settings": {
                        "__type": "facebook",
                        "url": post_url
                    }
                })
                print("✅ Added Facebook Feed schedule (fallback format)")

    # 5. Output
    output_path = target_dir / "social_schedule.json"
    if schedule:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(schedule, f, indent=2, ensure_ascii=False)
        print(f"✅ Generated Schedule: {output_path}")
    else:
        print("⚠️ No schedule generated (check IDs or missing content).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_schedule.py <post_directory>")
        sys.exit(1)

    post_dir = sys.argv[1]
    if post_dir.endswith("/"): post_dir = post_dir[:-1]
    generate_schedule(post_dir)
