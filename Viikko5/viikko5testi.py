
import csv
from datetime import datetime
from collections import defaultdict

def lue_csv(tiedosto: str) -> list[dict]:
    """
    Lukee CSV-tiedoston ja palauttaa listan sanakirjoja.
    :param tiedosto: CSV-tiedoston polku
    :return: Lista riveistä sanakirjoina
    """
    rivit = []
    with open(tiedosto, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            rivit.append(row)
    return rivit

def muunna_data(data: list[dict]) -> list[dict]:
    """
    Muuntaa arvot oikeisiin tyyppeihin (datetime, int).
    :param data: Lista sanakirjoja merkkijonoarvoilla
    :return: Lista sanakirjoja muunnetuilla arvoilla
    """
    muunnettu = []
    for rivi in data:
        aika = datetime.fromisoformat(rivi['Aika'])
        kulutus = [int(rivi['Kulutus vaihe 1 Wh']),
                   int(rivi['Kulutus vaihe 2 Wh']),
                   int(rivi['Kulutus vaihe 3 Wh'])]
        tuotanto = [int(rivi['Tuotanto vaihe 1 Wh']),
                    int(rivi['Tuotanto vaihe 2 Wh']),
                    int(rivi['Tuotanto vaihe 3 Wh'])]
        muunnettu.append({'aika': aika, 'kulutus': kulutus, 'tuotanto': tuotanto})
    return muunnettu

def laske_yhteenveto(data: list[dict]) -> tuple[dict, dict]:
    """
    Laskee päiväkohtaiset summat Wh-yksikössä ja tallentaa päivämäärän.
    :param data: Lista muunnettuja rivejä
    :return: (yhteenveto, paivamaarat)
    """
    yhteenveto = defaultdict(lambda: {'kulutus': [0,0,0], 'tuotanto': [0,0,0]})
    paivamaarat = {}
    for rivi in data:
        paiva = rivi['aika'].strftime('%A').lower()  # esim. 'maanantai'
        if paiva not in paivamaarat:
            paivamaarat[paiva] = rivi['aika']  # Ensimmäinen esiintymä
        for i in range(3):
            yhteenveto[paiva]['kulutus'][i] += rivi['kulutus'][i]
            yhteenveto[paiva]['tuotanto'][i] += rivi['tuotanto'][i]
    return yhteenveto, paivamaarat

def wh_to_kwh(arvo_wh: int) -> float:
    """
    Muuntaa Wh → kWh.
    :param arvo_wh: Arvo wattitunteina
    :return: Arvo kilowattitunteina
    """
    return arvo_wh / 1000

def tulosta_taulukko(yhteenveto: dict, paivamaarat: dict) -> None:
    """
    Tulostaa yhteenvedon taulukkona, sisältäen päivämäärän ja desimaalipilkun.
    """
    print("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
    print("Päivä         Pvm         Kulutus [kWh]                 Tuotanto [kWh]")
    print("             (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3")
    print("-" * 75)

    paivat = ['maanantai','tiistai','keskiviikko','torstai','perjantai','lauantai','sunnuntai']
    for paiva in paivat:
        if paiva in yhteenveto:
            kulutus = [wh_to_kwh(x) for x in yhteenveto[paiva]['kulutus']]
            tuotanto = [wh_to_kwh(x) for x in yhteenveto[paiva]['tuotanto']]
            pvm = paivamaarat[paiva].strftime('%d.%m.%Y')
            # Muotoillaan desimaalipilkulla
            kulutus_fmt = [f"{x:.2f}".replace('.', ',') for x in kulutus]
            tuotanto_fmt = [f"{x:.2f}".replace('.', ',') for x in tuotanto]
            print(f"{paiva:<12} {pvm:<11} {kulutus_fmt[0]:>6} {kulutus_fmt[1]:>6} {kulutus_fmt[2]:>6}    {tuotanto_fmt[0]:>6} {tuotanto_fmt[1]:>6} {tuotanto_fmt[2]:>6}")

def main() -> None:
    tiedosto = 'viikko5.csv'
    data = lue_csv(tiedosto)
    muunnettu = muunna_data(data)
    yhteenveto, paivamaarat = laske_yhteenveto(muunnettu)
    tulosta_taulukko(yhteenveto, paivamaarat)

if __name__ == "__main__":
    main()
