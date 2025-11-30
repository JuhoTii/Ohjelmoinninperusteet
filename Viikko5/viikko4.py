import datetime
import csv

#Tiedoston polku
file_path = 'viikko42.csv'

#luetaan tiedosto ja tulostetaan rivit
with open(file_path,newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        print(row)