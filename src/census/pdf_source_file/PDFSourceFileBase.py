from dataclasses import dataclass


@dataclass
class PDFSourceFileBase:
    group: str
    i_group: int
    title: str
    fields: list[str]
    i_total: int
    offset: int

    @property
    def doc_id(self):
        return self.group + "-" + self.title.title().replace(" ", "-")
