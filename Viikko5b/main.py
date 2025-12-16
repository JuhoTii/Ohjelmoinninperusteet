# Copyright (c) 2025 Juho Tiihonen
# License: MIT


"""Pääohjelma, joka käyttää muita moduuleja CSV-tiedostojen lukemiseen,"""

from luefunktio import lue_csvt
from muunnafunktio import muunna_data, muodosta_raporttirivit
from kirjoitafunktio import kirjoita_raportti


def main() -> None:
    """Lukee CSV-tiedostot, muuntaa datan ja kirjoittaa raportin."""
    tiedostot = ["viikko41.csv", "viikko42.csv", "viikko43.csv"]

    datat = lue_csvt(tiedostot)
    paivat = muunna_data(datat)
    rivit = muodosta_raporttirivit(paivat)
    kirjoita_raportti(rivit, "raportti.txt")
    print("Valmis: raportti.txt luotu.")


if __name__ == "__main__":
    main()
