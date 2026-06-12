from census.pdf_source_file.PDFSourceConfig import PDFSourceConfig


class PDFSourceFileLoader:
    @classmethod
    def list(cls):
        files = []
        for config in PDFSourceConfig.LIST[:2]:
            file = cls(
                group=config["group"],
                i_group=config["i_group"],
                title=config.get("title"),
                fields=config["fields"],
                has_gnd_num=config["has_gnd_num"],
                row_tol=config.get("row_tol", 10),
            )
            files.append(file)

        return files
