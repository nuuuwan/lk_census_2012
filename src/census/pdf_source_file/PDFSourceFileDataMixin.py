import os

from census.pdf_source_file.ParseUtils import ParseUtils
from census.pdf_source_file.PDFSourceFileDataExpandMixin import (
    PDFSourceFileDataExpandMixin,
)
from utils_future import File, JSONFile, Log

log = Log("PDFSourceFileDataMixin")


class PDFSourceFileDataMixin(PDFSourceFileDataExpandMixin):

    @property
    def data_path(self):
        return os.path.join(self.dir_data, "data.json")

    @property
    def errors_path(self):
        return os.path.join(self.dir_data, "errors.json")

    def extract_fields(self, lines):
        fields = []
        for line in lines:
            line = line.replace("\u2010", "-")
            tokens = line.split()
            if tokens[:2] == ["number", "Total"]:
                fields = tokens[2:]
                return fields
        raise ValueError("Fields not found in the text file.")

    @staticmethod
    def _extract_line(line, fields):
        line = line.replace("\u2010", "-")
        tokens = line.split()
        n_tokens = len(tokens)
        if n_tokens < 10:
            return None
        if tokens[:2] == ["number", "Total"]:
            return None
        i_field_start = n_tokens - len(fields) + 1
        region_name_and_num = " ".join(tokens[0:(i_field_start)])

        words = region_name_and_num.split()
        last_word = words[-1]
        if any([c.isdigit() for c in last_word]):
            gnd_num = last_word
            region_name = " ".join(words[:-1])
        elif len(words) > 2 and words[-2].isdigit():
            gnd_num = words[-2] + "" + words[-1]
            region_name = " ".join(words[:-2])
        else:
            gnd_num = None
            region_name = region_name_and_num

        total_value_from_source = ParseUtils.parse_int(tokens[i_field_start])
        values_only = [
            ParseUtils.parse_int(token)
            for token in tokens[i_field_start + 1 :]
        ]
        values = dict(zip(fields, values_only))
        total_value = sum(values_only)
        return dict(
            region_name=region_name,
            gnd_num=gnd_num,
            values=values,
            total_value=total_value,
            total_value_from_source=total_value_from_source,
        )

    def _dedupe_lines(self, lines):
        seen = set()
        deduped_lines = []
        for line in lines:
            if line not in seen:
                deduped_lines.append(line)
                seen.add(line)
        return deduped_lines

    def build_data(self):
        data_file = JSONFile(self.data_path)
        if data_file.exists:
            log.debug(f"{data_file} exists.")
            return

        lines = File(self.txt_path).read_lines()
        lines = self._dedupe_lines(lines)

        fields = self.extract_fields(lines)
        errors = []
        d_list = []
        for line in lines:
            d = self._extract_line(line, fields)
            if d:
                d_list.append(d)

        if errors:
            errors_file = JSONFile(self.errors_path)
            errors_file.write(errors)
            log.warning(f"Wrote {len(errors)} errors to {errors_file}.")

        d_list = self._expand_data_list(d_list)

        data_file.write(d_list)
        log.info(f"Wrote {len(d_list)} rows to {data_file}.")
