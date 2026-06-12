import os
import re

import camelot
import pandas as pd
import pymupdf
from tqdm import tqdm

from census.pdf_source_file.ParseUtils import ParseUtils
from utils_future import File, JSONFile, Log

log = Log("PDFSourceFileRawDataMixin")


class PDFSourceFileRawDataMixin:
    MAX_PAGES_TO_PROCESS = 10

    DASH_MAP = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
    }

    @property
    def raw_data_path(self):
        return os.path.join(self.dir_data, "raw_data.json")

    @property
    def numeric_columns(self):
        return ["total_value"] + self.fields

    @property
    def column_names(self):
        return (
            ["region_name"]
            + (["gnd_num"] if self.has_gnd_num else [])
            + self.numeric_columns
        )

    @property
    def n_columns(self):
        return len(self.column_names)

    # Minimum width (points) of a whitespace gap to count as a column
    # separator.
    COL_GAP_MIN = 12
    # Tolerance (points) for matching a gap to an existing separator cluster.
    COL_CLUSTER_TOL = 45

    @classmethod
    def _infer_columns(cls, page, n_columns):
        words = page.get_text("words")

        rows = {}
        Q_Y = 5
        for w in words:
            y0, x0, y1, x1, text = w[:5]
            y_key = round((y0 + y1) / 2.0 / Q_Y) * Q_Y
            rows.setdefault(y_key, []).append((x0, x1, text))

        # Collect mid-x of every wide gap between consecutive words in a row.
        clusters = []  # each: {"count": int, "mids": [float]}
        for row in rows.values():
            xs = sorted(row)
            for (_, x1_a, w_a), (x0_b, _, w_b) in zip(xs, xs[1:]):
                assert x1_a <= x0_b
                if x0_b - x1_a < cls.COL_GAP_MIN:
                    continue
                mid = (x1_a + x0_b) / 2.0
                for c in clusters:
                    centroid = sum(c["mids"]) / len(c["mids"])
                    if abs(mid - centroid) <= cls.COL_CLUSTER_TOL:
                        c["count"] += 1
                        c["mids"].append(mid)
                        break
                else:
                    clusters.append({"count": 1, "mids": [mid]})

        # Keep the most persistent separators, then order them left to right.
        clusters.sort(key=lambda c: c["count"], reverse=True)

        seps = sorted(
            round(sum(c["mids"]) / len(c["mids"]), 2)
            for c in clusters[: n_columns - 1]
        )

        if len(seps) != n_columns - 1:
            log.debug(f"len(rows)={len(rows)}")
            log.debug(f"len(clusters)={len(clusters)}")
            log.debug(f"Inferred {len(seps)} separators: {seps}")
            raise ValueError(
                f"Invalid number of seperators: {
                    len(seps)} != {
                    n_columns - 1}."
            )
        columns = ",".join(str(s) for s in seps)
        return columns

    def _normalize_columns(self, df):
        n = self.n_columns
        if df.shape[1] > n:
            df = df.iloc[:, :n]
        elif df.shape[1] < n:
            for j in range(df.shape[1], n):
                df[j] = ""
        df.columns = self.column_names
        return df

    _NUM_RE = re.compile(r"^-?\d+(\.\d+)?$")

    @classmethod
    def _is_numeric_cell(cls, v):
        s = str(v).strip().replace("\xa0", "").replace(",", "")
        if s in ("", "-"):
            return True
        return bool(cls._NUM_RE.match(s))

    def _is_valid_row(self, row):
        if str(row["region_name"]).strip().replace("\xa0", "") == "":
            return False
        return all(
            self._is_numeric_cell(row[col]) for col in self.numeric_columns
        )

    def _filter_valid_rows(self, df):
        mask = df.apply(self._is_valid_row, axis=1)
        n_dropped = int((~mask).sum())
        if n_dropped:
            log.debug(f"Dropping {n_dropped} malformed rows.")
        return df[mask].reset_index(drop=True)

    def remap_raw_data(self, d):
        values = {
            field: ParseUtils.parse_int(d[field]) for field in self.fields
        }

        total_value = sum(values.values())
        total_value_from_source = ParseUtils.parse_int(d["total_value"])
        if total_value != total_value_from_source:
            log.debug(f"{d=}")
            raise ValueError(
                f"Totals mismatch for {d['region_name']}:"
                + f" {total_value} != {total_value_from_source}"
            )

        return dict(
            region_name=d["region_name"],
            gnd_num=d.get("gnd_num"),
            total_value=total_value,
            values=values,
            total_value_from_source=total_value_from_source,
        )

    def build_raw_data(self):
        if os.path.exists(self.raw_data_path):
            log.debug(f"{File(self.raw_data_path)} exists.")
            return

        doc = pymupdf.open(self.local_path)
        n_pages = len(doc)
        last_page = min(n_pages, self.MAX_PAGES_TO_PROCESS or n_pages)

        dfs = []
        for i_page in tqdm(
            range(1, last_page + 1), desc="Extracting raw data"
        ):
            columns = self._infer_columns(doc[i_page - 1], self.n_columns)
            tables = camelot.read_pdf(
                self.local_path,
                pages=str(i_page),
                flavor="stream",
                edge_tol=500,
                row_tol=self.row_tol,
                strip_text="\n",
                columns=[columns],
            )
            for table in tables:
                dfs.append(self._normalize_columns(table.df))

        doc.close()

        if not dfs:
            log.warning(f"No tables found in {self.local_path}")
            return

        df = pd.concat(dfs, ignore_index=True)
        df = df.replace(self.DASH_MAP, regex=True)
        df = self._filter_valid_rows(df)

        if df.empty:
            log.warning(f"No valid rows after filtering in {self.local_path}")
            return

        data_list = [
            self.remap_raw_data(d) for d in df.to_dict(orient="records")
        ]
        json_file = JSONFile(self.raw_data_path)
        json_file.write(data_list)
        log.info(f"Wrote {len(data_list)} rows to {json_file}.")

    def read_raw_data_list(self):
        return JSONFile(self.raw_data_path).read()
