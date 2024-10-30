import requests
from json import loads
import pandas as pd

def levenshtein(palavra1:str, palavra2:str)->int:
    tam_pl1, tam_pl2 = len(palavra1), len(palavra2)
    # criação da matriz vazia, onde o número de linhas é 1 mais que o tamanho da primeira palavra 
    # e o número de colunas é 1 a mais que o tamanho de letras da palavra 2
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

nomes = [loads(requests.get("http://localhost/nome").text)[1] for i in range(3)]
nomes_distancia = [levenshtein(nomes[0],nomes[i]) for i in range(len(nomes))]
df = pd.DataFrame({
    "Nomes": nomes,
    "Distância para origem": nomes_distancia
})
print(df)