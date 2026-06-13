from census.pdf_source_file.PDFSourceConfig import PDFSourceConfig


class DEFAULT:
    HAS_GND_NUM = True
    ROW_TOL = 10


class PDFSourceFileLoader:
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
                row_tol=config.get("row_tol", DEFAULT.ROW_TOL),
            )
            files.append(file)

        return files
