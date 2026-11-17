import csv
import json
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]

SOURCE_FILE = (
    APP_ROOT
    / "data"
    / "processed"
    / "indicators.json"
)

LOOKUP_FILE = (
    APP_ROOT
    / "lookups"
    / "tip_iocs.csv"
)

FIELDNAMES = [
    "indicator",
    "indicator_type",
    "sources",
    "score",
    "severity",
]

def update_lookup():
    with SOURCE_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        records = json.load(file)

    rows = []
    for record in records:
        indicator = record.get(
            "indicator",
            {}
        )

        observations = record.get(
            "observations",
            []
        )

        analysis = record.get(
            "analysis",
            {}
        )

        sources = sorted({
            observation.get("source")
            for observation in observations
            if observation.get("source")
        })

        rows.append({
            "indicator":
                indicator.get("value", ""),
            "indicator_type":
                indicator.get(
                    "indicator_type",
                    ""
                ),

            "sources":
                ";".join(sources),
            "score":
                analysis.get("score", ""),

            "severity":
                analysis.get(
                    "severity",
                    ""
                ),})

    LOOKUP_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with LOOKUP_FILE.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    update_lookup()
