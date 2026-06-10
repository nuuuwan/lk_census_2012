import os

from gig_future import Ent, EntType
from utils_future import File, JSONFile, Log

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
        if last_word[0].isdigit():
            gnd_num = last_word
            region_name = " ".join(words[:-1])
        else:
            gnd_num = None
            region_name = region_name_and_num

        total_value_from_source = ParseUtils.parse_int(tokens[i_field_start])
        values_only = [
            ParseUtils.parse_int(token)
            for token in tokens[i_field_start + 1:]
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

    @staticmethod
    def expand_data(data_list):
        previous_ent_type = None
        previous_ent_id = None
        new_data_list = []
        for data in data_list[:1000]:
            region_name = data["region_name"]
            print(region_name)
            if previous_ent_type is not None and region_name == "Sri Lnka":
                continue

            if previous_ent_type is None:
                filter_ent_type_and_id_list = [(EntType.COUNTRY, "LK")]
            elif previous_ent_type == EntType.COUNTRY:
                filter_ent_type_and_id_list = [
                    (EntType.DISTRICT, previous_ent_id)
                ]
            elif previous_ent_type == EntType.DISTRICT:
                filter_ent_type_and_id_list = [(EntType.DSD, previous_ent_id)]
            elif previous_ent_type == EntType.DSD:
                filter_ent_type_and_id_list = [(EntType.GND, previous_ent_id)]
            elif previous_ent_type == EntType.GND:
                if data["gnd_num"] is None:
                    filter_ent_type_and_id_list = [
                        (EntType.GND, previous_ent_id[:7]),
                        (EntType.DSD, previous_ent_id[:5]),
                        (EntType.DISTRICT, previous_ent_id[:2]),
                    ]
                else:
                    filter_ent_type_and_id_list = [
                        (EntType.GND, previous_ent_id[:7])
                    ]
            else:
                raise ValueError(
                    f"Unexpected previous_ent_type: {previous_ent_type}"
                )

            ents = Ent.list_from_name_fuzzy(
                region_name,
                filter_ent_type_and_id_list=filter_ent_type_and_id_list,
                limit=5,
                min_fuzz_ratio=90,
            )
            if len(ents) == 0:
                raise ValueError(f"No matching ent found for: {region_name}")

            if len(ents) > 1:
                log.warning(f"Multiple matching ents for: {region_name}")

            ent = ents[0]
            new_data = dict(
                region_id=ent.id,
                region_name=ent.name,
                total_value=data["total_value"],
                values=data["values"],
                total_value_from_source=data["total_value_from_source"],
            )
            previous_ent_type = EntType.from_id(ent.id)
            previous_ent_id = ent.id
            new_data_list.append(new_data)

        return new_data_list

    def build_data(self):
        lines = File(self.txt_path).read_lines()
        fields = self.extract_fields()
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

        d_list = self.expand_data(d_list)
        data_file = JSONFile(self.data_path)
        data_file.write(d_list)
        log.info(f"Wrote {len(d_list)} rows to {data_file}.")
