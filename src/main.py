import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
from src.models.pessoa import Pessoa
from src.services.gender_service import GenderAPIService
from src.repo.csv_repo import ler_csv
from src.repo.json_repo import salvar_json
from collections import Counter

def main():
    caminho_arquivo = "lista_clientes.csv"
    dados_raw = ler_csv(caminho_arquivo)
   
    gender_service = GenderAPIService()

    pessoas = []
    for linha in dados_raw:
        p = Pessoa(
            nome=linha.get("nome_completo", ""),
            email=linha.get("email", ""),
            celular=linha.get("celular", ""),
            interesse=linha.get("interesse", ""),
            cpf=linha.get("cpf", ""),
            cep=linha.get("cep", ""),
        )
        p.inferir_genero(gender_service)
        pessoas.append(p)

    pessoas.sort(key=lambda x: x.nome_completo)

    users_json = {
        "users": [
            {
                "nome_completo": p.nome_completo,
                "primeiro_nome": p.primeiro_nome,
                "segundo_nome": p.segundo_nome,
                "genero": p.genero,
                "email": p.email,
                "celular": p.celular,
                "interesse": p.interesse,
                "cpf": p.cpf,
                "bairro": p.bairro,
                "cidade": p.cidade,
                "estado": p.estado,
                "observacoes": "; ".join(p.observacoes),
            }
            for p in pessoas
        ]
    }

    salvar_json("saida.json", users_json)

    total = len(pessoas)
    generos = Counter(p.genero for p in pessoas)
    print("Distribuição de gênero:")
    for g, c in generos.items():
        print(f"  {g}: {c} ({c/total*100:.2f}%)")

    estados = Counter(p.estado for p in pessoas if p.estado)
    print("\nDistribuição geográfica por estado:")
    for e, c in estados.items():
        print(f"  {e}: {c} ({c/total*100:.2f}%)")

    cpfs_invalidos = sum(1 for p in pessoas if "CPF inválido" in p.observacoes)
    celulares_ausentes = sum(1 for p in pessoas if "Celular ausente" in p.observacoes)
    print(f"\nCPFs inválidos: {cpfs_invalidos}")
    print(f"Celulares ausentes: {celulares_ausentes}")

    interesses = Counter(p.interesse for p in pessoas)
    print("\nDistribuição das áreas de interesse:")
    for i, c in interesses.items():
        print(f"  {i}: {c} ({c/total*100:.2f}%)")

    interesse_genero = {}
    for p in pessoas:
        if p.genero not in interesse_genero:
            interesse_genero[p.genero] = Counter()
        interesse_genero[p.genero][p.interesse] += 1

    print("\nÁreas de interesse por gênero:")
    for genero, counter in interesse_genero.items():
        print(f"  {genero}:")
        total_gen = sum(counter.values())
        for area, qtd in counter.items():
            print(f"    {area}: {qtd} ({qtd/total_gen*100:.2f}%)")

if __name__ == "__main__":
    main()
