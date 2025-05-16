import requests

url = "http://localhost:8000/users/"

user_data = {
    "email": "gaizkam20@gmail.com",
    "username": "Gaizka", 
    "age": 24
}

response = requests.post(url, json=user_data)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")