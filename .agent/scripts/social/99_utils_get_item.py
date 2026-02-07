import sys
import json
from pathlib import Path

def get_item(post_dir, index):
    target_dir = Path(post_dir)
    input_path = target_dir / "social_schedule_base64.json"

    if not input_path.exists():
        print(f"Error: {input_path} not found.")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        schedule = json.load(f)

    if index < 0 or index >= len(schedule):
        print(f"Error: Index {index} out of range (0-{len(schedule)-1})")
        sys.exit(1)

    # Return as a list containing just this item, to match socialPost array expectation
    print(json.dumps([schedule[index]], ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python get_schedule_item.py <post_directory> <index>")
        sys.exit(1)

    get_item(sys.argv[1], int(sys.argv[2]))
