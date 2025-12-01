# Copyright (c) 2025 Juho Tiihonen
# License: MIT


import csv
from datetime import datetime
from collections import defaultdict

def lue_csv(tiedosto: str) -> list[dict]:
    """Lukee CSV-tiedoston ja palauttaa rivit sanakirjoina."""
    with open(tiedosto, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter=';'))

def muunna_data(rivit: list[dict]) -> dict:
    """Sanakirja ryhmittelee datan päivittäin ja laskee summat (Wh -> kWh)."""
    paivat = defaultdict(lambda: [0, 0, 0, 0, 0, 0])  # kulutus v1,v2,v3, tuotanto v1,v2,v3
    for rivi in rivit:
        aika = datetime.fromisoformat(rivi['Aika'])
        pvm_str = aika.strftime('%d.%m.%Y')
        key = (aika.strftime('%A'), pvm_str)  # esim. ('maanantai', '13.10.2025')

        # Lisää kulutus ja tuotanto (muunna int ja jaa 1000)
        paivat[key][0] += int(rivi['Kulutus vaihe 1 Wh'])
        paivat[key][1] += int(rivi['Kulutus vaihe 2 Wh'])
        paivat[key][2] += int(rivi['Kulutus vaihe 3 Wh'])
        paivat[key][3] += int(rivi['Tuotanto vaihe 1 Wh'])
        paivat[key][4] += int(rivi['Tuotanto vaihe 2 Wh'])
        paivat[key][5] += int(rivi['Tuotanto vaihe 3 Wh'])

    # Muunna Wh -> kWh ja pyöristä kahteen desimaaliin
    for key in paivat:
        paivat[key] = [round(x / 1000, 2) for x in paivat[key]]

    return paivat


def tulosta_raportti(paivat: dict, otsikko: str) -> None:
    print(otsikko)
    print()
    print(f"{'Päivä':<12} {'Pvm':<12} {'Kulutus [kWh]':<30} {'Tuotanto [kWh]':<20}")
    print(f"{'':<12} {'(pv.kk.vvvv)':<12} {'v1':>8} {'v2':>8} {'v3':>8} {'':>4} {'v1':>8} {'v2':>8} {'v3':>8}")
    print("-" * 75)

    for (paiva, pvm), arvot in paivat.items():
        kulutus = [f"{x:.2f}".replace('.', ',') for x in arvot[:3]]
        tuotanto = [f"{x:.2f}".replace('.', ',') for x in arvot[3:]]
        print(f"{paiva:<12} {pvm:<12} "
              f"{kulutus[0]:>8} {kulutus[1]:>8} {kulutus[2]:>8} {'':>4} "
              f"{tuotanto[0]:>8} {tuotanto[1]:>8} {tuotanto[2]:>8}")


def main() -> None:
    tiedosto = 'viikko5.csv'
    data = lue_csv(tiedosto)
    paivat = muunna_data(data)
    tulosta_raportti(paivat, "Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)")

if __name__ == "__main__":
    main()
