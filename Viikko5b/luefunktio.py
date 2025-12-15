

import csv
from typing import List, Dict

def lue_csv(tiedosto: str) -> List[Dict[str, str]]:
    with open(tiedosto, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))

def lue_csvt(tiedostot: List[str]) -> List[Dict[str, str]]:
    yhdistetty: List[Dict[str, str]] = []
    for nimi in tiedostot:
        try:
            rivit = lue_csv(nimi)
            for r in rivit:
                r["Lähde"] = nimi
            yhdistetty.extend(rivit)
        except FileNotFoundError:
            print(f"VAROITUS: '{nimi}' ei löytynyt – ohitetaan.")
