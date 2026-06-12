import os

from census.pdf_source_file.ParseUtils import ParseUtils
from utils_future import File, JSONFile, Log

log = Log("PDFSourceFileDataMixin")


class PDFSourceFileRawDataMixin:
    MAX_LINES_TO_PROCESS = None

    @property
    def raw_data_path(self):
        return os.path.join(self.dir_data, "raw_data.json")

    @property
    def errors_path(self):
        return os.path.join(self.dir_data, "errors.json")

    @staticmethod
    def _is_gnd_num(word):
        n_word = len(word)
        has_digit = any(c.isdigit() for c in word)
        has_slash = "/" in word
        return has_digit and (n_word <= 5 or (has_slash and n_word <= 7))

    def _extract_gnd_num(self, region_name_and_num):

        if self.has_gnd_num:
            words = region_name_and_num.split(" ")
            if (
                len(words) >= 2
                and len(words[-1]) <= 2
                and words[-2].isnumeric()
            ):
                words = words[:-2] + [words[-2] + "" + words[-1]]

            last_word = words[-1]
            if self._is_gnd_num(last_word):
                region_name = " ".join(words[:-1])
                return region_name, last_word

        return region_name_and_num, None

    def _extract_line(self, line, fields):
        line = (
            line.replace("\u2010", "-")
            .replace("\xa0", " ")
            .replace("\u00a0", " ")
        )
        tokens = line.split(self.DELIM_TXT)
        tokens = [token.strip() for token in tokens if token.strip()]

        n_tokens = len(tokens)
        if n_tokens < 1 + len(fields):
            return None
        if not tokens[0]:
            return None
        i_fields_start = n_tokens - len(fields)
        region_name_and_num = " ".join(tokens[0 : i_fields_start - 1]).strip()
        print(f"{region_name_and_num=}")

        region_name, gnd_num = self._extract_gnd_num(region_name_and_num)
        print(f"{region_name=}, {gnd_num=}")

        if not region_name:
            raise ValueError(f"Region name is empty ({region_name_and_num=})")

        n_fields = len(fields)
        total_value_from_source = ParseUtils.parse_int(tokens[-n_fields])
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

        errors = []
        d_list = []
        has_found_sl = False
        for line in (
            lines[: self.MAX_LINES_TO_PROCESS]
            if self.MAX_LINES_TO_PROCESS
            else lines
        ):
            if not has_found_sl:
                if "Sri" in line:
                    has_found_sl = True
                else:
                    continue
            d = self._extract_line(line, self.fields)
            if d:
                d_list.append(d)

        if errors:
            errors_file = JSONFile(self.errors_path)
            errors_file.write(errors)
            log.warning(f"Wrote {len(errors)} errors to {errors_file}.")

        if len(d_list) == 0:
            raise ValueError("No valid data extracted from lines.")

        raw_data_file.write(d_list)
        log.info(f"Wrote {len(d_list)} rows to {raw_data_file}.")

    def read_raw_data_list(self):
        raw_data_file = JSONFile(self.raw_data_path)
        return raw_data_file.read()
