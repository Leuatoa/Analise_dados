import csv

def ler_csv(caminho):
    with open(caminho, encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        return [linha for linha in leitor]
