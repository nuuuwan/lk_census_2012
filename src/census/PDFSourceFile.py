import os

import requests
from utils import File, Log

log = Log("PDFSourceFile")


class PDFSourceFile:
    DIR_DATA = "data"

    def __init__(self, group, i_group, url):
        self.group = group
        self.i_group = i_group
        self.url = url

    @property
    def local_path(self):
        return os.path.join(
            self.DIR_DATA, f"{self.group}_P{self.i_group:02d}.pdf"
        )

    def download(self):
        if not os.path.exists(self.local_path):
            log.debug(f"🌐 Downloading {self.url}...")
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            os.makedirs(self.DIR_DATA, exist_ok=True)
            with open(self.local_path, "wb") as f:
                f.write(response.content)
            log.info(f"Downloaded {self.url} to {File(self.local_path)}.")
        else:
            log.debug(f"File {File(self.local_path)} already exists.")

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

    @classmethod
    def build_all(cls):
        for file in cls.list():
            file.download()
