import os

import requests

from census.pdf_source_file.PDFSourceFileDataMixin import \
    PDFSourceFileDataMixin
from census.pdf_source_file.PDFSourceFileMetadataMixin import \
    PDFSourceFileMetadataMixin
from census.pdf_source_file.PDFSourceFileTxtMixin import PDFSourceFileTxtMixin
from utils_future import File, Log

log = Log("PDFSourceFile")


class PDFSourceFile(
    PDFSourceFileMetadataMixin, PDFSourceFileTxtMixin, PDFSourceFileDataMixin
):
    DIR_ORIGINAL_DATA = "original_data"
    DIR_DATA = "data"

    def __init__(self, group, i_group, url):
        self.group = group
        self.i_group = i_group
        self.url = url

    @property
    def doc_id(self):
        return f"{self.group}_P{self.i_group:02d}"

    @property
    def local_path(self):
        return os.path.join(self.DIR_ORIGINAL_DATA, self.doc_id + ".pdf")

    def download(self):
        if not os.path.exists(self.local_path):
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            os.makedirs(self.DIR_DATA, exist_ok=True)
            with open(self.local_path, "wb") as f:
                f.write(response.content)
            log.info(f"🌐 Downloaded {self.url} to {File(self.local_path)}.")
        else:
            log.debug(f"File {File(self.local_path)} already exists.")

    @property
    def dir_data(self):
        dir_data = os.path.join(self.DIR_DATA, self.doc_id)
        os.makedirs(dir_data, exist_ok=True)
        return dir_data

    @classmethod
    def list(cls):
        files = []
        for group, n_group in [("population", 1), ("housing", 0)]:
            for i_group in range(1, n_group + 1):
                code = group[0].upper()
                url = (
                    "http://203.94.94.83:8041"
                    + "/Pages/Activities/Reports/FinalReport_GN"
                    + f"/{group}/{code}{i_group}.pdf"
                )
                files.append(cls(group, i_group, url))
        return files

    def build(self):
        self.download()
        self.to_metadata()
        self.to_txt()
        self.build_data()

    @classmethod
    def build_all(cls):
        for file in cls.list():
            file.build()
