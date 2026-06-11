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


DSD_UPDATE_MAP = [
    dict(
        id="LK-2303",
        current_ids=["LK-2302", "LK-2303"],
        name="Kothmale",
        current_names=["Kothmale East", "Kothmale West"],
        year_last_modified="2019",
    ),  # Kothmale → Kothmale East + Kothmale West
    dict(
        id="LK-2306",
        current_ids=["LK-2306", "LK-2307"],
        current_names=["Hanguranketha", "Mathurata"],
        year_last_modified="2019",
    ),  # Hanguranketha → Hanguranketha + Mathurata
    dict(
        id="LK-2309",
        current_ids=["LK-2309", "LK-2310"],
        current_names=["Walapane", "Niladandahinna"],
        year_last_modified="2019",
    ),  # Walapane → Walapane + Niladandahinna
    dict(
        id="LK-2312",
        current_ids=["LK-2312", "LK-2313"],
        current_names=["Nuwara-Eliya", "Thalawakelle"],
        year_last_modified="2019",
    ),  # Nuwara-Eliya → Nuwara-Eliya + Thalawakelle
    dict(
        id="LK-2315",
        current_ids=["LK-2314", "LK-2315"],
        name="Ambagamuwa",
        current_names=["Ambagamuwa Korale", "Norwood"],
        year_last_modified="2019",
    ),  # Ambagamuwa → Ambagamuwa Korale + Norwood
    dict(
        id="LK-3136",
        current_ids=["LK-3135", "LK-3136", "LK-3137"],
        current_names=["Hikkaduwa", "Rathgama", "Madampagama"],
        year_last_modified="2019",
    ),  # Hikkaduwa → Hikkaduwa + Rathgama + Madampagama
    dict(
        id="LK-3127",
        current_ids=["LK-3127", "LK-3128"],
        current_names=["Baddegama", "Wanduramba"],
        year_last_modified="2019",
    ),  # Baddegama → Baddegama + Wanduramba
    dict(
        id="LK-9118",
        current_ids=["LK-9118", "LK-9119"],
        current_names=["Balangoda", "Kaltota"],
        year_last_modified="2019",
    ),  # Balangoda → Balangoda + Kaltota
]


class PDFSourceFileDataMixin:

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
        idx = {
            "Kandy Four Gravets & Gangawata Korale": "Gangawata Korale",
            "Ambanganga Korale": "Ambanganga",
            "Laggala-Pallegama": "Laggala",
            "Pathameny": "Pattameni",
            "Attiaddy": "Aththiyadi",
            "Nallur Irajathani": "Nallur Rajathani",
        }
        for item in DSD_UPDATE_MAP:
            name = item.get("name")
            current_names = item.get("current_names", [])
            if name:
                idx[name] = current_names[0]
        return idx.get(region_name, region_name)

    @staticmethod
    def _expand_data_list(data_list):
        n_data_list = len(data_list)
        log.info(f"Expanding data {n_data_list} rows")
        previous_ent_type = None
        previous_ent_id = None
        new_data_list = []
        no_ent_list = []
        for data in data_list:
            region_name = data["region_name"]
            region_name = PDFSourceFileDataMixin._remap_region_name(
                region_name
            )

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

            # Correct for Pre-2019 DSD Data
            id_list = [
                ent_id for ent_type, ent_id in filter_ent_type_and_id_list
            ]
            for item in DSD_UPDATE_MAP:
                current_ids = item["current_ids"]
                if set(id_list) & set(current_ids):
                    for current_id in current_ids:
                        filter_ent_type_and_id_list.append(
                            (EntType.GND, current_id)
                        )

            ents = Ent.list_from_name_fuzzy(
                region_name,
                filter_ent_type_and_id_list=filter_ent_type_and_id_list,
                limit=1,
                min_fuzz_ratio=80,
            )

            if len(ents) == 0:
                log.error(f"No match: {region_name} ({previous_ent_id=})")
                no_ent_list.append(data)
                if len(no_ent_list) > 10:
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
