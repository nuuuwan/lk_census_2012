from utils import Log

log = Log("PDFSourceFileBuilderMixin")


class PDFSourceFileBuilderMixin:
    def build(self):

        self.download()
        self.to_metadata()
        self.build_txt()
        self.build_raw_data()
        self.build_data()
        self.validate()
        self.read_data_list()

    @classmethod
    def build_all(cls):
        file_list = cls.list()
        n_files = len(file_list)
        for i_file, file in enumerate(file_list, start=1):
            log.info("-" * 20)
            log.info(f"{i_file}/{n_files}) {file.doc_id}...")
            log.info("-" * 20)
            file.build()
