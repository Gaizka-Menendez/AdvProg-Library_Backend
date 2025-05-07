import requests
import json


response = requests.get('https://api.chucknorris.io/jokes/random')

if response.status_code == 200:
    data = response.json()
    # print(data['value'])
    print(json.dumps(data, indent=3))
else:
    print(f"Error al obtener los datos: {response.status_code}")

