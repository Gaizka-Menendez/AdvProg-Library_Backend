import requests

url = "http://127.0.0.1:8000/usuarios/"

# user_data = {
#     "name":"Fernando Alonso Torres",
#     "password":"fennadito33",
#     "age":33,
#     "contact_mail": "fenando33@gmail.com"
# }

# response = requests.post(url, json=user_data)
# print(f"Código de respuesta: {response.status_code}")
# print(f"Respuesta: {response.json()}")

# user_data = {
#     "name":"Fernando Alonso Torres",
#     "password":"fennadito33",
#     "age":33,
#     "contact_mail": "fenando@gmail.com"
# }

# response = requests.post(url, json=user_data)
# print(f"Código de respuesta: {response.status_code}")
# print(f"Respuesta: {response.json()}")

# name = "Fernando Alonso Torres"
# url = f"http://127.0.0.1:8000/usuarios/{name}"

# response = requests.get(url)
# print(f"Código de respuesta: {response.status_code}")
# print(f"Respuesta: {response.json()}")

genre_data1 = {
    "genre_name":"Accion",
}

genre_data2 = {
    "genre_name":"Suspense",
}

genre_data3 = {
    "genre_name":"Terror",
}

response = requests.post(url, json=genre_data1)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")

response = requests.post(url, json=genre_data2)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")

response = requests.post(url, json=genre_data3)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")