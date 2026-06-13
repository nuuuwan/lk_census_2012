import os
import re

import camelot
import pandas as pd
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from tqdm import tqdm

from census.pdf_source_file.ParseUtils import ParseUtils
from utils_future import File, JSONFile, Log

log = Log("PDFSourceFileRawDataMixin")


class PDFSourceFileRawDataMixin:
    MAX_PAGES_TO_PROCESS = 3
    MAX_PAGES_FOR_LAYOUT_ANALYSIS = 3

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
    COL_GAP_MIN = 5
    # Tolerance (points) for matching a gap to an existing separator cluster.
    COL_CLUSTER_TOL = 20

    @staticmethod
    def _iter_pdfminer_words(page_layout):
        for element in page_layout:
            if not isinstance(element, LTTextContainer):
                continue
            for line in element:
                if not isinstance(line, LTTextLine):
                    continue

                cur_chars = []  # list of (x0, x1, char)
                for ch in line:
                    text = getattr(ch, "get_text", lambda: "")()
                    x0 = getattr(ch, "x0", None)
                    x1 = getattr(ch, "x1", None)
                    y0 = getattr(ch, "y0", None)
                    y1 = getattr(ch, "y1", None)

                    is_space = (text == "") or text.isspace()
                    if is_space or x0 is None:
                        if cur_chars:
                            yield PDFSourceFileRawDataMixin._emit_word(
                                cur_chars
                            )
                            cur_chars = []
                        continue

                    cur_chars.append((x0, x1, y0, y1, text))

                if cur_chars:
                    yield PDFSourceFileRawDataMixin._emit_word(cur_chars)

    @staticmethod
    def _emit_word(chars):
        x0 = min(c[0] for c in chars)
        x1 = max(c[1] for c in chars)
        y_mid = sum((c[2] + c[3]) / 2.0 for c in chars) / len(chars)
        text = "".join(c[4] for c in chars)
        return (x0, x1, y_mid, text)

    def _infer_columns(self, page_layouts, n_columns):
        clusters = []  # each: {"count": int, "mids": [float], "samples": []}
        Q_Y = 5

        for page_layout in page_layouts:
            rows = {}
            for x0, x1, y_mid, text in self._iter_pdfminer_words(page_layout):
                y_key = round(y_mid / Q_Y) * Q_Y
                rows.setdefault(y_key, []).append((x0, x1, text))

            rows = dict(sorted(rows.items(), key=lambda kv: kv[0]))

            for row in rows.values():
                infos = sorted(row)
                for (_, x1_a, w_a), (x0_b, _, w_b) in zip(infos, infos[1:]):
                    gap = x0_b - x1_a
                    if gap < self.COL_GAP_MIN:
                        # log.debug(
                        #     f'too close: "{w_b}" and "{w_a}" ({gap:.2f})'
                        # )
                        continue

                    mid = (x1_a + x0_b) / 2.0
                    best = None
                    best_dist = None
                    for c in clusters:
                        centroid = sum(c["mids"]) / len(c["mids"])
                        dist = abs(mid - centroid)
                        if dist <= self.COL_CLUSTER_TOL and (
                            best_dist is None or dist < best_dist
                        ):
                            best, best_dist = c, dist

                    if best is not None:
                        best["count"] += 1
                        best["mids"].append(mid)
                        best["samples"].append((w_b, w_a))
                    else:
                        clusters.append(
                            {
                                "count": 1,
                                "mids": [mid],
                                "samples": [(w_b, w_a)],
                            }
                        )

        clusters.sort(key=lambda c: c["count"], reverse=True)

        # for cluster in clusters:
        #     log.debug(
        #         f'{cluster["count"]:d}'
        #         + "\t"
        #         + "\t".join(
        #             [(f"{s[0]}...{s[1]}") for s in cluster["samples"][:4]]
        #         ),
        #     )

        clusters = clusters[: n_columns - 1]

        def _central(xs):
            mean = sum(xs) / len(xs)
            return mean

        seps = sorted(round(_central(c["mids"]), 2) for c in clusters)

        if len(seps) != n_columns - 1:
            log.debug(f"column_names={str(self.column_names)}")
            log.debug(f"{n_columns=}")
            log.debug(f"len(clusters)={len(clusters)}")
            log.debug(f"Inferred {len(seps)} separators: {seps}")
            raise ValueError(
                f"Invalid number of seps: {len(seps)} != {n_columns - 1}."
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
        if "region_name" not in d:
            return None
        region_name = d["region_name"]
        if not region_name:
            return None
        region_name = re.sub(r"[^\x00-\x7F]+", " ", region_name)
        region_name = region_name.strip()

        for invalid_region_name_text in ["District", "Population"]:
            if invalid_region_name_text in region_name:
                return None

        if not d["total_value"]:
            return None

        try:
            values = {
                field: ParseUtils.parse_int(d[field]) for field in self.fields
            }
            total_value_from_source = ParseUtils.parse_int(d["total_value"])
        except Exception as e:
            log.debug(f"{region_name=}, {d=}")
            raise e
        if total_value_from_source == 0:
            return None

        total_value = sum(values.values())
        if total_value != total_value_from_source:
            log.debug(f"{d=}")
            raise ValueError(
                f"Totals mismatch for {d['region_name']}:"
                + f" {total_value} != {total_value_from_source}"
            )

        return dict(
            region_name=region_name,
            gnd_num=d.get("gnd_num"),
            total_value=total_value,
            values=values,
            total_value_from_source=total_value_from_source,
        )

    def process_page(
        self,
        i_page,
        columns,
        table_areas,
    ):
        dfs = []
        try:
            tables = camelot.read_pdf(
                self.local_path,
                pages=str(i_page),
                flavor="stream",
                edge_tol=500,
                row_tol=self.row_tol,
                strip_text="\n",
                columns=[columns],
                table_areas=table_areas,
            )
        except Exception as e:
            log.debug(f"column_names={self.column_names}")
            log.debug(f"{i_page=}")
            log.debug(f"{columns=}")
            raise e

        for table in tables:
            dfs.append(self._normalize_columns(table.df))

        if i_page == 1:
            camelot.plot(tables[0], kind="grid").savefig(
                f"debug_{self.doc_id}_{i_page}.png", dpi=300
            )
        return dfs

    def _compute_table_areas(self, page_layouts):
        page_layout = page_layouts[0]
        y0 = min(e.y0 for e in page_layout if isinstance(e, LTTextContainer))
        y1 = max(e.y1 for e in page_layout if isinstance(e, LTTextContainer))
        x0 = min(e.x0 for e in page_layout if isinstance(e, LTTextContainer))
        x1 = max(e.x1 for e in page_layout if isinstance(e, LTTextContainer))
        return [f"{x0},{y0},{x1},{y1}"]

    def build_raw_data(self):
        if os.path.exists(self.raw_data_path):
            log.debug(f"{File(self.raw_data_path)} exists.")
            return

        # Lay out every page once with pdfminer so column inference and
        # camelot share one coordinate frame.
        page_layouts_for_analysis = list(
            extract_pages(
                self.local_path,
                page_numbers=range(self.MAX_PAGES_FOR_LAYOUT_ANALYSIS),
            )
        )

        columns = self._infer_columns(
            page_layouts_for_analysis, self.n_columns
        )

        doc = PDFDocument(PDFParser(open(self.local_path, "rb")))
        n_pages = doc.catalog["Pages"].resolve()["Count"]
        last_page = min(n_pages, self.MAX_PAGES_TO_PROCESS)

        table_areas = self._compute_table_areas(
            page_layouts_for_analysis,
        )

        dfs = []
        for i_page in tqdm(
            range(1, last_page + 1), desc="Extracting raw data"
        ):
            dfs_for_page = self.process_page(i_page, columns, table_areas)
            dfs.extend(dfs_for_page)

        if not dfs:
            log.warning(f"No tables found in {self.local_path}")
            return

        df = pd.concat(dfs, ignore_index=True)
        df = df.replace(self.DASH_MAP, regex=True)

        if df.empty:
            log.warning(f"No valid rows after filtering in {self.local_path}")
            return

        data_list = [
            self.remap_raw_data(d) for d in df.to_dict(orient="records")
        ]
        data_list = [d for d in data_list if d is not None]
        json_file = JSONFile(self.raw_data_path)
        json_file.write(data_list)
        log.info(f"Wrote {len(data_list)} rows to {json_file}.")

    def read_raw_data_list(self):
        return JSONFile(self.raw_data_path).read()
