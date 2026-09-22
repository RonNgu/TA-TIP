import json
from pathlib import Path

JSON_FILE = Path(__file__).resolve().parents[1] / "TIP" / "data" / "processed" / "indicators.json"

with JSON_FILE.open("r", encoding="utf-8") as f:
    data = json.load(f)

for record in data:
    print(json.dumps(record))