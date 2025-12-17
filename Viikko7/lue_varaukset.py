# Copyright (c) 2025 Juho Tiihonen
# This code is licensed under the MIT License.
# TÄMÄ VERSIO KÄYTTÄÄ SANAKIRJOJA (dict) listojen sijaan.
# Tämä on selkeämpi kuin listat, koska viittaukset ovat nimillä (esim. varaus["nimi"])
# eikä "mystisillä" indekseillä (varaus[1]). Koodi on luettavampi ja virhealttiutta on vähemmän.

from datetime import datetime, date, time
from typing import List, Dict


def muunna_varaustiedot(varaus: List[str]) -> Dict:
    """
    Muuntaa listan varauskentät sanakirjaksi.
    Odotettu järjestys rivillä:
    id|nimi|sähköposti|puhelin|paiva|kellonaika|kesto|hinta|vahvistettu|kohde|luotu
    """
    return {
        "id": int(varaus[0]),
        "nimi": varaus[1].strip(),
        "sahkoposti": varaus[2].strip(),
        "puhelin": varaus[3].strip(),
        "paiva": datetime.strptime(varaus[4], "%Y-%m-%d").date(),
        "kellonaika": datetime.strptime(varaus[5], "%H:%M").time(),
        "kesto": int(varaus[6]),
        "hinta": float(varaus[7]),
        "vahvistettu": varaus[8].strip().lower() == "true",
        "kohde": varaus[9].strip(),
        "luotu": datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"),
    }


def _is_header(parts: List[str]) -> bool:
    """Jos ensimmäinen kenttä ei ole kokonaisluku, oletetaan otsikkorivi."""
    try:
        int(parts[0])
        return False
    except Exception:
        return True


def hae_varaukset(varaustiedosto: str) -> List[Dict]:
    #hakee varaukset
    varaukset: List[Dict] = []
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # Jos tiedostossa on otsikkorivi, ohitetaan se
            if i == 1 and _is_header(parts):
                continue
            varaukset.append(muunna_varaustiedot(parts))
    return varaukset


def vahvistetut_varaukset(varaukset: List[Dict]) -> None:

    print("-" * 0, end="")
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            print(
                f"- {varaus['nimi']}, {varaus['kohde']}, {varaus['paiva'].strftime('%d.%m.%Y')} klo {varaus['kellonaika'].strftime('%H.%M')}")
    print()


def pitkat_varaukset(varaukset: List[Dict]) -> None:
    for varaus in varaukset:
        if varaus["kesto"] >= 3:
            print(f"- {varaus['nimi']}, {varaus['paiva'].strftime('%d.%m.%Y')} klo {varaus['kellonaika'].strftime('%H.%M')}, kesto {varaus['kesto']} h, {varaus['kohde']}")
    print()


def varausten_vahvistusstatus(varaukset: List[Dict]) -> None:
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            print(f"{varaus['nimi']} → Vahvistettu")
        else:
            print(f"{varaus['nimi']} → EI vahvistettu")
    print()


def varausten_lkm(varaukset: List[Dict]) -> None:
    vahvistetut = sum(1 for v in varaukset if v["vahvistettu"])
    ei_vahvistetut = len(varaukset) - vahvistetut
    print(f"- Vahvistettuja varauksia: {vahvistetut} kpl")
    print(f"- Ei-vahvistettuja varauksia: {ei_vahvistetut} kpl")
    print()


def varausten_kokonaistulot(varaukset: List[Dict]) -> None:
    tulot = sum(v["kesto"] * v["hinta"] for v in varaukset if v["vahvistettu"])
    print("Vahvistettujen varausten kokonaistulot:",
          f"{tulot:.2f}".replace('.', ','), "€")
    print()


def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)
    print("4) Yhteenveto vahvistuksista")
    varausten_lkm(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot")
    varausten_kokonaistulot(varaukset)


if __name__ == "__main__":
    main()
