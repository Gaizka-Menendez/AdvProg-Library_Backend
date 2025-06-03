import requests
import json

# Añdimos unos cuantos usuarios 
url = "http://127.0.0.1:8000/Usuarios/"

user1 = {
    "name": "Ana Garcia Herrero",
    "contact_mail": "ana.garcia@example.com",
    "age": 24,
    "password": "ILOVEFLOWERS"
}

user2 = {
    "name": "Juan Perez Arriaga",
    "contact_mail": "juan.perez@example.com",
    "age": 55,
    "password": "JuanintheBest"
}

user3 = {
    "name": "Fernando Alonso Torres",
    "contact_mail": "fenandito@example.com",
    "age": 33,
    "password": "Elnano33"
}

users = [user1, user2, user3]

for u in users:
    response = requests.post(url, json=u)
    print(f"Código de respuesta: {response.status_code}")
    print(f"Respuesta: {response.json()}")
    
# Prueba del método get de usuarios

name = "Fernando Alonso Torres"
url = f"http://127.0.0.1:8000/Usuarios/{name}"

response = requests.get(url)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")


# Añadimos unos cuantos géneros

url = f"http://127.0.0.1:8000/Generos/"

genre_data1 = {
    "genre_name":"Accion",
}

genre_data2 = {
    "genre_name":"Suspense",
}

genre_data3 = {
    "genre_name":"Terror",
}

genres = [genre_data1, genre_data2, genre_data3]

for g in genres:
    response = requests.post(url, json=g)
    print(f"Código de respuesta: {response.status_code}")
    print(f"Respuesta: {response.json()}")
    
    
    
# Añadimos unos cuantos items a la biblioteca:
# Añadimos unos libros:
url_books = "http://127.0.0.1:8000/Libros/"
book_data1 = {
    "name": "Asesinato en el Orient Express",
    "author": "Agatha Chrsitie Clarissa" 
}

book_data2 = {
    "name": "Geronimo Stilton",
    "author": "Elisabetta Dami Dami" 
}

book_data3 = {
    "name": "Harry Potter y la piedra filosofal",
    "author": "Joanne Kathleen Rowling" 
}

books_to_create = [book_data1, book_data2, book_data3]

genres_for_books = ["Misterio", "Infantil", "Fantasia"]


for i, book_data in enumerate(books_to_create):
    genre = genres_for_books[i]
    
    
    full_url = f"{url_books}?genre_name={genre}"
    
    response = requests.post(full_url, json=book_data)
    
    print(f"--- Creando Libro: '{book_data['name']}' (Género: {genre}) ---")
    print(f"Código de respuesta: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}") 
    

# Añadimos una cuantas películas:


url_films = "http://127.0.0.1:8000/Peliculas/"


film_data1 = {
    "name": "Interestellar",
    "actors": "Matthew McConaughey, Anne Hathaway, Jessica Chastain"
}

film_data2 = {
    "name": "El Señor de los Anillos: La Comunidad del Anillo",
    "actors": "Elijah Wood, Ian McKellen, Viggo Mortensen"
}

film_data3 = {
    "name": "Origen", 
    "actors": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page"
}


films_to_create = [film_data1, film_data2, film_data3]


genres_for_films = ["Ciencia Ficcion", "Fantasia", "Ciencia Ficcion"]


for i, film_data in enumerate(films_to_create):
    genre = genres_for_films[i]
    
    
    full_url = f"{url_films}?genre_name={genre}"
    
    response = requests.post(full_url, json=film_data)
    
    print(f"--- Creando Película: '{film_data['name']}' (Género: {genre}) ---")
    print(f"Código de respuesta: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")



# Realizamos un préstamo de un libro solo

url_loan = "http://127.0.0.1:8000/Realizar_un_prestamo/"

user_data = {
    "name": "Juan Perez Arriaga",
    "contact_mail": "juan.perez@example.com",
    "password": "JuanintheBest"
}

book_data = {
    "name": "Harry Potter y la piedra filosofal", 
    "author": "J. K. Rowling"
}

response = requests.post(
    url_loan,
    json={
        "user": user_data,
        "book": book_data,
        "film": None 
    }
)

print(f"--- Préstamo de Libro ---")
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {json.dumps(response.json(), indent=2)}")



# # Ahora solo préstamo de la película

# url_loan = "http://127.0.0.1:8000/Realizar_un_prestamo/"
# user_data = {
#     "name": "Ana Garcia Herrero",
#     "contact_mail": "ana.garcia@example.com",
#     "password": "ILOVEFLOWERS"
# }

# film_data = {
#     "name": "Die Hard", 
#     "actors": "Bruce Willis, Alan Rickman, Bonnie Bedelia"
# }
# response = requests.post(
#     url_loan,
#     json={
#         "user": user_data,
#         "book": None,
#         "film": film_data
#     }
# )

# print(f"\n--- Préstamo de Película ---")
# print(f"Código de respuesta: {response.status_code}")
# print(f"Respuesta: {json.dumps(response.json(), indent=2)}")




# url_loan = "http://127.0.0.1:8000/Realizar_un_prestamo/"
# user_data = {
#     "name": "Juan Perez Arriaga",
#     "contact_mail": "juan.perez@example.com",
#     "password": "JuanintheBest"
# }
# book_data = {
#     "name": "El Hobbit",
#     "author": "J.R. R. Tolkien"
# }

# film_data = {
#     "name": "Inception",
#     "actors": "Leonardo DiCaprio, Joseph Gordon-Levitt"
# }
# response = requests.post(
#     url_loan,
#     json={
#         "user": user_data,
#         "book": book_data,
#         "film": film_data
#     }
# )

# print(f"\n--- Préstamo de Libro y Película (o fallo si no permitido) ---")
# print(f"Código de respuesta: {response.status_code}")
# print(f"Respuesta: {json.dumps(response.json(), indent=2)}")


# # Intentar prestar nada (debería dar 400 Bad Request)
# response_none = requests.post(
#     url_loan,
#     json={
#         "user": user_data,
#         "book": None,
#         "film": None
#     }
# )

# print(f"\n--- Préstamo de Nada (debería fallar) ---")
# print(f"Código de respuesta: {response_none.status_code}")
# print(f"Respuesta: {json.dumps(response_none.json(), indent=2)}")


# # # Devolución de préstamos
# # url_return = "http://127.0.0.1:8000/Devolver_prestamo/"


# # user_data_existing = {
# #     "name": "Juan Perez Arriaga",
# #     "contact_mail": "juan.perez@example.com",
# #     "password": "JuanintheBest"
# # }
# # loan_data_empty = {
# #     "user_id": 1,
# #     "book_ref_number": None, 
# #     "film_ref_number": None  
# # }


# # response = requests.put(
# #     url_return,
# #     json=loan_data_empty
# # )

# # print(f"\n--- Intentando Devolver Préstamo SIN Libro ni Película ---")
# # print(f"Código de respuesta: {response.status_code}")
# # print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")