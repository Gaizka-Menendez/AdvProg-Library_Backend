import requests

url = "http://localhost:8000/users/"

# user_data = {
#     "email": "juanito20@gmail.com",
#     "username": "Juan", 
#     "age": 24
# }

# user_data = {
#     "email": "giosvienar@gmail.com",
#     "username": "Giosvienar M", 
#     "age": 20
# }

user_data = {
    "email": "joaco@gmail.com",
    "username": "Joaquin Quintero Perez", 
    "age": 50
}

response = requests.post(url, json=user_data)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")
