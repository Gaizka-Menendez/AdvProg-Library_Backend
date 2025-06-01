import requests

url = "http://127.0.0.1:8000/usuarios/"

user_data = {
    "name":"Fernando Alonso Torres",
    "password":"fennadito33",
    "age":33,
    "contact_mail": "fenando33@gmail.com"
}

response = requests.post(url, json=user_data)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")

user_data = {
    "name":"Fernando Alonso Torres",
    "password":"fennadito33",
    "age":33,
    "contact_mail": "fenando@gmail.com"
}

response = requests.post(url, json=user_data)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")

name = "Fernando Alonso Torres"
url = f"http://127.0.0.1:8000/usuarios/{name}"

response = requests.get(url)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")