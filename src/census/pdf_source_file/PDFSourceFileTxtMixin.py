import os

import camelot
import pandas as pd
import pymupdf

from utils_future import File, Log

log = Log("PDFSourceFileTxtMixin")


class PDFSourceFileTxtMixin:
    @property
    def txt_path(self):
        return os.path.join(self.dir_data, "data.txt")

    def build_txt(self):
        if os.path.exists(self.txt_path):
            log.debug(f"{File(self.txt_path)} exists.")
            return
        log.debug(f"Extracting tables from {File(self.local_path)}...")

        doc = pymupdf.open(self.local_path)
        n_pages = len(doc)
        doc.close()
        log.debug(f"Found {n_pages} pages in {File(self.local_path)}.")

        dfs = []
        for i_page in range(1, n_pages + 1):
            try:
                tables = camelot.read_pdf(
                    self.local_path,
                    pages=str(i_page),
                    flavor="stream",
                )
                for table in tables:
                    dfs.append(table.df)
            except Exception as e:
                log.warning(f"Skipping page {i_page}: {e}")

        if not dfs:
            log.warning(f"No tables found in {self.local_path}")
            return

        df = pd.concat(dfs, ignore_index=True)
        df.to_csv(self.txt_path, sep="\t", index=False, header=False)
        log.info(f"Saved {len(df)} rows to {File(self.txt_path)}.")
