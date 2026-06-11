from dataclasses import dataclass


@dataclass
class PDFSourceFileBase:
    group: str
    i_group: int
    title: str
    fields: list[str]
    i_total: int

    @property
    def doc_id(self):
        return self.group.title() + "-" + self.title.title().replace(" ", "-")
