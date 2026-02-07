import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

# Import our new Renderer
try:
    from . import social_renderer as renderer_module
    SocialRenderer = renderer_module.SocialRenderer
except ImportError:
    # Handle direct execution
    import importlib.util
    spec = importlib.util.spec_from_file_location("SocialRenderer", str(Path(__file__).parent / "03_social_renderer.py"))
    social_renderer_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(social_renderer_mod)
    SocialRenderer = social_renderer_mod.SocialRenderer

def get_frontmatter(content):
    """Extracts basic frontmatter from MDX content."""
    frontmatter = {}
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        # Simple parsing for title, description, and image
        title_match = re.search(r'title:\s*"(.*?)"', yaml_content)
        if title_match:
            frontmatter['title'] = title_match.group(1)
        desc_match = re.search(r'description:\s*"(.*?)"', yaml_content)
        if desc_match:
            frontmatter['description'] = desc_match.group(1)
        image_match = re.search(r'image:\s*"(.*?)"', yaml_content)
        if image_match:
            frontmatter['image'] = image_match.group(1)
    return frontmatter

def get_social_data(post_dir):
    """Reads social.json if available."""
    social_path = Path(post_dir) / "social.json"
    if social_path.exists():
        try:
            with open(social_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not read social.json: {e}")
    return None

def get_post_images(post_dir, content, hero_image_path=None):
    """Finds all valid images referenced in MDX and post directory, preserving order."""
    images = []
    project_root = Path(os.getcwd())
    public_dir = project_root / "public"

    if hero_image_path and hero_image_path.exists():
        images.append(hero_image_path)

    matches = re.findall(r'src=["\'](\/[^"\']+)["\']|!\[.*?\]\((\/[^)\s]+)\)', content)
    for match in matches:
        path_str = match[0] if match[0] else match[1]
        if not path_str: continue
        clean_path = path_str.lstrip('/')
        full_path = public_dir / clean_path
        if full_path.exists() and full_path.is_file():
             images.append(full_path)

    if len(images) <= 1:
        extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        for item in post_dir.iterdir():
            if item.is_file() and item.suffix.lower() in extensions:
                 if "story-" in item.name or "feed-" in item.name: continue
                 is_duplicate = False
                 for added_img in images:
                     if item.resolve() == added_img.resolve():
                         is_duplicate = True
                         break
                 if not is_duplicate:
                     images.append(item)

    unique_images = []
    seen = set()
    for img in images:
        resolved = str(img.resolve())
        if resolved not in seen:
            unique_images.append(img)
            seen.add(resolved)
    return unique_images

def generate_assets(post_dir):
    renderer = SocialRenderer()
    post_path = Path(post_dir)
    mdx_path = post_path / "index.mdx"
    output_dir = post_path / "social-media"
    output_dir.mkdir(exist_ok=True)
    print(f"📂 Output Folder: {output_dir}")

    if not mdx_path.exists():
        print(f"❌ No index.mdx found in {post_dir}")
        return

    print(f"📖 Reading {mdx_path}...")
    with open(mdx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    meta = get_frontmatter(content)
    social_data = get_social_data(post_path)

    # Hero Image Logic
    image_rel_path = meta.get('image', '').replace('../../', '')
    project_root = Path(os.getcwd())
    possible_paths = [project_root / image_rel_path, post_path / image_rel_path, post_path / "image.jpg", post_path / "hero.jpg"]
    hero_image_path = None
    for p in possible_paths:
        if p.exists() and p.is_file():
            hero_image_path = p
            break

    available_images = get_post_images(post_path, content, hero_image_path)
    if not available_images:
        print("❌ No images found.")
        return

    # Generate Timestamp Prefix
    timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
    print(f"🕒 Timestamp for assets: {timestamp_str}")

    STORY_SIZE = (1080, 1920)
    FEED_SIZE = (1080, 1350)
    margin = 80

    # --- 1. Feed Posts ---
    if hero_image_path:
        bg_img_base = renderer.create_base_image(hero_image_path, FEED_SIZE, blur=False)
        items = []
        if meta.get('title'):
            items.append({'name': 'feed-post-1-title', 'text': meta['title'], 'font': renderer.fonts['title'], 'max_width': 20})

        summary_short = ""
        if social_data and 'promotion' in social_data:
            summary_short = social_data['promotion'].get('summary_short', '')
        if not summary_short and meta.get('description'):
            summary_short = meta['description']
        if summary_short:
            items.append({'name': 'feed-post-2-summary-short', 'text': summary_short, 'font': renderer.fonts['body'], 'max_width': 30})

        for item in items:
            img = bg_img_base.copy()
            draw = ImageDraw.Draw(img)
            text_height = renderer.measure_text_height(item['text'], item['font'], item['max_width'])
            box_height = text_height + 120 # padding * 2
            box_width = FEED_SIZE[0] - (margin * 2)
            box_x = margin
            box_y = max(100, (FEED_SIZE[1] - box_height) / 2)
            box_coords = (box_x, box_y, box_x + box_width, box_y + box_height)

            glass = renderer.create_glass_effect(img, box_coords)
            img.paste(glass, (int(box_x), int(box_y)))
            draw.rectangle(box_coords, outline=(255,255,255,80), width=4)
            renderer.draw_text_clean(draw, item['text'], (box_x + 40, box_y + 60), item['font'], item['max_width'], image=img)

            # Apply Timestamp
            output_path = output_dir / f"{timestamp_str}-{item['name']}.jpg"
            img.convert("RGB").save(output_path, "JPEG", quality=95)
            print(f"✅ Created Feed Post: {output_path}")

    # --- 2. Story Cover ---
    current_img_idx = 0
    base_img = renderer.create_base_image(available_images[current_img_idx], STORY_SIZE, blur=False)
    draw = ImageDraw.Draw(base_img)
    title = meta.get('title', '')
    desc = meta.get('description', '')

    title_height = renderer.measure_text_height(title, renderer.fonts['title'], 20)
    desc_height = renderer.measure_text_height(desc, renderer.fonts['body'], 35)
    total_text_height = title_height + 40 + desc_height
    box_height = total_text_height + 120
    box_width = STORY_SIZE[0] - (margin * 2)
    box_x = margin
    box_y = max(100, (STORY_SIZE[1] - box_height) / 2)
    box_coords = (box_x, box_y, box_x + box_width, box_y + box_height)

    glass_patch = renderer.create_glass_effect(base_img, box_coords)
    base_img.paste(glass_patch, (int(box_x), int(box_y)))
    draw.rectangle(box_coords, outline=(255,255,255,80), width=4)

    current_y = box_y + 60
    current_y = renderer.draw_text_clean(draw, title, (box_x + 40, current_y), renderer.fonts['title'], 20, image=base_img)
    current_y += 40
    renderer.draw_text_clean(draw, desc, (box_x + 40, current_y), renderer.fonts['body'], 35, image=base_img)
    draw.text((margin, 1700), "🔗 Link na Bio", font=renderer.fonts['footer'], fill=(255,255,255,255))

    output_path = output_dir / f"{timestamp_str}-story-cover.jpg"
    base_img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Created Story Cover (Glass): {output_path}")

    # --- 3. Tweet Stories ---
    if social_data and 'promotion' in social_data and 'twitter_thread' in social_data['promotion']:
        tweets = social_data['promotion']['twitter_thread']
        for i, tweet in enumerate(tweets):
            current_img_idx = (current_img_idx + 1) % len(available_images)
            bg_path = available_images[current_img_idx]
            img_tweet = renderer.create_base_image(bg_path, STORY_SIZE, blur=False)
            draw_t = ImageDraw.Draw(img_tweet)
            tweet_height = renderer.measure_text_height(tweet, renderer.fonts['body'], 30)
            box_height = tweet_height + 120
            box_width = STORY_SIZE[0] - (margin * 2)
            box_x = margin
            box_y = max(100, (STORY_SIZE[1] - box_height) / 2)
            box_coords = (box_x, box_y, box_x + box_width, box_y + box_height)

            glass = renderer.create_glass_effect(img_tweet, box_coords)
            img_tweet.paste(glass, (int(box_x), int(box_y)))
            draw_t.rectangle(box_coords, outline=(255,255,255,80), width=4)
            draw_t.text((margin, box_y - 60), f"Part {i+1}/{len(tweets)}", font=renderer.fonts['meta'], fill=(220,220,220,255))
            renderer.draw_text_clean(draw_t, tweet, (box_x + 40, box_y + 60), renderer.fonts['body'], 30, image=img_tweet)

            if i == len(tweets) - 1:
                 draw_t.text((margin, 1700), "🔗 Link na Bio", font=renderer.fonts['footer'], fill=(255,255,255,255))
            else:
                 draw_t.text((margin, 1700), "👉 Próximo", font=renderer.fonts['footer'], fill=(255,255,255,200))

            output_tweet_path = output_dir / f"{timestamp_str}-story-tweet-{i+1}.jpg"
            img_tweet.convert("RGB").save(output_tweet_path, "JPEG", quality=95)
            print(f"   - Created: {output_tweet_path} (Img: {bg_path.name})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]
    generate_assets(target_dir)
