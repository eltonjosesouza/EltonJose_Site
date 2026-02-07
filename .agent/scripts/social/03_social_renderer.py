import os
import sys
import textwrap
try:
    from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    print("❌ Error: 'Pillow' library is not installed.")
    sys.exit(1)

try:
    from pilmoji import Pilmoji
    HAS_PILMOJI = True
except ImportError:
    HAS_PILMOJI = False

class SocialRenderer:
    def __init__(self):
        self.fonts = self._load_fonts()

    def _load_fonts(self):
        """Load fonts safely."""
        font_path = "/System/Library/Fonts/Helvetica.ttc"
        if not os.path.exists(font_path):
            font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"

        try:
            return {
                'title': ImageFont.truetype(font_path, 80),
                'body': ImageFont.truetype(font_path, 45),
                'footer': ImageFont.truetype(font_path, 30),
                'meta': ImageFont.truetype(font_path, 25)
            }
        except IOError:
            print("⚠️  Custom font not found, using default.")
            d = ImageFont.load_default()
            return {'title': d, 'body': d, 'footer': d, 'meta': d}

    def measure_text_height(self, text, font, max_width):
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

    def draw_text_clean(self, draw, text, start_pos, font, max_width, fill=(255,255,255,255), image=None):
        """Draws text without shadow (Clean look), returns new y. Uses Pilmoji if available."""
        x, y = start_pos
        wrapper = textwrap.TextWrapper(width=max_width)
        current_y = y
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

    def create_base_image(self, source_image_path, size, blur=False):
        """Creates the background base image."""
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
            img = img.filter(ImageFilter.GaussianBlur(15))
            overlay = Image.new('RGBA', size, (0, 0, 0, 120))
            img = Image.alpha_composite(img, overlay)
        return img

    def create_glass_effect(self, bg_image, box_coords, blur_radius=30, opacity=140):
        """Applies a glassmorphism effect to a region."""
        box_coords = tuple(map(int, box_coords))
        width, height = bg_image.size
        box_coords = (
            max(0, box_coords[0]), max(0, box_coords[1]),
            min(width, box_coords[2]), min(height, box_coords[3])
        )
        crop = bg_image.crop(box_coords)
        crop = crop.filter(ImageFilter.GaussianBlur(blur_radius))
        overlay = Image.new('RGBA', crop.size, (0, 0, 0, opacity))
        crop = Image.alpha_composite(crop, overlay)
        return crop
