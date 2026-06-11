from census.pdf_source_file.PDFSourceFileBase import PDFSourceFileBase
from census.pdf_source_file.PDFSourceFileBuilderMixin import (
    PDFSourceFileBuilderMixin,
)
from census.pdf_source_file.PDFSourceFileDataMixin import (
    PDFSourceFileDataMixin,
)
from census.pdf_source_file.PDFSourceFileDownloadMixin import (
    PDFSourceFileDownloadMixin,
)
from census.pdf_source_file.PDFSourceFileMetadataMixin import (
    PDFSourceFileMetadataMixin,
)
from census.pdf_source_file.PDFSourceFileRawDataMixin import (
    PDFSourceFileRawDataMixin,
)
from census.pdf_source_file.PDFSourceFileTxtMixin import PDFSourceFileTxtMixin
from census.pdf_source_file.PDFSourceFileValidateMixin import (
    PDFSourceFileValidateMixin,
)
from census.pdf_source_file.SourceConfig import SourceConfig
from utils_future import Log

log = Log("PDFSourceFile")


class PDFSourceFile(
    PDFSourceFileBase,
    PDFSourceFileBuilderMixin,
    PDFSourceFileDownloadMixin,
    PDFSourceFileMetadataMixin,
    PDFSourceFileTxtMixin,
    PDFSourceFileDataMixin,
    PDFSourceFileRawDataMixin,
    PDFSourceFileValidateMixin,
):

    @classmethod
    def list(cls):
        files = []
        for config in SourceConfig.LIST[-1:]:
            file = cls(
                group=config["group"],
                i_group=config["i_group"],
                title=config.get("title"),
                fields=config["fields"],
                i_total=config["i_total"],
                offset=config["offset"],
            )
            files.append(file)

        return files
