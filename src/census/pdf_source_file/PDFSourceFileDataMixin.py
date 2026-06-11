import os

from census.pdf_source_file.ParseUtils import ParseUtils
from census.pdf_source_file.PDFSourceFileDataExpandMixin import \
    PDFSourceFileDataExpandMixin
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
        for i_line, line in enumerate(lines):
            line = line.replace("\u2010", "-")
            tokens = line.split()
            if tokens[:2] == ["number", "Total"]:
                fields = tokens[2:]
                return fields, i_line

            if tokens[:6] == [
                "District,",
                "DS",
                "division",
                "and",
                "GN",
                "division",
            ]:
                fields = ["Both sexes", "Male", "Female"]
                return fields, i_line

        raise ValueError("Fields not found in the text file.")

    @staticmethod
    def _extract_line(line, fields):
        line = line.replace("\u2010", "-")
        tokens = line.split()
        print(tokens)
        n_tokens = len(tokens)
        if n_tokens < 1 + len(fields):
            return None
        i_field_start = n_tokens - len(fields)
        print(f"{i_field_start=}")
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

        values_only = [
            ParseUtils.parse_int(token) for token in tokens[i_field_start:]
        ]
        if len(values_only) != len(fields):
            raise ValueError(
                f"Expected {len(fields)} values but found {len(values_only)}"
            )

        values = dict(zip(fields, values_only))
        total_value = sum(values_only)
        d = dict(
            region_name=region_name,
            gnd_num=gnd_num,
            values=values,
            total_value=total_value,
        )
        log.debug(d)
        return d

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

        fields, offset = self.extract_fields(lines)
        log.debug(f"{fields=}")
        errors = []
        d_list = []
        for line in lines[offset + 1:]:
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

    def read_data_list(self):
        data_file = JSONFile(self.data_path)
        return data_file.read()
