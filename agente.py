import requests
from json import loads

nomes = [loads(requests.get("http://localhost/nome").text)[1] for i in range(3)]
print(nomes)
