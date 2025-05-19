import requests
import json


"""
url = "http://127.0.0.1:8000/pilotos/"

print("HOlahola")

pilotos_data = {
    "pilotos":"Fer. Alonso",
    "victorias":32,
    "anosactivo":"33"
}

response = requests.post(url, json=pilotos_data)
print(f"Código de respuesta: {response.status_code}")
# print(f"Respuesta: {response.json()}")
print(type(response))
print(response.text)

"""


base_url = "http://127.0.0.1:8000"

# --- Pruebas para /pilots/ ---

def test_create_pilot():
    url = f"{base_url}/pilots/"
    pilot_data = {"name": "Lewis Hamilton", "vict": 103, "active_years": 19, "races_won": []}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=pilot_data)
    assert response.status_code == 200
    assert response.json()["msg"] == "Información del piloto recibida correctamente"
    assert response.json()["PiloT name"] == "Lewis Hamilton"
    assert response.json()["Victories"] == 103
    print("Test de creación de piloto pasado.")

def test_get_pilot_races_found():
    # Para esta prueba, primero necesitamos asegurarnos de que existe un piloto con carreras ganadas.
    # Esto podría implicar crear un piloto y luego (en una API real) crear carreras asociadas a ese piloto.
    # Para simplificar la prueba sin implementar toda la creación, asumimos que ya existe un piloto llamado "Lewis Hamilton" con carreras.
    pilot_name = "Lewis Hamilton"
    url = f"{base_url}/pilots/{pilot_name}/races"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        assert data["msg"] == "Piloto encontrado"
        assert "races_won" in data
        assert "races" in data and isinstance(data["races"], list)
        print(f"Test de obtención de carreras de '{pilot_name}' pasado.")
    elif response.status_code == 404:
        print(f"Advertencia: El piloto '{pilot_name}' no se encontró para la prueba de obtención de carreras.")
        assert False, f"El piloto '{pilot_name}' no se encontró, asegúrate de que exista para esta prueba."
    else:
        assert False, f"Error al obtener las carreras de '{pilot_name}': {response.status_code} - {response.text}"

def test_get_pilot_races_not_found():
    pilot_name = "NonExistentPilot"
    url = f"{base_url}/pilots/{pilot_name}/races"
    response = requests.get(url)
    assert response.status_code == 404
    assert response.json()["detail"] == f"El piloto {pilot_name} no esta registrado en la BBDD"
    print(f"Test de piloto '{pilot_name}' no encontrado pasado.")

# --- Pruebas para /races/ ---

def test_create_race():
    url = f"{base_url}/races/"
    race_data = {"name": "Monaco GP", "year": 2024, "winner_id": 1}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=race_data)
    assert response.status_code == 200
    assert response.json()["msg"] == "Información de la carrera recibida correctamente"
    assert response.json()["Race name"] == "Monaco GP"
    assert response.json()["Year of the race"] == 2024
    assert response.json()["Winner of the race"] == 1
    print("Test de creación de carrera pasado.")

if __name__ == "__main__":
    print("Iniciando pruebas...")
    test_create_pilot()
    test_create_race()
    test_get_pilot_races_found()
    test_get_pilot_races_not_found()
    print("Todas las pruebas básicas completadas.")