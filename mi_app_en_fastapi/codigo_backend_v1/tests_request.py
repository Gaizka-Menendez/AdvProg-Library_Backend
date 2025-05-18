import requests

url = "http://localhost:8000/users/"

# user_data = {
#     "email": "gaizkam20@gmail.com",
#     "username": "Gaizka", 
#     "age": 24
# }

# user_data = {
#     "email": "gaizka.menendez.hernandez@alumnos.upm.es",
#     "username": "Gaizka M", 
#     "age": 20
# }

user_data = {
    "email": "jmenendez0001@gmail.com",
    "username": "Joaquin Menéndez Cruces", 
    "age": 50
}

response = requests.post(url, json=user_data)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")