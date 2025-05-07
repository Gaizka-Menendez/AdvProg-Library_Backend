import requests

latitude = 40.4154
longitude = -3.7074
url = (f'https://api.open-meteo.com/v1/forecast?'
       f'latitude={latitude}&longitude={longitude}'
       '&current_weather=true')
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    weather = data['current_weather']
    print(f"Temperatura: {weather['temperature']}°C")
else:
    print(f"Error al obtener los datos: {response.status_code}")
    print(response.text)