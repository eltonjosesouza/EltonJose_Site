import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

def find_target_directory(given_path=None):
    """
    Determines the target directory.
    If a path is given, uses it.
    Otherwise, tries to determine from current working directory or arguments.
    """
    if given_path:
        target = Path(given_path)
    else:
        target = Path(os.getcwd())

    # If the target is a file (e.g., the .mdx file), use its parent directory
    if target.is_file():
        return target.parent

    return target

def parse_mdx_frontmatter(mdx_path):
    """
    Parses frontmatter to extract tags and description.
    Handles both inline '[tag]' and multi-line '- tag' formats.
    """
    tags = []
    description = ""

    try:
        with open(mdx_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        in_frontmatter = False
        in_tags_block = False

        for line in lines:
            stripped = line.strip()

            # Detect frontmatter boundaries
            if stripped == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break # End of frontmatter

            if not in_frontmatter:
                continue

            # Extract Description
            if stripped.startswith('description:'):
                in_tags_block = False
                # Try to get inline description
                match = re.search(r'description:\s*["\']?(.*?)["\']?$', stripped)
                if match:
                    description = match.group(1)

            # Extract Tags
            elif stripped.startswith('tags:'):
                # Check for inline format: tags: [a, b]
                match_inline = re.search(r'tags:\s*\[(.*?)\]', stripped)
                if match_inline:
                    raw_tags = match_inline.group(1)
                    tags = [t.strip().strip("'").strip('"') for t in raw_tags.split(',')]
                    in_tags_block = False
                else:
                    # Start of multi-line block
                    in_tags_block = True

            elif in_tags_block and stripped.startswith('- '):
                tag_value = stripped[2:].strip()
                tags.append(tag_value)

            elif in_tags_block and stripped and not stripped.startswith('- '):
                 # Non-empty line that doesn't start with dash means end of tags block
                 in_tags_block = False

    except Exception as e:
        print(f"Warning: Could not read MDX frontmatter: {e}")

    return tags, description

def create_social_json(directory):
    """Creates the social.json file in the specified directory."""
    target_dir = Path(directory)
    file_path = target_dir / "social.json"
    mdx_path = target_dir / "index.mdx"

    # Update: Always overwrite if file exists to fix missing data,
    # OR logic to merge could be added here. For now, we recreate or update.
    # But user complained it wasn't populated, so let's overwrite for this fix task.
    # Ideally we should merge, but strictly adhering to 'create' for now.

    existing_data = {}
    if file_path.exists():
        print(f"File exists: {file_path}. parsing existing to merge...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except:
            pass

    # Try to get defaults from MDX
    extracted_tags = []
    extracted_description = ""
    if mdx_path.exists():
        extracted_tags, extracted_description = parse_mdx_frontmatter(mdx_path)

    # Format tags as hashtags
    hashtags = [f"#{tag.replace(' ', '')}" for tag in extracted_tags]
    if not hashtags:
         hashtags = ["#Tech", "#Dev"]

    # Use existing summary if available and not empty, otherwise usage description
    summary_short = existing_data.get('promotion', {}).get('summary_short', "")
    if not summary_short and extracted_description:
         summary_short = extracted_description

    # Prepare final data (merging logic: prefer existing non-empty values, else new ones)
    data = {
        "meta": {
            "version": "1.0",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "linked_post": mdx_path.name if mdx_path.exists() else "unknown"
        },
        "promotion": {
            "summary_short": summary_short,
            "summary_professional": existing_data.get('promotion', {}).get('summary_professional', ""),
            "hashtags": hashtags if hashtags != ["#Tech", "#Dev"] else existing_data.get('promotion', {}).get('hashtags', hashtags),
            "twitter_thread": existing_data.get('promotion', {}).get('twitter_thread', ["Tweet 1...", "Tweet 2..."])
        },
        "repost_optimization": {
            "og_title_variant": existing_data.get('repost_optimization', {}).get('og_title_variant', ""),
            "pinterest_image": existing_data.get('repost_optimization', {}).get('pinterest_image', "")
        },
        "automation": {
            "status": existing_data.get('automation', {}).get('status', "draft"),
            "platforms_posted": existing_data.get('automation', {}).get('platforms_posted', [])
        }
    }

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Success: Updated {file_path}")
        return str(file_path)
    except Exception as e:
        print(f"Error creating file: {e}")
        return None

if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None

    if path_arg == "." or path_arg is None:
        target_dir = os.getcwd()
    else:
        target_dir = path_arg

    final_path = create_social_json(target_dir)
