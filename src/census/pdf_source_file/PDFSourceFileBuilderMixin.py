from utils import Log

from census.pdf_source_file.PDFSourceConfig import PDFSourceConfig

log = Log("PDFSourceFileBuilderMixin")


class DEFAULT:
    HAS_GND_NUM = True
    ROW_TOL = 10


class PDFSourceFileBuilderMixin:
    @classmethod
    def list(cls):
        files = []
        for config in PDFSourceConfig.LIST:
            file = cls(
                group=config["group"],
                i_group=config["i_group"],
                title=config.get("title"),
                fields=config["fields"],
                has_gnd_num=config.get("has_gnd_num", DEFAULT.HAS_GND_NUM),
            )
            files.append(file)

        return files

    def build(self):
        self.download()
        self.to_metadata()
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
