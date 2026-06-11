class Corrections:

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
    GND_RENAME_MAP = {
        "Nanaddan": "Nanattan",  # after LK-4212090
        "UthuchchenaiOothuchenai": "Uthuchchenai",  # after LK-5110015
        "Si(cid:425)andy 1Si(cid:425)andy 1": "Sittandy 1",  # after LK-5112015
        "Kommathurai EastKommathurai": "Kommathurai East",  # after LK-5112090
    }

    DSD_RENAME_MAP = {
        "Ellainagar": "Eravur Town",
        "Kalmunai Tamil Division (Sub Division)": "Kalmunai North",
    }
