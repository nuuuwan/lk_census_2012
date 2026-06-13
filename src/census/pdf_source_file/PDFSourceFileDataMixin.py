import os

from tqdm import tqdm

from census.pdf_source_file.Corrections import Corrections
from gig_future import Ent, EntType
from utils_future import JSONFile, Log

log = Log("PDFSourceFileDataExpandMixin")


class PDFSourceFileDataMixin:
    MAX_NO_ENT_LIST = 10
    MIN_DATA_LIST_SIZE = 30

    @classmethod
    def _remap_region_name(cls, region_name):
        idx = Corrections.GND_RENAME_MAP | Corrections.DSD_RENAME_MAP
        for item in Corrections.DSD_UPDATE_MAP:
            name = item.get("name")
            current_names = item.get("current_names", [])
            if name:
                idx[name] = current_names[0]
        return idx.get(region_name, region_name)

    # flake8: noqa: C901
    @classmethod
    def get_filter_ent_type_and_id_list(
        cls,
        previous_ent_type,
        previous_ent_id,
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
            return [
                (EntType.GND, previous_ent_id[:7]),
                (EntType.DSD, previous_ent_id[:5]),
                (EntType.DISTRICT, previous_ent_id[:2]),
            ]

        raise ValueError(f"Unexpected previous_ent_type: {previous_ent_type}")

    @classmethod
    def _expand_data(
        cls, previous_ent_type, previous_ent_id, data, no_ent_list
    ):
        filter_ent_type_and_id_list = cls.get_filter_ent_type_and_id_list(
            previous_ent_type,
            previous_ent_id,
        )

        # Correct for Pre-2019 DSD Data
        id_list = [ent_id for ent_type, ent_id in filter_ent_type_and_id_list]
        for item in Corrections.DSD_UPDATE_MAP:
            current_ids = item["current_ids"]
            if set(id_list) & set(current_ids):
                for current_id in current_ids:
                    filter_ent_type_and_id_list.append(
                        (EntType.GND, current_id)
                    )
        if "LK-6148" in id_list:
            filter_ent_type_and_id_list.append((EntType.GND, "LK-6145"))
        if "LK-6145" in id_list:
            filter_ent_type_and_id_list.append((EntType.GND, "LK-6148"))

        region_name = data["region_name"]
        alt_region_name = cls._remap_region_name(region_name)

        ents = Ent.list_from_name_fuzzy(
            [region_name, alt_region_name],
            filter_ent_type_and_id_list=filter_ent_type_and_id_list,
            limit=1,
            min_fuzz_ratio=80,
        )

        if len(ents) == 0:
            log.error(f'No match: "{region_name}" ({previous_ent_id=})')
            no_ent_list.append((region_name, previous_ent_id))
            if len(no_ent_list) > cls.MAX_NO_ENT_LIST:
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

            return None

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

        return new_data, previous_ent_type, previous_ent_id, data, no_ent_list

    @classmethod
    def _expand_data_list(cls, data_list):
        n_data_list = len(data_list)
        log.info(f"Expanding data {n_data_list} rows")
        previous_ent_type = None
        previous_ent_id = None
        new_data_list = []
        no_ent_list = []
        for data in tqdm(data_list, desc="Expanding data"):
            output = cls._expand_data(
                previous_ent_type,
                previous_ent_id,
                data,
                no_ent_list,
            )
            if output is None:
                continue
            (
                new_data,
                previous_ent_type,
                previous_ent_id,
                data,
                no_ent_list,
            ) = output
            new_data_list.append(new_data)

        if no_ent_list:
            log.error(f"🛑 {len(no_ent_list)} entries had no matching ent.")
            print("\t{")
            print("\t\t#")
            for region_name, previous_ent_id in no_ent_list:
                print(
                    f'\t\t"{region_name}":"{region_name}",'
                    + f"  # after {previous_ent_id}"
                )
            print("\t\t#")
            print("\t}")

        log.info(
            f"Expanded data list from {len(data_list)}"
            + f" to {len(new_data_list)} entries."
        )
        return new_data_list

    @property
    def data_path(self):
        return os.path.join(self.dir_data, "data.json")

    def build_data(self):
        data_file = JSONFile(self.data_path)
        if data_file.exists:
            log.debug(f"{data_file} exists.")
            return
        raw_data_list = self.read_raw_data_list()
        data_list = self._expand_data_list(raw_data_list)
        data_file.write(data_list)
        log.info(f"Wrote {len(data_list)} rows to {data_file}.")

    def read_data_list(self):
        data_file = JSONFile(self.data_path)
        data_list = data_file.read()
        n_data_list = len(data_list)
        if len(data_list) < self.MIN_DATA_LIST_SIZE:
            raise ValueError(
                f"Data list size {n_data_list} < {self.MIN_DATA_LIST_SIZE}"
            )
        log.info(f"Read {n_data_list:,} rows from {data_file}.")
        return data_list
