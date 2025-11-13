"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""


from datetime import datetime


def main():
    varaukset = "varaukset.txt"

    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip().split('|')

    # Muunnokset
    varausnumero = int(varaus[0])
    varaaja = varaus[1]

    # Päivämäärä ja aika
    paiva = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    suomalainenPaiva = paiva.strftime("%d.%m.%Y")

    aika = datetime.strptime(varaus[3], "%H:%M").time()
    suomalainenAika = aika.strftime("%H.%M")

    tuntimaara = int(varaus[4])
    tuntihinta = float(varaus[5])
    maksettu = varaus[6].lower() == "true"
    kohde = varaus[7]
    puhelin = int(varaus[8])
    sahkoposti = varaus[9]

    # Tulostus
    print(f"Varausnumero: {varausnumero}")
    print(f"Varaaja: {varaaja}")
    print(f"Päivämäärä: {suomalainenPaiva}")
    print(f"Aloitusaika: {suomalainenAika}")
    print(f"Tuntimäärä: {tuntimaara}")
    print(f"Tuntihinta: {tuntihinta} €")
    print(f"Maksettu: {'kyllä' if maksettu else 'ei'}")
    print(f"Kohde: {kohde}")
    print(f"Puhelin: {puhelin}")
    print(f"Sähköposti: {sahkoposti}")


if __name__ == "__main__":
    main()
