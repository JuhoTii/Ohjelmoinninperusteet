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
    varausnumero = varaus[0]
    paivamaara = varaus[2]
    aloitusaika = varaus[3]
    tuntimaara = varaus[4]
    tuntihinta = float(varaus[5])
    kokonaishinta = float(tuntihinta) * int(tuntimaara)
    maksettu = varaus[6].strip().lower() == "true" and "Kyllä" or "Ei"
    kohde = varaus[7]
    puhelin = varaus[8]
    sahkoposti = varaus[9]
    print(f"Varausnumero: {varausnumero}")
    print(f"Varaaja: {nimi}")
    print(f"Päivämäärä: {paivamaara}")
    print(f"Aloitusaika: {aloitusaika}")
    print(f"Tuntimäärä: {tuntimaara}")
    print(f"Tuntihinta: {tuntihinta:.2f}€")
    print(f"Kokonaishinta: {kokonaishinta:.2f}€")
    print(f"Maksettu: {maksettu}")
    print(f"Kohde: {kohde}")
    print(f"Puhelin: {puhelin}")
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

    # hae_varausnumero(varaus)
    hae_varaaja(varaus)
    # hae_paiva(varaus)
    # hae_aloitusaika(varaus)
    # hae_tuntimaara(varaus)
    # hae_tuntihinta(varaus)
    # laske_kokonaishinta(varaus)
    # hae_maksettu(varaus)
    # hae_kohde(varaus)
    # hae_puhelin(varaus)
    # hae_sahkoposti(varaus)


if __name__ == "__main__":
    main()
