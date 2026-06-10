import os

from utils import File, JSONFile, Log

log = Log("PDFSourceFileDataMixin")


class ParseUtils:

    @staticmethod
    def parse_int(x):
        x = str(x)
        x = x.replace(",", "")
        return int(x)


class PDFSourceFileDataMixin:

    @property
    def data_path(self):
        return os.path.join(self.dir_data, "data.json")

    @property
    def errors_path(self):
        return os.path.join(self.dir_data, "errors.json")

    def extract_fields(self):
        lines = File(self.txt_path).read_lines()
        fields = []
        for line in lines:
            line = line.replace("\u2010", "-")
            tokens = line.split()
            if tokens[:2] == ["number", "Total"]:
                fields = tokens[2:]
                return fields
        raise ValueError("Fields not found in the text file.")

    def _extract_line(self, line, fields):
        line = line.replace("\u2010", "-")
        tokens = line.split()
        n_tokens = len(tokens)
        if n_tokens < 10:
            return None
        if tokens[:2] == ["number", "Total"]:
            return None
        i_field_start = n_tokens - len(fields) + 1
        region_name = " ".join(tokens[0:(i_field_start)])
        total_value_from_source = ParseUtils.parse_int(tokens[i_field_start])
        values_only = [
            ParseUtils.parse_int(token)
            for token in tokens[i_field_start + 1:]
        ]
        values = dict(zip(fields, values_only))
        total_value = sum(values_only)
        return dict(
            region_name=region_name,
            values=values,
            total_value=total_value,
            total_value_from_source=total_value_from_source,
        )

    def extract_data(self):
        lines = File(self.txt_path).read_lines()
        fields = self.extract_fields()
        errors = []
        d_list = []
        for line in lines:
            d = self._extract_line(line, fields)
            if d:
                d_list.append(d)

        data_file = JSONFile(self.data_path)
        data_file.write(d_list)
        log.info(f"Wrote {len(d_list)} rows to {data_file}.")
        if errors:
            errors_file = JSONFile(self.errors_path)
            errors_file.write(errors)
            log.warning(f"Wrote {len(errors)} errors to {errors_file}.")
