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
        "Hebbekanda": "Hambakanda",  # after LK-2315080
        "Halvitigala Step 2": "Halvitigala Colony 2",  # after LK-3118075
        "Wellabada - Thiranagama": "Thiranagama Wellabada",  # after LK-3136085
        "Ihala Muruthawela": "Muruthawela Ihala",  # after LK-3325160
        "Ihala Walasmulla": "Walasmulla Ihala",  # after LK-3325215
        "Pahala Walasmulla": "Walasmulla Pahala",  # after LK-3325215
        "Pahala Yatigala": "Yatigala Pahala",  # after LK-3327125
        "Nanaddan": "Nanattan",  # after LK-4212090
        "Thadduvankoddy": "Thattuwankotty",  # after LK-4506055
        "Chemmann Odai": "Semmanodai",  # after LK-5104040
        "UthuchchenaiOothuchenai": "Uthuchchenai",  # after LK-5110015
        #
        "Si(cid:425)andy 1Si(cid:425)andy 1": "Sittandy 1",  # after LK-5112015
        "Mayilavaddavan": "Mylavedduvan",  # after LK-5112075
        "Kommathurai EastKommathurai": "Kommathurai East",  # after LK-5112090
        "Gnasooriyam Sathukam": "Gnanasooriyam Square",  # after LK-5118110
        "Araipattai 03": "Arayampathy 3",  # after LK-5127075
        "Araipattai South": "Arayampathy South",  # after LK-5127085
        "Araipattai Central": "Arayampathy Central",  # after LK-5127095
        "Araipattai 02": "Arayampathy 02",  # after LK-5127095
        #
        "Vankalai North": "Vankalai North",  # after LK-4209085
        "Vankalai West": "Vankalai West",  # after LK-4209085
        "Vankalai East": "Vankalai East",  # after LK-4209085
        "Thomaspuri": "Thomaspuri",  # after LK-4209085
        "Naruvilikkulam": "Naruvilikkulam",  # after LK-4209085
        "Vanchiankulam": "Vanchiankulam",  # after LK-4209085
        "Ilahadipiddy": "Ilahadipiddy",  # after LK-4209085
        "Ilanthamoddai": "Ilanthamoddai",  # after LK-4209085
        "Periyakaddaikadu": "Periyakaddaikadu",  # after LK-4209085
        #
        "Aththikkuli": "Aththikkuli",  # after LK-4209085
        "Kanchithalvu": "Kanchithalvu",  # after LK-4209085
        "Chemmantheevu": "Chemmantheevu",  # after LK-4209085
        "Murunkan": "Murunkan",  # after LK-4209085
        "Cheddiyar Mahankaddai Adampan": "Cheddiyar Mahankaddai Adampan",  # after LK-4209085
        "Iraddaikkulam": "Iraddaikkulam",  # after LK-4209085
        "Chundikkuli": "Chundikkuli",  # after LK-4209085
        "Puttirarkandan": "Puttirarkandan",  # after LK-4209085
        "Razoolputhuveli": "Razoolputhuveli",  # after LK-4209085
        "Nanattan": "Nanattan",  # after LK-4209085
        "Umanagari": "Umanagari",  # after LK-4209085
        #
        "Araipattai East": "Arayampathy East",  # after LK-5127115
        "Araipattai North": "Arayampathy North",  # after LK-5127115
        "Araipattai 01": "Arayampathy 01",  # after LK-5127115
        "Araipattai West": "Arayampathy West",  # after LK-5127115
        "Sammanthurai Tamil Division 01": "Sammanthurai TD 01",  # after LK-5218015
        "Sammanthurai Tamil Division 04": "Sammanthurai TD 04",  # after LK-5218015
        "Sammanthurai Tamil Division 02": "Sammanthurai TD 02",  # after LK-5218015
        "Sammanthurai Tamil Division 03": "Sammanthurai TD 03",  # after LK-5218085
        "Kalmunai Tamil Division (Sub Division)": "Kalmunai North",  # after LK-5218255
        #
        "Maruthamunai 01": "Maruthamunai 01",  # after LK-5224
        "Maruthamunai 02": "Maruthamunai 02",  # after LK-5224
        "Maruthamunai 03": "Maruthamunai 03",  # after LK-5224
        "Maruthamunai 04": "Maruthamunai 04",  # after LK-5224
        "Maruthamunai 05": "Maruthamunai 05",  # after LK-5224
        "Maruthamunai 06": "Maruthamunai 06",  # after LK-5224
        "Islamabad & Kalmunai Town": "Islamabad & Kalmunai Town",  # after LK-5224090
    }

    DSD_RENAME_MAP = {
        "Kandy Four Gravets & Gangawata Korale": "Gangawata Korale",
        "Ambanganga Korale": "Ambanganga",
        "Laggala-Pallegama": "Laggala",
        "Pathameny": "Pattameni",
        "Attiaddy": "Aththiyadi",
        "Nallur Irajathani": "Nallur Rajathani",
        "Kiralessa": "Kandalama",
        "Sirambiady": "Chirampiyadi",
        "South Bar": "Southbar",
        #
        "Ellainagar": "Eravur Town",  # after LK-5115
    }
