import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

def update_schedule(post_dir, now=False, new_date=None):
    target_dir = Path(post_dir)
    schedule_path = target_dir / "social_schedule.json"

    if not schedule_path.exists():
        print(f"❌ Error: social_schedule.json not found in {target_dir}")
        print("👉 Run 'create-story' workflow first to generate it.")
        sys.exit(1)

    try:
        with open(schedule_path, 'r', encoding='utf-8') as f:
            schedule = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON: {e}")
        sys.exit(1)

    updated_count = 0
    current_utc = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    for item in schedule:
        if now:
            # Set to Publish NOW
            item['type'] = 'now'
            item['date'] = current_utc # "now" usually ignores date but good to have current
            updated_count += 1
        elif new_date:
            # Update Date, Preserve Time
            try:
                # Expecting format YYYY-MM-DDTHH:MM:SSZ or similar
                original_iso = item['date']
                if 'T' in original_iso:
                    original_time = original_iso.split('T')[1]
                else:
                    original_time = "10:00:00Z" # Default fallback

                # Reconstruct
                item['date'] = f"{new_date}T{original_time}"
                item['type'] = 'schedule' # Ensure it is schedule
                updated_count += 1
            except Exception as e:
                print(f"⚠️ Could not parse date for item: {e}")

    # Save
    with open(schedule_path, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)

    mode = "NOW" if now else f"Date: {new_date}"
    print(f"✅ Updated {updated_count} items in {schedule_path}")
    print(f"📅 Mode: {mode}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update social schedule timing.")
    parser.add_argument("post_dir", help="Directory of the blog post")
    parser.add_argument("--now", action="store_true", help="Set publication to NOW")
    parser.add_argument("--date", help="Set publication date (YYYY-MM-DD)")

    args = parser.parse_args()

    if not args.now and not args.date:
        print("ℹ️ No changes requested. Use --now or --date YYYY-MM-DD")
        sys.exit(0)

    update_schedule(args.post_dir, args.now, args.date)
