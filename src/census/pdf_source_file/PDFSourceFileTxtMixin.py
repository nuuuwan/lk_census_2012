import os

import camelot
import pandas as pd

from utils_future import File, Log

log = Log("PDFSourceFileTxtMixin")


class PDFSourceFileTxtMixin:
    @property
    def txt_path(self):
        return os.path.join(self.dir_data, "data.txt")

    def to_txt(self):
        if os.path.exists(self.txt_path):
            log.debug(f"{File(self.txt_path)} already exists.")
            return

        tables = camelot.read_pdf(
            self.local_path, pages="all", flavor="stream"
        )
        dfs = []
        for table in tables:
            dfs.append(table.df)

        if not dfs:
            log.warning(f"No tables found in {self.local_path}")
            return

        df = pd.concat(dfs, ignore_index=True)
        df.to_csv(self.txt_path, sep="\t", index=False, header=False)
        log.info(f"Saved {len(df)} rows to {File(self.txt_path)}.")
