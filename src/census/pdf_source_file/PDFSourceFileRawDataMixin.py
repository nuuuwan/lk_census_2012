import os

from census.pdf_source_file.ParseUtils import ParseUtils
from utils_future import File, JSONFile, Log

log = Log("PDFSourceFileDataMixin")


class PDFSourceFileRawDataMixin:

    @property
    def raw_data_path(self):
        return os.path.join(self.dir_data, "raw_data.json")

    @property
    def errors_path(self):
        return os.path.join(self.dir_data, "errors.json")

    def extract_fields(self, lines):
        fields = None
        i_total = None
        i_line = None

        for i_line, line in enumerate(lines[:10]):
            line = line.replace("\u2010", "-").replace("\xa0", " ")
            tokens = line.split("\t")

            if tokens[:3] == ["", "number", "Total"]:
                fields = tokens[3:]
                i_total = 2

            if tokens[:2] == ["District, DS division and GN division", ""]:
                fields = tokens[3:]
                i_total = 2

            if fields:
                non_empty_fields = [field for field in fields if field]
                if non_empty_fields:
                    break

        if not fields:
            raise ValueError("Could not find fields in the first 10 lines.")

        return fields, i_total, i_line

    @staticmethod
    def _extract_line(line, fields, i_total):
        line = (
            line.replace("\u2010", "-")
            .replace("\xa0", " ")
            .replace("\u00a0", " ")
        )
        tokens = line.split("\t")
        n_tokens = len(tokens)
        if n_tokens < 1 + len(fields):
            return None
        if not tokens[0]:
            return None
        region_name_and_num = " ".join(tokens[0:(i_total)])
        words = region_name_and_num.split(" ")
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
        region_name = region_name.strip()
        if not region_name:
            raise ValueError(f"Region name is empty ({region_name_and_num=})")

        total_value_from_source = ParseUtils.parse_int(tokens[i_total])
        n_fields = len(fields)
        values_only = [
            ParseUtils.parse_int(token) for token in tokens[-n_fields:]
        ]

        values = dict(zip(fields, values_only))
        total_value = sum(values_only)
        d = dict(
            region_name=region_name,
            gnd_num=gnd_num,
            total_value_from_source=total_value_from_source,
            total_value=total_value,
            values=values,
        )
        return d

    def _dedupe_lines(self, lines):
        seen = set()
        deduped_lines = []
        for line in lines:
            if line not in seen:
                deduped_lines.append(line)
                seen.add(line)
        return deduped_lines

    def build_raw_data(self):
        raw_data_file = JSONFile(self.raw_data_path)
        if raw_data_file.exists:
            log.debug(f"{raw_data_file} exists.")
            return

        lines = File(self.txt_path).read_lines()
        lines = self._dedupe_lines(lines)

        fields, i_total, offset = self.extract_fields(lines)
        log.debug(f"{fields=}")
        errors = []
        d_list = []
        for line in lines[offset + 1:]:
            d = self._extract_line(line, fields, i_total)
            if d:
                d_list.append(d)

        if errors:
            errors_file = JSONFile(self.errors_path)
            errors_file.write(errors)
            log.warning(f"Wrote {len(errors)} errors to {errors_file}.")

        raw_data_file.write(d_list)
        log.info(f"Wrote {len(d_list)} rows to {raw_data_file}.")

    def read_raw_data_list(self):
        raw_data_file = JSONFile(self.raw_data_path)
        return raw_data_file.read()
