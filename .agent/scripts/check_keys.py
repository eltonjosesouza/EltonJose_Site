import json
from pathlib import Path
import sys

path = Path(sys.argv[1]) / "social_schedule_base64.json"
with open(path) as f:
    data = json.load(f)
    print("Keys in first item:", data[0].keys())
