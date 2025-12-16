"""Kirjoitusfunktio raportin viemiseen tekstitiedostoon."""
from typing import List

def kirjoita_raportti(rivit: List[str], polku: str = "raportti.txt") -> None:
    """Kirjoittaa annetut rivit tekstitiedostoon UTF-8-koodauksella."""
    with open(polku, "w", encoding="utf-8") as f:
        for r in rivit:
            f.write(r + "\n")






