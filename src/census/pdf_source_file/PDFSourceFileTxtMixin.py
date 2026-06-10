import os
import tempfile

import camelot
import pandas as pd
from pypdf import PdfReader, PdfWriter
from utils import File, Log

log = Log("PDFSourceFileTxtMixin")


class PDFSourceFileTxtMixin:
    @property
    def txt_path(self):
        return os.path.join(self.dir_data, "data.txt")

    def to_txt(self):
        if os.path.exists(self.txt_path):
            log.debug(f"{File(self.txt_path)} already exists.")
            return
        reader = PdfReader(self.local_path)
        dfs = []

        with tempfile.TemporaryDirectory() as tmpdir:
            for page_num, page in enumerate(reader.pages, start=1):
                writer = PdfWriter()
                writer.add_page(page)
                tmp_path = os.path.join(tmpdir, f"page_{page_num:04d}.pdf")
                with open(tmp_path, "wb") as f:
                    writer.write(f)

                tables = camelot.read_pdf(
                    tmp_path, pages="1", flavor="stream"
                )
                for table in tables:
                    dfs.append(table.df)

        if not dfs:
            log.warning(f"No tables found in {self.local_path}")
            return

        df = pd.concat(dfs, ignore_index=True)
        df.to_csv(self.txt_path, sep="\t", index=False, header=False)
        log.info(f"Saved {len(df)} rows to {File(self.txt_path)}.")
