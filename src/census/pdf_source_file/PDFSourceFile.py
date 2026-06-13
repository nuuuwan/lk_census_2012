from census.pdf_source_file.PDFSourceFileBase import PDFSourceFileBase
from census.pdf_source_file.PDFSourceFileBuilderMixin import \
    PDFSourceFileBuilderMixin
from census.pdf_source_file.PDFSourceFileDataMixin import \
    PDFSourceFileDataMixin
from census.pdf_source_file.PDFSourceFileDownloadMixin import \
    PDFSourceFileDownloadMixin
from census.pdf_source_file.PDFSourceFileMetadataMixin import \
    PDFSourceFileMetadataMixin
from census.pdf_source_file.PDFSourceFileRawDataMixin import \
    PDFSourceFileRawDataMixin
from census.pdf_source_file.PDFSourceFileValidateMixin import \
    PDFSourceFileValidateMixin
from utils_future import Log

log = Log("PDFSourceFile")


class PDFSourceFile(
    PDFSourceFileBase,
    #
    PDFSourceFileBuilderMixin,
    #
    PDFSourceFileDownloadMixin,
    PDFSourceFileMetadataMixin,
    PDFSourceFileRawDataMixin,
    PDFSourceFileDataMixin,
    PDFSourceFileValidateMixin,
):

    pass
