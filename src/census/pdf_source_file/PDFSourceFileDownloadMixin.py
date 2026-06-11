import os

import requests

from utils_future import File, Log

log = Log("PDFSourceFileDownloadMixin")


class PDFSourceFileDownloadMixin:

    DIR_DATA = "data"

    @property
    def local_path(self):
        return os.path.join(self.dir_data, "source.pdf")

    @property
    def url(self):
        code = self.group[0].upper()
        group_str = self.group
        if group_str == "Population":
            group_str = group_str.lower()
        return (
            "http://203.94.94.83:8041"
            + "/Pages/Activities/Reports/FinalReport_GN"
            + f"/{group_str}/{code}{self.i_group}.pdf"
        )

    def download(self):
        if not os.path.exists(self.local_path):
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            os.makedirs(self.dir_data, exist_ok=True)
            with open(self.local_path, "wb") as f:
                f.write(response.content)
            log.info(f"🌐 Downloaded {self.url} to {File(self.local_path)}.")
        else:
            log.debug(f"File {File(self.local_path)} exists.")

    @property
    def dir_data(self):
        dir_data = os.path.join(self.DIR_DATA, self.doc_id)
        os.makedirs(dir_data, exist_ok=True)
        return dir_data
