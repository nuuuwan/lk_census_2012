import os

from census.pdf_source_file.Corrections import Corrections
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

    MAX_NO_ENT_LIST = 10

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

    @staticmethod
    def _remap_region_name(region_name):
        idx = Corrections.GND_RENAME_MAP | Corrections.DSD_RENAME_MAP
        for item in Corrections.DSD_UPDATE_MAP:
            name = item.get("name")
            current_names = item.get("current_names", [])
            if name:
                idx[name] = current_names[0]
        return idx.get(region_name, region_name)

    # flake8: noqa: C901
    @staticmethod
    def get_filter_ent_type_and_id_list(
        previous_ent_type, previous_ent_id, gnd_num
    ):
        if previous_ent_type is None:
            return [(EntType.COUNTRY, "LK")]

        if previous_ent_type == EntType.COUNTRY:
            return [(EntType.DISTRICT, previous_ent_id)]

        if previous_ent_type == EntType.DISTRICT:
            return [(EntType.DSD, previous_ent_id)]

        if previous_ent_type == EntType.DSD:
            return [(EntType.GND, previous_ent_id)]

        if previous_ent_type == EntType.GND:
            if gnd_num is None:
                return [
                    (EntType.GND, previous_ent_id[:7]),
                    (EntType.DSD, previous_ent_id[:5]),
                    (EntType.DISTRICT, previous_ent_id[:2]),
                ]

            return [(EntType.GND, previous_ent_id[:7])]

        raise ValueError(f"Unexpected previous_ent_type: {previous_ent_type}")

    @staticmethod
    def _expand_data_list(data_list):
        n_data_list = len(data_list)
        log.info(f"Expanding data {n_data_list} rows")
        previous_ent_type = None
        previous_ent_id = None
        new_data_list = []
        no_ent_list = []
        for data in data_list:

            filter_ent_type_and_id_list = (
                PDFSourceFileDataMixin.get_filter_ent_type_and_id_list(
                    previous_ent_type, previous_ent_id, data.get("gnd_num")
                )
            )

            # Correct for Pre-2019 DSD Data
            id_list = [
                ent_id for ent_type, ent_id in filter_ent_type_and_id_list
            ]
            for item in Corrections.DSD_UPDATE_MAP:
                current_ids = item["current_ids"]
                if set(id_list) & set(current_ids):
                    for current_id in current_ids:
                        filter_ent_type_and_id_list.append(
                            (EntType.GND, current_id)
                        )
            if "LK-6148" in id_list:
                filter_ent_type_and_id_list.append((EntType.GND, "LK-6145"))

            region_name = data["region_name"]
            alt_region_name = PDFSourceFileDataMixin._remap_region_name(
                region_name
            )

            ents = Ent.list_from_name_fuzzy(
                [region_name, alt_region_name],
                filter_ent_type_and_id_list=filter_ent_type_and_id_list,
                limit=1,
                min_fuzz_ratio=80,
            )

            if len(ents) == 0:
                log.error(f"No match: {region_name} ({previous_ent_id=})")
                no_ent_list.append((region_name, previous_ent_id))
                if len(no_ent_list) > PDFSourceFileDataMixin.MAX_NO_ENT_LIST:
                    print("\t{")
                    print("\t\t#")
                    for region_name, previous_ent_id in no_ent_list:
                        print(
                            f'\t\t"{region_name}":"{region_name}",'
                            + f"  # after {previous_ent_id}"
                        )
                    print("\t\t#")
                    print("\t}")
                    raise ValueError("Too many entries with no matching ent.")

                continue

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
            n_completed = len(new_data_list)
            if previous_ent_type != EntType.GND:
                p_completed = n_completed / n_data_list
                log.debug(
                    f"{n_completed}/{n_data_list} - {p_completed:.1%}) {ent.id} {ent.name}"
                )

        if no_ent_list:
            log.error(f"🛑 {len(no_ent_list)} entries had no matching ent.")

        log.info(
            f"Expanded data list from {len(data_list)}"
            + f" to {len(new_data_list)} entries."
        )
        return new_data_list

    def _dedupe_lines(self, lines):
        seen = set()
        deduped_lines = []
        for line in lines:
            if line not in seen:
                deduped_lines.append(line)
                seen.add(line)
        return deduped_lines

    def build_data(self):
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
        data_file = JSONFile(self.data_path)
        data_file.write(d_list)
        log.info(f"Wrote {len(d_list)} rows to {data_file}.")
