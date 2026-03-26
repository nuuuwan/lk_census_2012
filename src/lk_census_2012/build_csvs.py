"""
Convert original census JSON data into one CSV file per table.

Source layout:
  original_data/statistics_gov_lk/data/
    tables.json         — table metadata  (table_id → {Title, …})
    fields.json         — field metadata  (table_id → {field_id → label})
    data_<dsd_num>.json — census data     (gnd_num → table_id → field_id → value)

Output:
  data/<NN>-<type>-<title_slug>.csv   (type: person | household)
    Columns: region_id, <field labels (lower_snake_case) …>
    One row per GND record.
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ORIGINAL_DATA_DIR = REPO_ROOT / "original_data" / "statistics_gov_lk" / "data"
OUTPUT_DATA_DIR = REPO_ROOT / "data"


def _slug(title: str) -> str:
    return title.lower().replace(" ", "_").replace("/", "_")


def _table_type(title: str) -> str:
    return "person" if "Population" in title else "household"


def _field_label(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def _parent_ids(gnd_id: str) -> list[str]:
    """Return [dsd_id, district_id, province_id, country_id] for a GND id."""
    return [gnd_id[:7], gnd_id[:5], gnd_id[:4], gnd_id[:2]]


def _aggregate_rows(gnd_rows, sorted_field_ids):
    """Aggregate GND rows into parent-level rows by summing numeric fields."""
    buckets = defaultdict(list)
    for row in gnd_rows:
        for parent_id in _parent_ids(row["gnd_id"]):
            buckets[parent_id].append(row["data"])

    agg_rows = []
    for region_id, data_list in buckets.items():
        merged = {}
        for fid in sorted_field_ids:
            total = 0
            is_float = False
            ok = True
            for d in data_list:
                raw = d.get(fid, 0)
                try:
                    v = float(raw)
                    if not float(raw).is_integer():
                        is_float = True
                    total += v
                except (ValueError, TypeError):
                    ok = False
                    break
            if ok:
                merged[fid] = total if is_float else int(total)
            else:
                merged[fid] = ""
        agg_rows.append({"region_id": region_id, "data": merged})
    return agg_rows


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
    for old in OUTPUT_DATA_DIR.glob("*.csv"):
        old.unlink()

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

        title = table_meta["Title"]
        title_slug = _slug(title)
        table_type = _table_type(title)
        out_path = (
            OUTPUT_DATA_DIR
            / f"{int(table_id):02d}-{table_type}-{title_slug}.csv"
        )

        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["region_id"] + field_labels)

            gnd_rows = rows[table_id]
            agg_rows = _aggregate_rows(gnd_rows, sorted_field_ids)

            all_rows = [
                {"region_id": r["gnd_id"], "data": r["data"]} for r in gnd_rows
            ] + agg_rows
            all_rows.sort(key=lambda r: r["region_id"])

            for row in all_rows:
                values = [row["region_id"]] + [
                    row["data"].get(fid, "") for fid in sorted_field_ids
                ]
                writer.writerow(values)

        total_rows = len(gnd_rows) + len(agg_rows)
        print(
            f"  wrote {out_path.name}  ({total_rows} rows: {len(gnd_rows)} GND + {len(agg_rows)} aggregated)"
        )


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
