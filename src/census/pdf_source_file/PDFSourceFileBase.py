from dataclasses import dataclass


@dataclass
class PDFSourceFileBase:
    group: str
    i_group: int
    title: str
    fields: list[str]
    has_gnd_num: bool
    row_tol: int = 10

    @property
    def doc_id(self):
        return self.group.title() + "-" + self.title.title().replace(" ", "-")
