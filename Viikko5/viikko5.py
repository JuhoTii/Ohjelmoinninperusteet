import datetime
import csv

#Tiedoston polku
file_path = 'viikko42.csv'
def lue_csv(viikko5_csv: str) -> list:
#luetaan tiedosto ja tulostetaan rivit

 with open(file_path,newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        print(row)



def main() -> None:
    """Ohjelman pääfunktio: lukee datan, laskee yhteenvedot ja tulostaa raportin."""
    ...





    if __name__ == "__main__":
        main()