from nip24 import *
from csv import DictReader
import csv
from tempfile import NamedTemporaryFile

filename_init = 'list-nip.csv'
filename_out = 'sprawdzone.csv'
tempfile = NamedTemporaryFile(mode='w', delete=False)
##Numer klienta
id = ''
##Klucz
key = ''
count = 0


with open(filename_init, 'r') as read_obj:
    with open(filename_out, 'w', newline='') as file:
        csv_dict_reader = DictReader(read_obj)
        fields = ['NIP', 'Status']
        numline = len(read_obj.readlines())
        ##Dla każdego wiersza sprawdz NIP w bazie
        for row in csv_dict_reader:
            writer = csv.DictWriter(file, fieldnames=fields)
            ##Logowanie do NIP24
            nip24 = NIP24Client(id, key)
            ##Sprawdzenie firmy po NIP
            active = nip24.isActiveExt(Number.NIP, row['NIP'])
            count = count + 1 
            ##Jeśli aktywny
            if active:
                status = "Aktywny"
                row['NIP'], row['Status'] = row['NIP'], status
                writer.writerow({'NIP': row['NIP'], 'Status': status})
            ##Jeśli nieaktywny
            else:
                if not nip24.getLastError():
                    status = "Nieaktywny"
                    row['NIP'], row['Status'] = row['NIP'], status
                    writer.writerow({'NIP': row['NIP'], 'Status': status})
            ##Jeśli błąd odczytu danych
                else:
                    status = nip24.getLastError()
                    row['NIP'], row['Status'] = row['NIP'], status
                    writer.writerow({'NIP': row['NIP'], 'Status': status})
            ##Ilość spawdzoych wierszy
            print("Sprawdzone:", count, "/", numline)