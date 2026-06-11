from gig_future import Ent, EntType
from utils_future import Log

log = Log("PDFSourceFileValidateMixin")


class PDFSourceFileValidateMixin:
    @classmethod
    def validate_totals(cls, data_idx, parent_ent_type, child_ent_type):
        parent_ents = Ent.list_from_type(parent_ent_type)
        child_ents = Ent.list_from_type(child_ent_type)

        n_parents = len(parent_ents)
        n_parents_with_mismatch = 0
        for parent_ent in parent_ents:
            parent_data = data_idx.get(parent_ent.id)
            if not parent_data:
                continue
            parent_values = parent_data["values"]

            child_ents_for_parent_ent = [
                child_ent
                for child_ent in child_ents
                if parent_ent.id in child_ent.id
            ]

            sum_child_values = {}
            for child_ent in child_ents_for_parent_ent:
                child_data = data_idx.get(child_ent.id)
                if not child_data:
                    continue
                child_values = child_data["values"]
                for k, v in child_values.items():
                    sum_child_values[k] = sum_child_values.get(k, 0) + v

            if sum_child_values != parent_values:
                log.warning(f"⚠️ Values mismatch for {parent_ent.id} ")
                n_parents_with_mismatch += 1

        if n_parents_with_mismatch > 0:
            log.warning(
                f"⚠️ {parent_ent_type.name} > {child_ent_type.name}:"
                + f"  {n_parents_with_mismatch}/{n_parents} mismatches."
            )
        else:
            log.info(
                f"✅ {parent_ent_type.name} > {child_ent_type.name}:"
                + f" All {n_parents} totals match."
            )

    @classmethod
    def validate_ent_coverage(
        cls,
        ent_type,
        data_list,
    ):
        ents = Ent.list_from_type(ent_type)
        ent_ids = set(ent.id for ent in ents)

        missing_ent_ids = ent_ids - data_list
        if missing_ent_ids:
            log.warning(
                f"⚠️ {ent_type.name}: {len(missing_ent_ids)} IDs missing."
            )
            if len(missing_ent_ids) <= 10:
                log.warning(f"\t{', '.join(missing_ent_ids)}")
            else:
                log.warning(f"\t{', '.join(list(missing_ent_ids)[:10])}...")

        else:
            log.info(f"✅ {ent_type.name}: All {len(ent_ids)} IDs covered.")

    def validate_data(self):
        log.info(f"Validated data for {self.doc_id}.")
        data_list = self.read_data_list()
        ids_with_data = set([data["region_id"] for data in data_list])
        for ent_type in [
            EntType.COUNTRY,
            EntType.DISTRICT,
            EntType.DSD,
            EntType.GND,
        ]:
            self.validate_ent_coverage(ent_type, ids_with_data)

        # data_idx = {data["region_id"]: data for data in data_list}
        # for parent_ent_type, child_ent_type in [
        #     (EntType.COUNTRY, EntType.DISTRICT),
        #     (EntType.DISTRICT, EntType.DSD),
        #     (EntType.DSD, EntType.GND),
        # ]:
        #     self.validate_totals(data_idx, parent_ent_type, child_ent_type)
