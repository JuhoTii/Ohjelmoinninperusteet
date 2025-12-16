
# Copyright (c) 2025 Juho Tiihonen
# License: MIT

"""Pääohjelma (Viikko6): lukee 2025.csv antaa käyttöliittymän."""

from datetime import datetime, date
from typing import List
import sys
from lukija_v6 import lataa_vuosi
from laskenta_v6 import muodosta_paivat, muodosta_kuukaudet, muodosta_vuosi
from raportti_v6 import raportti_paivavalilta, raportti_kuukausi, raportti_vuosi
from kirjaaja_v6 import tallenna_raportti


def _kysy_pvm(teksti: str, allowed_year: int | None = 2025) -> date:
    """Kysyy päivämäärän muodossa pv.kk.vvvv ja palauttaa date.
    Jos allowed_year on asetettu (esim. 2025), vuosi pakotetaan siihen.
    """
    while True:
        s = input(teksti).strip()
        try:
            dt = datetime.strptime(s, "%d.%m.%Y")
            d = dt.date()
            if allowed_year is not None and d.year != allowed_year:
                print(
                    f"Päivämäärän tulee olla vuodelta {allowed_year}. "
                    f"Anna arvo muodossa pv.kk.vvvv (esim. 13.10.{allowed_year})."
                )
                continue  # palaa kysymään ALKUpäivää uudelleen
            return d
        except ValueError:
            print("Virheellinen muoto. Esimerkki: 13.10.2025")


def _kysy_kk() -> int:
    """Kysyy kuukauden numeron 1–12."""
    while True:
        s = input("Anna kuukauden numero (1–12): ").strip()
        try:
            k = int(s)
            if 1 <= k <= 12:
                return k
        except ValueError:
            pass
        print("Anna luku väliltä 1–12.")


def _valikko() -> int:
    """Näyttää raporttivalikon ja palauttaa valinnan (1–4)."""
    print("\nValitse raporttityyppi:")
    print("1) Päiväkohtainen yhteenveto aikaväliltä")
    print("2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle")
    print("3) Vuoden 2025 kokonaisyhteenveto")
    print("4) Lopeta ohjelma")
    while True:
        s = input("Valinta (1–4): ").strip()
        if s in {"1", "2", "3", "4"}:
            return int(s)
        print("Anna arvo 1–4.")


def _jatkovalikko(rivit: List[str]) -> bool:
    """Raportin jälkeen: kirjoita tiedostoon / tee uusi / lopeta.
    Palauttaa True jos halutaan jatkaa, False jos lopetetaan."""
    print("\nMitä haluat tehdä seuraavaksi?")
    print("1) Kirjoita raportti tiedostoon raportti.txt")
    print("2) Palaa päävalikkoon")
    print("3) Lopeta")
    while True:
        s = input("Valinta (1–3): ").strip()
        if s == "1":
            tallenna_raportti(rivit, "raportti.txt")
            print("Raportti kirjoitettu: raportti.txt")
            return True  # palataan uuteen raporttiin
        elif s == "2":
            return False
        elif s == "3":
            raise SystemExit("Ohjelma lopetettu käyttäjän toimesta.")
        else:
            print("Anna arvo 1–3.")


def main() -> None:
    """Lukee datan, pyörittää valikkoa ja tulostaa raportteja."""
    print("Ladataan dataa 2025.csv...")
    rivit = lataa_vuosi("2025.csv")
    paivat = muodosta_paivat(rivit)
    kkdata = muodosta_kuukaudet(paivat)
    vdata = muodosta_vuosi(paivat)
    print("Valmis. Data ladattu.")

    while True:
        valinta = _valikko()
        if valinta == 1:
            alku = _kysy_pvm("Alkupäivä (pv.kk.vvvv): ", allowed_year=2025)
            loppu = _kysy_pvm("Loppupäivä (pv.kk.vvvv): ", allowed_year=2025)
            raportti = raportti_paivavalilta(paivat, alku, loppu)
        elif valinta == 2:
            kk = _kysy_kk()
            raportti = raportti_kuukausi(kkdata, kk)
        elif valinta == 3:
            raportti = raportti_vuosi(vdata)
        elif valinta == 4:
            print("Lopetetaan ohjelma.")
            break

        for r in raportti:
            print(r)

            if not _jatkovalikko(raportti):
                break


if __name__ == "__main__":
    main()
