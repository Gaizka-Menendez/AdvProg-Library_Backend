import requests
import os

api_key = os.getenv('API_KEY')

question = ("Dime los tres primeros números primos")

#  Tanto los headers como el payload son necesarios para la API de OpenAI y nos los tienen que comunicar
payload = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": question
        }
    ],
    "temperature": 0.3 # Cuanto más bajo mayor precisión
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
    }

url = "https://api.openai.com/v1/chat/completions"

response = requests.post(url, headers=headers, json=payload)

# Si probamos a poner un timeout, esta petición fallará. Por esta razón lo probaríamos con un try y except
# try:
#     response = requests.post(url, headers=headers, json=payload, timeout=0.05)
# except Exception as e:
#     print(str(e))

# Esta parte del código iría justo antes de la línea 42, pero lo hemos puesto aquí para que no falle el programa


if response.status_code == 200:
    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    print(f"Respuesta de OpenAI: {answer}")
else:
    print(f"Error al obtener los datos: {response.status_code}")
    print(response.text)