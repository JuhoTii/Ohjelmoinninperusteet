
# Copyright (c) 2025 Juho Tiihonen
# License: MIT

"""CSV-lukufunktio vuoden 2025 tuntidatalle (Viikko6).

Lukee 2025.csv ja palauttaa rivit sanakirjoina.
Avaimet normalisoidaan: strip + lower (esim. 'Aika' -> 'aika').
Olettaa erotinmerkin ';' ja UTF-8-koodauksen.
"""

import csv
from typing import List, Dict


def lataa_vuosi(polku: str = "2025.csv") -> List[Dict[str, str]]:
    """Lukee CSV-tiedoston ja palauttaa rivit sanakirjalistana.

    Parametrit:
        polku: CSV-tiedoston polku (oletus "2025.csv").
    Palauttaa:
        Lista sanakirjoja, joissa avaimet ovat pienaakkosilla.
    """
    with open(polku, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        rivit: List[Dict[str, str]] = []
        for r in reader:
            norm = { (k or "").strip().lower(): (v or "").strip() for k, v in r.items() }
            # Yhteensopivuus: jos sarake on 'keskilampotila', mapataan 'keskilämpötila':an
            if "keskilampotila" in norm and "keskilämpötila" not in norm:
                norm["keskilämpötila"] = norm.pop("keskilampotila")
            rivit.append(norm)
        return rivit
