"""
Convert original census JSON data into one CSV file per table.

Source layout:
  original_data/statistics_gov_lk/data/
    tables.json         — table metadata  (table_id → {Title, …})
    fields.json         — field metadata  (table_id → {field_id → label})
    data_<dsd_num>.json — census data     (gnd_num → table_id → field_id → value)

Output:
  data/table_<NN>_<title_slug>.csv
    Columns: gnd_id, <field labels (lower_snake_case) …>
    One row per GND record.
"""

import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ORIGINAL_DATA_DIR = REPO_ROOT / "original_data" / "statistics_gov_lk" / "data"
OUTPUT_DATA_DIR = REPO_ROOT / "data"


def _slug(title: str) -> str:
    return title.lower().replace(" ", "_").replace("/", "_")


def _field_label(label: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def load_metadata():
    with open(ORIGINAL_DATA_DIR / "tables.json") as f:
        tables = json.load(f)
    with open(ORIGINAL_DATA_DIR / "fields.json") as f:
        fields = json.load(f)
    return tables, fields


def build_rows_by_table(table_ids):
    """Return dict: table_id -> list of {dsd_id, gnd_id, data}."""
    rows = {tid: [] for tid in table_ids}

    for dsd_file in sorted(ORIGINAL_DATA_DIR.glob("data_*.json")):
        dsd_num = dsd_file.stem[len("data_") :]
        dsd_id = f"LK_{dsd_num}"

        with open(dsd_file) as f:
            dsd_data = json.load(f)

        for gnd_num, gnd_tables in dsd_data.items():
            gnd_id = f"LK_{gnd_num}"
            for table_id, field_values in gnd_tables.items():
                if table_id in rows:
                    rows[table_id].append(
                        {
                            "dsd_id": dsd_id,
                            "gnd_id": gnd_id,
                            "data": field_values,
                        }
                    )

    return rows


def write_csvs(tables, fields, rows):
    OUTPUT_DATA_DIR.mkdir(exist_ok=True)

    for table_id, table_meta in sorted(
        tables.items(), key=lambda x: int(x[0])
    ):
        table_fields = fields.get(table_id, {})
        if not table_fields:
            continue

        sorted_field_ids = sorted(table_fields.keys(), key=lambda x: int(x))
        field_labels = [
            _field_label(table_fields[fid]) for fid in sorted_field_ids
        ]

        title_slug = _slug(table_meta["Title"])
        out_path = (
            OUTPUT_DATA_DIR / f"table_{int(table_id):02d}_{title_slug}.csv"
        )

        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["region_id"] + field_labels)

            for row in rows[table_id]:
                values = [row["gnd_id"]] + [
                    row["data"].get(fid, "") for fid in sorted_field_ids
                ]
                writer.writerow(values)

        print(f"  wrote {out_path.name}  ({len(rows[table_id])} rows)")


def main():
    print("Loading metadata …")
    tables, fields = load_metadata()

    print("Reading DSD files …")
    rows = build_rows_by_table(set(tables.keys()))

    print(f"Writing {len(tables)} CSV files to {OUTPUT_DATA_DIR} …")
    write_csvs(tables, fields, rows)
    print("Done.")


if __name__ == "__main__":
    main()
