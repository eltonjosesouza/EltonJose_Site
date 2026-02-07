import os
import sys
import re
import json
from pathlib import Path
import textwrap

# Try importing Pillow
try:
    from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    print("❌ Error: 'Pillow' library is not installed.")
    print("👉 Please run: pip install Pillow")
    sys.exit(1)

# Try importing Pilmoji
try:
    from pilmoji import Pilmoji
    HAS_PILMOJI = True
except ImportError:
    HAS_PILMOJI = False
    print("⚠️ 'pilmoji' not found. Emojis may not render correctly.")
    print("👉 Run: pip install pilmoji")

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

    # 1. Add Hero Image first (if valid)
    if hero_image_path and hero_image_path.exists():
        images.append(hero_image_path)

    # 2. Parse MDX for <Image src="..." /> and standard markdown ![]()
    matches = re.findall(r'src=["\'](\/[^"\']+)["\']|!\[.*?\]\((\/[^)\s]+)\)', content)

    for match in matches:
        path_str = match[0] if match[0] else match[1]
        if not path_str:
            continue
        clean_path = path_str.lstrip('/')
        full_path = public_dir / clean_path
        if full_path.exists() and full_path.is_file():
             images.append(full_path)
        else:
            print(f"⚠️ Referenced image not found: {full_path}")

    # 3. Fallback: Scan directory (only if we have very few images)
    if len(images) <= 1:
        extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        for item in post_dir.iterdir():
            if item.is_file() and item.suffix.lower() in extensions:
                 if "story-" in item.name: continue
                 if "feed-" in item.name: continue
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

def create_base_image(source_image_path, size, blur=False):
    """Creates the background base image. default is sharp (no blur)."""
    img = Image.open(source_image_path).convert("RGBA")

    img_ratio = img.width / img.height
    target_ratio = size[0] / size[1]

    if img_ratio > target_ratio:
        new_height = size[1]
        new_width = int(new_height * img_ratio)
    else:
        new_width = size[0]
        new_height = int(new_width / img_ratio)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    left = (new_width - size[0]) / 2
    top = (new_height - size[1]) / 2
    right = (new_width + size[0]) / 2
    bottom = (new_height + size[1]) / 2

    img = img.crop((left, top, right, bottom))

    if blur:
        print(f"💧 Applying global blur to {source_image_path.name}...")
        img = img.filter(ImageFilter.GaussianBlur(15))
        overlay = Image.new('RGBA', size, (0, 0, 0, 120))
        img = Image.alpha_composite(img, overlay)

    return img

def create_glass_effect(bg_image, box_coords, blur_radius=30, opacity=140):
    """Applies a glassmorphism effect to a region."""
    box_coords = tuple(map(int, box_coords))

    width, height = bg_image.size
    box_coords = (
        max(0, box_coords[0]),
        max(0, box_coords[1]),
        min(width, box_coords[2]),
        min(height, box_coords[3])
    )

    crop = bg_image.crop(box_coords)
    crop = crop.filter(ImageFilter.GaussianBlur(blur_radius))

    overlay = Image.new('RGBA', crop.size, (0, 0, 0, opacity))
    crop = Image.alpha_composite(crop, overlay)

    return crop

def measure_text_height(text, font, max_width):
    """Calculates the total height of wrapped text."""
    if not text:
        return 0

    wrapper = textwrap.TextWrapper(width=max_width)
    lines = []
    for paragraph in text.split('\n'):
        lines.extend(wrapper.wrap(paragraph) if paragraph.strip() else [])

    if not lines:
        return 0

    bbox = font.getbbox("Ay")
    line_height = (bbox[3] - bbox[1]) + 20
    return len(lines) * line_height

def draw_text_clean(draw, text, start_pos, font, max_width, fill=(255,255,255,255), image=None):
    """Draws text without shadow (Clean look), returns new y. Uses Pilmoji if available."""
    x, y = start_pos
    wrapper = textwrap.TextWrapper(width=max_width)

    current_y = y

    # Setup Pilmoji if enabled
    pm = None
    if HAS_PILMOJI and image:
        pm = Pilmoji(image)

    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        if not paragraph.strip():
            bbox = draw.textbbox((0, 0), "A", font=font)
            current_y += (bbox[3] - bbox[1]) + 20
            continue

        lines = wrapper.wrap(paragraph)
        for line in lines:
            if pm:
                pm.text((int(x), int(current_y)), line, font=font, fill=fill)
            else:
                draw.text((x, current_y), line, font=font, fill=fill)

            bbox = draw.textbbox((x, current_y), line, font=font)
            line_height = (bbox[3] - bbox[1]) + 20
            current_y += line_height

    return current_y

def create_feed_post_batch(post_dir, output_dir, meta, hero_image_path, fonts):
    """Generates 3 feed posts (1080x1350) for LinkedIn/IG/FB: Title, Description, Hook."""
    FEED_SIZE = (1080, 1350)

    if not hero_image_path or not hero_image_path.exists():
        print("⚠️ No hero image available for feed post. Skipping.")
        return

    # 1. Base Image (Sharp)
    bg_img_base = create_base_image(hero_image_path, FEED_SIZE, blur=False)

    # Define Content Items
    items = []

    # Item 1: Title
    if meta.get('title'):
        items.append({
            'name': 'feed-post-1-title',
            'text': meta['title'],
            'font': fonts['title'],
            'max_width': 20
        })

    # Item 2: Summary Short (from social.json or MDX description)
    social_data = get_social_data(post_dir)
    summary_short = ""
    if social_data and 'promotion' in social_data:
        summary_short = social_data['promotion'].get('summary_short', '')

    if not summary_short and meta.get('description'):
        summary_short = meta['description']

    if summary_short:
        items.append({
            'name': 'feed-post-2-summary-short',
            'text': summary_short,
            'font': fonts['body'],
            'max_width': 30
        })

    # Item 3: Summary Professional (from social.json)
    summary_prof = ""
    if social_data and 'promotion' in social_data:
        summary_prof = social_data['promotion'].get('summary_professional', '')
        # Take just the first 2-3 paragraphs to fit
        if summary_prof:
             paragraphs = summary_prof.split('\n\n')
             summary_prof = "\n\n".join(paragraphs[:2]) # Limit text length

    if summary_prof:
        items.append({
            'name': 'feed-post-3-summary-prof',
            'text': summary_prof,
            'font': fonts['body'], # Maybe slightly smaller if text is long? Keep body for now
            'max_width': 35
        })

    # Generate Each
    margin = 80
    box_padding_vertical = 60

    for item in items:
        # Clone base
        img = bg_img_base.copy()
        draw = ImageDraw.Draw(img)

        text = item['text']
        font = item['font']
        max_width = item['max_width']

        text_height = measure_text_height(text, font, max_width)
        box_height = text_height + (box_padding_vertical * 2)
        box_width = FEED_SIZE[0] - (margin * 2)

        box_x = margin
        box_y = (FEED_SIZE[1] - box_height) / 2

        # Ensure box stays within vertical bounds + margin
        if box_y < 100: box_y = 100

        box_coords = (box_x, box_y, box_x + box_width, box_y + box_height)

        glass = create_glass_effect(img, box_coords)
        img.paste(glass, (int(box_x), int(box_y)))
        draw.rectangle(box_coords, outline=(255,255,255,80), width=4)

        draw_text_clean(draw, text, (box_x + 40, box_y + box_padding_vertical), font, max_width, image=img)

        output_path = output_dir / f"{item['name']}.jpg"
        img.convert("RGB").save(output_path, "JPEG", quality=95)
        print(f"✅ Created Feed Post: {output_path}")

def get_fonts():
    """Load fonts safely."""
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"

    try:
        fonts = {
            'title': ImageFont.truetype(font_path, 80),
            'body': ImageFont.truetype(font_path, 45),
            'footer': ImageFont.truetype(font_path, 30),
            'meta': ImageFont.truetype(font_path, 25)
        }
    except IOError:
        print("⚠️  Custom font not found, using default.")
        d = ImageFont.load_default()
        fonts = {'title': d, 'body': d, 'footer': d, 'meta': d}
    return fonts

def create_story(post_dir):
    post_path = Path(post_dir)
    mdx_path = post_path / "index.mdx"

    # Create social-media output directory
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

    image_rel_path = meta.get('image', '').replace('../../', '')
    project_root = Path(os.getcwd())

    possible_paths = [
        project_root / image_rel_path,
        post_path / image_rel_path,
        post_path / "image.jpg",
        post_path / "hero.jpg"
    ]

    hero_image_path = None
    for p in possible_paths:
        if p.exists() and p.is_file():
            hero_image_path = p
            break

    available_images = get_post_images(post_path, content, hero_image_path)
    if not available_images:
        print("❌ No images found.")
        return

    STORY_SIZE = (1080, 1920)
    fonts = get_fonts()
    margin = 80

    # --- 1. Feed Posts (Batch: Title, Summary, Hook) ---
    create_feed_post_batch(post_dir, output_dir, meta, hero_image_path, fonts)

    # --- 2. Story Cover (Glassmorphism) ---
    current_img_idx = 0
    base_img = create_base_image(available_images[current_img_idx], STORY_SIZE, blur=False)
    draw = ImageDraw.Draw(base_img)

    title = meta.get('title', '')
    desc = meta.get('description', '')

    title_height = measure_text_height(title, fonts['title'], max_width=20)
    desc_height = measure_text_height(desc, fonts['body'], max_width=35)

    padding = 60
    gap = 40
    total_text_height = title_height + gap + desc_height
    box_height = total_text_height + (padding * 2)
    box_width = STORY_SIZE[0] - (margin * 2)

    box_x = margin
    box_y = (STORY_SIZE[1] - box_height) / 2
    if box_y < 100: box_y = 100

    box_coords = (box_x, box_y, box_x + box_width, box_y + box_height)

    glass_patch = create_glass_effect(base_img, box_coords)
    base_img.paste(glass_patch, (int(box_x), int(box_y)))
    draw.rectangle(box_coords, outline=(255,255,255,80), width=4)

    current_y = box_y + padding
    current_y = draw_text_clean(draw, title, (box_x + 40, current_y), fonts['title'], max_width=20, image=base_img)
    current_y += gap
    draw_text_clean(draw, desc, (box_x + 40, current_y), fonts['body'], max_width=35, image=base_img)

    draw.text((margin, 1700), "🔗 Link na Bio", font=fonts['footer'], fill=(255,255,255,255))

    output_path = output_dir / "story-cover.jpg"
    base_img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Created Story Cover (Glass): {output_path}")

    # --- 3. Tweet Stories (Glassmorphism) ---
    if social_data and 'promotion' in social_data and 'twitter_thread' in social_data['promotion']:
        tweets = social_data['promotion']['twitter_thread']

        for i, tweet in enumerate(tweets):
            current_img_idx = (current_img_idx + 1) % len(available_images)
            bg_path = available_images[current_img_idx]

            img_tweet = create_base_image(bg_path, STORY_SIZE, blur=False)
            draw_t = ImageDraw.Draw(img_tweet)

            tweet_height = measure_text_height(tweet, fonts['body'], max_width=30)
            box_height = tweet_height + (padding * 2)

            box_width = STORY_SIZE[0] - (margin * 2)
            box_x = margin
            box_y = (STORY_SIZE[1] - box_height) / 2
            if box_y < 100: box_y = 100

            box_coords = (box_x, box_y, box_x + box_width, box_y + box_height)

            glass = create_glass_effect(img_tweet, box_coords)
            img_tweet.paste(glass, (int(box_x), int(box_y)))
            draw_t.rectangle(box_coords, outline=(255,255,255,80), width=4)

            draw_t.text((margin, box_y - 60), f"Part {i+1}/{len(tweets)}", font=fonts['meta'], fill=(220,220,220,255))

            draw_text_clean(draw_t, tweet, (box_x + 40, box_y + padding), fonts['body'], max_width=30, image=img_tweet)

            if i == len(tweets) - 1:
                 draw_t.text((margin, 1700), "🔗 Link na Bio", font=fonts['footer'], fill=(255,255,255,255))
            else:
                 draw_t.text((margin, 1700), "👉 Próximo", font=fonts['footer'], fill=(255,255,255,200))

            output_tweet_path = output_dir / f"story-tweet-{i+1}.jpg"
            img_tweet.convert("RGB").save(output_tweet_path, "JPEG", quality=95)
            print(f"   - Created: {output_tweet_path} (Img: {bg_path.name})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    create_story(target_dir)
