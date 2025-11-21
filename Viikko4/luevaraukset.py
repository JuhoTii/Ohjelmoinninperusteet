from datetime import datetime


def muunna_varaustiedot(varaus: list) -> list:
    # Tähän tulee siis varaus oletustietotyypeillä (str)
    # Varauksessa on 11 saraketta -> Lista -> Alkiot 0-10
    # Muuta tietotyypit haluamallasi tavalla -> Seuraavassa esimerkki ensimmäisestä alkioista
    muutettu_varaus = []
    # Ensimmäisen alkion = varaus[0] muunnos
    muutettu_varaus.append(int(varaus[0]))
    muutettu_varaus.append(str(varaus[1]))
    muutettu_varaus.append(str(varaus[2]))
    muutettu_varaus.append(str(varaus[3]))
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").time())
    muutettu_varaus.append(int(varaus[6]))
    muutettu_varaus.append(float(varaus[7]))
    muutettu_varaus.append(varaus[8].strip().lower() == "true")
    muutettu_varaus.append(str(varaus[9]))
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
    return muutettu_varaus


def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo",
                     "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset


def main():
    # HUOM! seuraaville riveille ei tarvitse tehdä mitään osassa A!
    # Osa B vaatii muutoksia -> Esim. tulostuksien (print-funktio) muuttamisen.
    # Kutsutaan funkioita hae_varaukset, joka palauttaa kaikki varaukset oikeilla tietotyypeillä
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    for vahvaraus in varaukset[1:]:
        if vahvaraus[8]:  # Vain vahvistetut varaukset
            nimi = vahvaraus[1]
            tila = vahvaraus[9]
            pvm = vahvaraus[4].strftime("%d.%m.%Y")
            klo = vahvaraus[5].strftime("%H.%M")
            print(f"- {nimi}, {tila}, {pvm} klo {klo}")
    print("------------------------------------------------------")
    print("2) Pitkät varaukset(kesto vähintään 3 tuntia  )")
    for pitvaraus in varaukset[1:]:
        if pitvaraus[6] >= 3:
            nimi = pitvaraus[1]
            pvm = pitvaraus[4].strftime("%d.%m.%Y")
            kelloaika = pitvaraus[5].strftime("%H.%M")
            kesto = pitvaraus[6]
            tila = pitvaraus[9]
            print(
                f"- {nimi}, Päivämäärä: {pvm} , kellonaika: {kelloaika} , kesto: {kesto} tuntia, tila: {tila}")
    print("------------------------------------------------------")

    print("3) Varausten vahvistus status:")
    for status in varaukset[1:]:
        if status[8] == True:
            vahstatus = "Vahvistettu"
        else:
            vahstatus = "Ei vahvistettu"
        nimi = status[1]
        vahvistettu = status[8]
        print(f"- {nimi}-> {vahstatus}")
    print("------------------------------------------------------")

    print("4) Yhteenveto vahvistuksista:")
    vahvistetut_maara = sum(1 for varaus in varaukset[1:] if varaus[8])
    eivahvistetut_maara = sum(1 for varaus in varaukset[1:] if not varaus[8])
    print(f"- Vahvistettuja varauksia: {vahvistetut_maara}")
    print(f"- Ei vahvistettuja varauksia: {eivahvistetut_maara}")

    print("------------------------------------------------------")

    print("5) Vahvistettujen varausten kokonaistulot")
    kokonaistulot = sum(varaus[7] for varaus in varaukset[1:] if varaus[8])
    muutettu_kokonaistulot = f"{kokonaistulot:.2f}".replace('.', ',')
    print(
        f"- Vahvistettujen varausten kokonaistulot: {muutettu_kokonaistulot} euroa")
    
    print("------------------------------------------------------")


if __name__ == "__main__":
    main()
