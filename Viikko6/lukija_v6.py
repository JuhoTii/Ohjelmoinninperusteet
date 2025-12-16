
# Copyright (c) 2025 Juho Tiihonen
# License: MIT

"""CSV-lukufunktio vuoden 2025 tuntidatalle (Viikko6).

Lukee 2025.csv ja palauttaa rivit sanakirjoina.
Avaimet normalisoidaan ja mapataan kanonisiin: aika, kulutus, tuotanto, keskilämpötila.
Olettaa erotinmerkin ';' ja UTF-8-koodauksen.
"""

import csv
from typing import List, Dict


def _normalize_key(k: str) -> str:
    """Mapataan CSV-otsikot kanonisiin avaimiin."""
    s = (k or "").strip().lower()

    aliases = {
        # aika
        "aika": "aika",
        "timestamp": "aika",
        "datetime": "aika",

        # kulutus
        "kulutus": "kulutus",
        "kulutus (netotettu) kwh": "kulutus",
        "kulutus (kwh)": "kulutus",
        "nettokulutus": "kulutus",

        # tuotanto
        "tuotanto": "tuotanto",
        "tuotanto (netotettu) kwh": "tuotanto",
        "tuotanto (kwh)": "tuotanto",
        "nettotuotanto": "tuotanto",

        # lämpötila
        "keskilämpötila": "keskilämpötila",
        "keskilampotila": "keskilämpötila",
        "vuorokauden keskilämpötila": "keskilämpötila",
        "vuorokauden keskilampotila": "keskilämpötila",
        "lämpötila": "keskilämpötila",
        "lampotila": "keskilämpötila",
    }

    if s in aliases:
        return aliases[s]


    if "kulutus" in s:
        return "kulutus"
    if "tuotanto" in s:
        return "tuotanto"
    if ("lämpö" in s) or ("lampo" in s) or ("keskilämpö" in s) or ("keskilampo" in s):
        return "keskilämpötila"
    return s


def lataa_vuosi(polku: str = "2025.csv") -> List[Dict[str, str]]:
    """Lukee CSV-tiedoston ja palauttaa rivit sanakirjalistana (avaimet kanonisoitu)."""
    with open(polku, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        rivit: List[Dict[str, str]] = []
        for r in reader:
            # HUOM: käytä r.items() ja append vain kerran
            norm = {_normalize_key(k): (v or "").strip() for k, v in r.items()}
            rivit.append(norm)
    return rivit
