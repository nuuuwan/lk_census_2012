import os

from pypdf import PdfReader

from utils_future import File, JSONFile, Log

log = Log("PDFSourceFileMetadataMixin")


class PDFSourceFileMetadataMixin:
    @property
    def metadata_path(self):
        return os.path.join(self.dir_data, "metadata.json")

    def to_metadata(self):
        if os.path.exists(self.metadata_path):
            log.debug(f"{File(self.metadata_path)} exists.")
            return
        reader = PdfReader(self.local_path)
        first_page_lines = [
            line.replace("\xa0", " ").strip()
            for line in reader.pages[0].extract_text().splitlines()
            if line.strip()
        ]
        title = first_page_lines[0] if first_page_lines else None
        pdf_meta = reader.metadata or {}
        metadata = {
            "title": title,
            "pdf_title": pdf_meta.get("/Title"),
            "author": pdf_meta.get("/Author"),
            "creation_date": pdf_meta.get("/CreationDate"),
        }
        json_file = JSONFile(self.metadata_path)
        json_file.write(metadata)
        log.info(f"Wrote {json_file}")
