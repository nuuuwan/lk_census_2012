import os

import camelot
import pandas as pd
import pymupdf
from tqdm import tqdm

from utils_future import File, Log

log = Log("PDFSourceFileTxtMixin")


class PDFSourceFileTxtMixin:
    DELIM_TXT = "|"
    MAX_PAGES_TO_PROCESS = 5

    # Unicode dash/minus variants -> ASCII "-"
    DASH_MAP = {
        "\u2010": "-",  # hyphen
        "\u2011": "-",  # non-breaking hyphen
        "\u2012": "-",  # figure dash
        "\u2013": "-",  # en dash
        "\u2014": "-",  # em dash
        "\u2212": "-",  # minus sign
    }
    DASHES = {"\u2010", "\u2011", "\u2012", "\u2013", "\u2014", "\u2212", "-"}

    @property
    def txt_path(self):
        return os.path.join(self.dir_data, "data.txt")

    DROP_DASH_COL = 3  # spurious column where Camelot drops the leading dash

    @classmethod
    def _fix_dropped_dashes(cls, df):
        def is_blank(v):
            return str(v).strip() in ("", "\xa0")

        j = cls.DROP_DASH_COL
        for i in range(len(df)):
            if j < df.shape[1] and is_blank(df.iat[i, j]):
                df.iat[i, j] = "-"
        return df

    def build_txt(self):
        if os.path.exists(self.txt_path):
            log.debug(f"{File(self.txt_path)} exists.")
            return

        doc = pymupdf.open(self.local_path)
        n_pages = len(doc)

        dfs = []
        for i_page in tqdm(
            range(
                1,
                min(
                    n_pages,
                    (
                        self.MAX_PAGES_TO_PROCESS
                        if self.MAX_PAGES_TO_PROCESS
                        else n_pages
                    ),
                )
                + 1,
            ),
            desc="Extracting text",
        ):
            page = doc[i_page - 1]
            width = page.rect.width
            height = page.rect.height

            # Find the actual bottom of content (pymupdf y increases downward)
            words = page.get_text("words")
            if words:
                max_y = max(w[3] for w in words)  # w[3] = y1 of word bbox
            else:
                max_y = height

            # Convert to PDF coordinate space (bottom-left origin)
            # pdf_y = height - pymupdf_y, so bottom of content = height - max_y
            pdf_y_min = height - max_y - 10  # 10pt padding
            table_areas = [f"0,{pdf_y_min},{width},{height}"]

            try:
                tables = camelot.read_pdf(
                    self.local_path,
                    pages=str(i_page),
                    flavor="stream",
                    edge_tol=500,
                    row_tol=self.row_tol,
                    strip_text="\n",
                    table_areas=table_areas,
                )
                for table in tables:
                    dfs.append(table.df)

            except Exception as e:
                log.warning(f"Skipping page {i_page}: {e}")

        doc.close()

        if not dfs:
            log.warning(f"No tables found in {self.local_path}")
            return

        df = pd.concat(dfs, ignore_index=True)

        # Repair dashes Camelot dropped to blank between two dashes
        # (run BEFORE normalization so flank-detection sees original glyphs too)
        df = self._fix_dropped_dashes(df)

        # Normalize all Unicode dash variants to ASCII "-"
        df = df.replace(self.DASH_MAP, regex=True)

        df.to_csv(
            self.txt_path, sep=self.DELIM_TXT, index=False, header=False
        )
        log.info(f"Saved {len(df)} rows to {File(self.txt_path)}.")
