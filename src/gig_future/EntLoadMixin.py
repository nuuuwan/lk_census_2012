from functools import cache

from rapidfuzz import fuzz

from gig_future.EntType import EntType
from utils_future import Log, String

log = Log("EntLoadMixin")


class EntLoadMixin:

    @classmethod
    def from_dict(cls, d):
        d = d.copy()

        for k in ["area_sqkm", "center_lat", "center_lng"]:
            if k in d:
                d[k] = String(d[k]).float if d[k] else 0

        return cls(d)

    @classmethod
    def from_id(cls, id: str):
        ent_type = EntType.from_id(id)
        ent_idx = cls.idx_from_type(ent_type)
        return ent_idx[id]

    @classmethod
    def list_from_type(cls, ent_type: EntType) -> list:
        d_list = ent_type.remote_data_list
        ent_list = [cls.from_dict(d) for d in d_list]
        return ent_list

    @classmethod
    def idx_from_type(cls, ent_type: EntType) -> dict:
        ent_list = cls.list_from_type(ent_type)
        ent_idx = {ent.id: ent for ent in ent_list}
        return ent_idx

    @classmethod
    def list_from_id_list(cls, id_list: list) -> list:
        ent_list = [cls.from_id(id) for id in id_list]
        return ent_list

    @classmethod
    def ids_from_type(cls, ent_type: EntType) -> list:
        ent_list = cls.list_from_type(ent_type)
        id_list = [ent.id for ent in ent_list]
        return id_list

    @staticmethod
    @cache
    def clean_name(x):
        x = x.replace("-", " ")
        x = x.split("(")[0]
        x = x.strip()
        x = x.lower()
        n = len(x)
        n2 = n // 2
        if x[:n2] == x[n2:]:
            x = x[:n2]
        return x

    # flake8: noqa: C901
    @classmethod
    def list_from_name_fuzzy(
        cls,
        fuzzy_name_list: list[str],
        filter_ent_type_and_id_list: list[tuple[EntType, str]],
        limit: int,
        min_fuzz_ratio: int,
    ) -> list:

        ent_and_ratio_list = []
        for entity_type, filter_parent_id in filter_ent_type_and_id_list:
            for ent in cls.list_from_type(entity_type):
                if filter_parent_id and not ent.is_parent_id(
                    filter_parent_id
                ):
                    continue
                for fuzzy_name in fuzzy_name_list:
                    for ent_name in [ent.name] + ent.other_name_list:
                        fuzz_ratio = fuzz.ratio(
                            cls.clean_name(ent_name),
                            cls.clean_name(fuzzy_name),
                        )
                        ent_and_ratio_list.append([ent, fuzz_ratio])

        return [
            item[0]
            for item in sorted(ent_and_ratio_list, key=lambda x: -x[1])
            if item[1] >= min_fuzz_ratio
        ][:limit]
