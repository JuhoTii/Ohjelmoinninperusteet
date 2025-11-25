"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin käyttäen funkitoita.
Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,90 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime


def hae_varaaja(varaus):
    nimi = varaus[1]
    print(f"Varaaja: {nimi}")


def hae_paiva(varaus):
    paivamaara = datetime.strptime(varaus[2].strip(), "%Y-%m-%d").strftime("%d.%m.%Y")
    print(f"Päivämäärä: {paivamaara}")


def hae_aloitusaika(varaus):
    aloitusaika = varaus[3]
    print(f"Aloitusaika: {aloitusaika}")


def hae_varausnumero(varaus):
    varausnumero = varaus[0]
    print(f"Varausnumero: {varausnumero}")


def hae_tuntimaara(varaus):
    tuntimaara = varaus[4]
    print(f"Tuntimäärä: {tuntimaara}")


def hae_tuntihinta(varaus):
    tuntihinta = float(varaus[5])
    print(f"Tuntihinta: {tuntihinta:.2f} €".replace('.', ','))


def laske_kokonaishinta(varaus):
    tuntihinta = float(varaus[5])
    tuntimaara = float(varaus[4])
    kokonaishinta = (tuntihinta) * (tuntimaara)
    print(f"Kokonaishinta: {kokonaishinta:.2f} €".replace('.', ','))


def hae_maksettu(varaus):
    maksettu = varaus[6].strip().lower()
    if maksettu in ["true"]:
        print("Maksettu: Kyllä")
    else:
        print("Maksettu: Ei")


def hae_kohde(varaus):
    kohde = varaus[7]
    print(f"Kohde: {kohde}")


def hae_puhelin(varaus):
    puhelin = varaus[8]
    print(f"Puhelin: {puhelin}")


def hae_sahkoposti(varaus):
    sahkoposti = varaus[9]
    print(f"Sähköposti: {sahkoposti}")


def main():
    # Maaritellaan tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto, luetaan ja splitataan sisalto
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()
        varaus = varaus.split('|')

    # Toteuta loput funktio hae_varaaja(varaus) mukaisesti
    # Luotavat funktiota tekevat tietotyyppien muunnoksen
    # ja tulostavat esimerkkitulosteen mukaisesti

    hae_varausnumero(varaus)
    hae_varaaja(varaus)
    hae_paiva(varaus)
    hae_aloitusaika(varaus)
    hae_tuntimaara(varaus)
    hae_tuntihinta(varaus)
    laske_kokonaishinta(varaus)
    hae_maksettu(varaus)
    hae_kohde(varaus)
    hae_puhelin(varaus)
    hae_sahkoposti(varaus)


if __name__ == "__main__":
    main()
