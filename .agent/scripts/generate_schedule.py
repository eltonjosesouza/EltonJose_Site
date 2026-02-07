import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

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

    # Find Story Cover
    cover = social_media_dir / "story-cover.jpg"
    if cover.exists():
        images["story_cover"] = str(cover.absolute())

    # Find Story Tweets (sorted)
    tweets = sorted(list(social_media_dir.glob("story-tweet-*.jpg")))
    images["story_tweets"] = [str(t.absolute()) for t in tweets]

    # Find Feed Posts
    feed_title = social_media_dir / "feed-post-1-title.jpg"
    if feed_title.exists():
        images["feed_title"] = str(feed_title.absolute())

    feed_summary = social_media_dir / "feed-post-2-summary-short.jpg"
    if feed_summary.exists():
        images["feed_summary"] = str(feed_summary.absolute())

    return images

def linen_text_format(text):
    """Formats text for social media (basic HTML p tags if required by tool)."""
    if not text: return ""

    formatted = ""
    for line in text.split('\n'):
        if line.strip():
            formatted += f"<p>{line.strip()}</p>"
    return formatted

def generate_schedule(post_dir):
    target_dir = Path(post_dir)
    mdx_path = target_dir / "index.mdx"

    if not mdx_path.exists():
        print(f"❌ Error: index.mdx not found in {target_dir}")
        return

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

    # 4. Construct Schedule
    schedule = []

    # --- LinkedIn (10:00 AM) ---
    if linkedin_id:
        linkedin_attachments = []
        if images['feed_title']: linkedin_attachments.append(images['feed_title'])
        if images['feed_summary']: linkedin_attachments.append(images['feed_summary'])

        if linkedin_attachments and linkedin_text:
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
            print("✅ Added LinkedIn schedule")
        else:
            print("⚠️ Skipping LinkedIn: Missing text or feed images.")
    else:
        print("ℹ️ Skipping LinkedIn: POSTIZ_LINKEDIN_ID not set.")

    # --- Instagram Stories (09:00 AM) ---
    story_attachments = []
    if images['story_cover']: story_attachments.append(images['story_cover'])
    story_attachments.extend(images['story_tweets'])

    if story_attachments:
        # Instagram Stories
        if instagram_id:
            schedule.append({
                "integrationId": instagram_id,
                "type": "schedule",
                "date": f"{date_str}T09:00:00Z",
                "postsAndComments": [
                    {
                        "content": "New Post! Check connection in bio.",
                        "attachments": story_attachments
                    }
                ],
                "settings": [{"key": "media_type", "value": "STORY"}]
            })
            print("✅ Added Instagram Story schedule")
        else:
            print("ℹ️ Skipping Instagram Story: POSTIZ_INSTAGRAM_ID not set.")

        # Facebook Stories
        if facebook_id:
            schedule.append({
                "integrationId": facebook_id,
                "type": "schedule",
                "date": f"{date_str}T09:00:00Z",
                 "postsAndComments": [
                    {
                        "content": "New Post!",
                        "attachments": story_attachments
                    }
                ],
                "settings": [{"key": "media_type", "value": "STORY"}]
            })
            print("✅ Added Facebook Story schedule")
        else:
            print("ℹ️ Skipping Facebook Story: POSTIZ_FACEBOOK_ID not set.")
    else:
        print("⚠️ Skipping Stories: Missing story images.")

    # --- Instagram/Facebook Feed (22:00 PM same day) ---
    feed_attachments = []
    if images['feed_title']: feed_attachments.append(images['feed_title'])
    if images['feed_summary']: feed_attachments.append(images['feed_summary'])

    if feed_attachments and feed_text:
        # Instagram Feed
        if instagram_id:
            schedule.append({
                "integrationId": instagram_id,
                "type": "schedule",
                "date": f"{date_str}T22:00:00Z",
                "postsAndComments": [
                    {
                        "content": linen_text_format(feed_text),
                        "attachments": feed_attachments
                    }
                ],
                 "settings": []
            })
            print("✅ Added Instagram Feed schedule")

        # Facebook Feed
        if facebook_id:
            schedule.append({
                "integrationId": facebook_id,
                "type": "schedule",
                "date": f"{date_str}T22:00:00Z",
                 "postsAndComments": [
                    {
                        "content": linen_text_format(feed_text),
                        "attachments": feed_attachments
                    }
                ],
                 "settings": []
            })
            print("✅ Added Facebook Feed schedule")

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
