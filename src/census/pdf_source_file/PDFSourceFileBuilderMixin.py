from utils import Log

log = Log("PDFSourceFileBuilderMixin")


class PDFSourceFileBuilderMixin:
    def build(self):
        log.info("-" * 20)
        log.info(f"{self.doc_id}...")
        log.info("-" * 20)

        self.download()
        self.to_metadata()
        self.build_txt()
        self.build_raw_data()
        self.build_data()
        self.validate()
        self.read_data_list()

    @classmethod
    def build_all(cls):
        for file in cls.list():
            file.build()
