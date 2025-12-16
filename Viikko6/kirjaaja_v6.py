# Copyright (c) 2025 Juho Tiihonen
# License: MIT

"""Raportin tallennus tiedostoon (Viikko6)."""

from typing import List

def tallenna_raportti(rivit: List[str], tiedosto: str = "raportti.txt") -> None:
    """Kirjoittaa raportin rivit tiedostoon UTF-8-koodauksella. """
    try:
        with open(tiedosto, "w", encoding="utf-8") as f:
            for rivi in rivit:
                f.write(rivi + "\n")
    except Exception as e:
        print(f"Virhe kirjoitettaessa tiedostoon {tiedosto}: {e}")
