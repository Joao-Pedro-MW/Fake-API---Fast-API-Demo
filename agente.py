import requests
from json import loads
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("AGENTE_TOKEN")
headers = {"Authorization": f"Bearer {token}"}

def levenshtein(palavra1: str, palavra2: str) -> int:
    tam_pl1, tam_pl2 = len(palavra1), len(palavra2)
    df = [[0] * (tam_pl2 + 1) for _ in range(tam_pl1 + 1)]
    for i in range(tam_pl1 + 1):
        df[i][0] = i
    for j in range(tam_pl2 + 1):
        df[0][j] = j
    for i in range(1, tam_pl1 + 1):
        for j in range(1, tam_pl2 + 1):
            if palavra1[i - 1] == palavra2[j - 1]:
                df[i][j] = df[i - 1][j - 1]
            else:
                df[i][j] = 1 + min(df[i - 1][j], df[i][j - 1], df[i - 1][j - 1])
    return df[tam_pl1][tam_pl2]

nomes = [loads(requests.get("http://localhost:80/nome", headers=headers).text)['nome'] for i in range(10)]

nomes_distancia = [levenshtein(nomes[0], nomes[i]) for i in range(len(nomes))]
df = pd.DataFrame({
    "Nomes": nomes,
    "Distância para origem": nomes_distancia
})

print(df)
