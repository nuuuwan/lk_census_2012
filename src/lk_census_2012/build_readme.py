"""Auto-generate the root README.md from repo metadata."""

import csv
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ORIGINAL_DATA_DIR = REPO_ROOT / "original_data" / "statistics_gov_lk" / "data"
DATA_DIR = REPO_ROOT / "data"
README_PATH = REPO_ROOT / "README.md"
SAMPLE_ROWS = 10


def _field_label(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def _table_type(title: str) -> str:
    return "person" if "Population" in title else "household"


def _slug(title: str) -> str:
    return title.lower().replace(" ", "_").replace("/", "_")


def load_metadata():
    with open(ORIGINAL_DATA_DIR / "tables.json") as f:
        tables = json.load(f)
    with open(ORIGINAL_DATA_DIR / "fields.json") as f:
        fields = json.load(f)
    return tables, fields


def count_regions() -> dict:
    gnds, dsds, districts, provinces = set(), set(), set(), set()
    for dsd_file in ORIGINAL_DATA_DIR.glob("data_*.json"):
        dsd_num = dsd_file.stem[len("data_") :]
        dsd_id = f"LK_{dsd_num}"
        dsds.add(dsd_id)
        districts.add(dsd_id[:5])
        provinces.add(dsd_id[:4])
        with open(dsd_file) as f:
            for gnd_num in json.load(f):
                gnds.add(f"LK_{gnd_num}")
    return {
        "gnds": len(gnds),
        "dsds": len(dsds),
        "districts": len(districts),
        "provinces": len(provinces),
    }


def _is_numeric(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def _fmt(value: str) -> str:
    """Format a cell: comma-separate numbers, leave strings as-is."""
    try:
        i = int(value)
        return f"{i:,}"
    except ValueError:
        pass
    try:
        f = float(value)
        return f"{f:,.4f}".rstrip("0").rstrip(".")
    except ValueError:
        pass
    return value


def sample_table_md(csv_path: Path, n: int = SAMPLE_ROWS) -> list[str]:
    """Return a markdown table of the first n rows of a CSV."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(n) if True]

    # Determine alignment per column: right-align if any data cell is numeric
    is_num = [
        any(_is_numeric(row[i]) for row in rows if i < len(row))
        for i in range(len(header))
    ]
    sep = (
        "|"
        + "|".join("---:" if is_num[i] else "---" for i in range(len(header)))
        + "|"
    )
    header_row = "|" + "|".join(header) + "|"
    data_rows = [
        "|"
        + "|".join(_fmt(cell) if _is_numeric(cell) else cell for cell in row)
        + "|"
        for row in rows
    ]
    return [header_row, sep] + data_rows


def build_readme(tables, fields) -> str:
    counts = count_regions()
    n_tables = len(tables)

    person_tables = sorted(
        [
            (tid, m)
            for tid, m in tables.items()
            if _table_type(m["Title"]) == "person"
        ],
        key=lambda x: int(x[0]),
    )
    household_tables = sorted(
        [
            (tid, m)
            for tid, m in tables.items()
            if _table_type(m["Title"]) == "household"
        ],
        key=lambda x: int(x[0]),
    )

    lines = []

    # Title & intro
    lines += [
        "# Sri Lanka — Census of Population and Housing 2012",
        "",
        "Processed data from Sri Lanka's **Census of Population and Housing 2012**,",
        "organised into clean CSV tables with statistics at every administrative level.",
        "",
    ]

    # Source
    lines += [
        "## Source",
        "",
        "Originally extracted from [@alexstorer/srilanka](https://github.com/alexstorer/srilanka),",
        "an app built by @alexstorer for the Department of Census and Statistics and the World Bank.",
        "The source data has since been removed, but the app remains accessible",
        "[here](https://s3-us-west-2.amazonaws.com/worldbank-srilanka/choropleth-example.html).",
        "",
    ]

    # Region hierarchy
    lines += [
        "## Region Hierarchy",
        "",
        "Each CSV row is identified by a `region_id` covering one of five administrative levels:",
        "",
        "| Level | Example | ID length | Count |",
        "|-------|---------|-----------|-------|",
        f"| GND (Grama Niladhari Division) | `LK_1127055` | 10 chars | {counts['gnds']:,} |",
        f"| DSD (Divisional Secretariat Division) | `LK_1127` | 7 chars | {counts['dsds']:,} |",
        f"| District | `LK_11` | 5 chars | {counts['districts']:,} |",
        f"| Province | `LK_1` | 4 chars | {counts['provinces']:,} |",
        "| Country | `LK` | 2 chars | 1 |",
        "",
        "The hierarchy runs GND → DSD → District → Province → Country.",
        "Each table includes aggregated rows for all parent levels, computed by summing GND values.",
        "",
    ]

    # Data format
    lines += [
        "## Data Format",
        "",
        f"**{n_tables} CSV files** in `data/`, one per census table, named:",
        "",
        "```",
        "<NN>-<type>-<table_name>.csv",
        "```",
        "",
        "- `<NN>` — zero-padded table number",
        "- `<type>` — `person` (population statistics) or `household` (housing statistics)",
        "- `<table_name>` — lower_snake_case table title",
        "",
        "Each file has a `region_id` column followed by lower_snake_case field columns.",
        "",
    ]

    # Tables with samples
    def table_section(title, table_list):
        section = [f"## {title}", ""]
        for tid, meta in table_list:
            table_type = _table_type(meta["Title"])
            slug = _slug(meta["Title"])
            fname = f"{int(tid):02d}-{table_type}-{slug}.csv"
            table_fields = fields.get(tid, {})
            sorted_fids = sorted(table_fields.keys(), key=lambda x: int(x))
            field_names = ", ".join(
                f"`{_field_label(table_fields[fid])}`" for fid in sorted_fids
            )
            section += [f"### `{fname}`", "", f"Fields: {field_names}", ""]

            csv_path = DATA_DIR / fname
            if csv_path.exists():
                section += [f"*First {SAMPLE_ROWS} rows:*", ""]
                section += sample_table_md(csv_path)
            section.append("")
        return section

    lines += table_section("Person (Population) Tables", person_tables)
    lines += table_section("Household Tables", household_tables)

    # Build instructions
    lines += [
        "## Regenerating the Data",
        "",
        "```bash",
        "python src/lk_census_2012/build_csvs.py",
        "python src/lk_census_2012/build_readme.py",
        "```",
        "",
    ]

    return "\n".join(lines)


def main():
    tables, fields = load_metadata()
    content = build_readme(tables, fields)
    README_PATH.write_text(content, encoding="utf-8")
    print(f"Wrote {README_PATH}")


if __name__ == "__main__":
    main()
