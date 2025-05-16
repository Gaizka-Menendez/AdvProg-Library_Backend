from fastapi import FastAPI
import logging # para los mensajes de registro
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
        title = "Mi primera API de FastASPI",
        description = "Una API de ejemplo",
        version = "1.0.0"
    ) 

# de la librería fastapi importamos la clase FastAPI y la instanciamos

logging.basicConfig(
    level=logging.WARNING, #DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) # Solo va a logar los niveles superiores o de mayor gravedad.

logger = logging.getLogger(__name__)

class User(BaseModel):
    username: str
    email: str
    age: Optional[int]
    

# Definimos un endpoint, en la raiz del path definimos que al ser llamado con un método get te contesta con un json 
# con un msg
@app.get("/hello")
def initial_greeting():
    logger.info("Recibida petición al saludo genérico")
    return {"msg": "Hello world, I'm using FastAPI!!!"}

@app.get("/hello/{name}")
def custom_greeting(name:str):
    logger.info(f"Recibida petición para un saludo personalizado de {name}")
    processed_name = name.capitalize()
    logger.debug(f"Nombre procesado: {processed_name}")
    if processed_name == "Pepe":
        logger.warning("Pepe ha entrado a la web!!!")
    return {"msg": f"Hello, {processed_name}!!!!"}


@app.post("/users/")
def create_user(user: User):
    logger.info(f"Registro de usuario recibido: {user}")
    # Registramos al usuario en la BBDD
    return {
        "msg": "Usuario registrado correctamente",
        "usuario": user.username
    }
