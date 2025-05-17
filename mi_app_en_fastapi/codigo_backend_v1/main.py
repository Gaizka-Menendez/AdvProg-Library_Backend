from fastapi import FastAPI, HTTPException
import logging # para los mensajes de registro
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


# --- DB setup ---
DATABASE_URL = "sqlite:///./usuarios.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class UserDB(Base):
    __tablename__ ="usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)
    
Base.metadata.create_all(bind=engine)
    
    
    

class User(BaseModel):
    username: str = Field(..., min_length=3, description="Nombre de ususario mínimo de 3 caracteres")
    email: str = Field(..., description="Email del usuario")
    age: Optional[int] = Field(None, ge=0, description="Edad no negativa (opcional)")
    
    @field_validator("username")
    def username_with_vowels(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("El nombre de usuario debe contener al menos una vocal")
        return value
        
        
    
    # Como es un model validator nos llega lo que es una instancia completa "instance" y se basa en validaciones cruzadas
    # es decir que una variable dependa de otra en la validación
    @model_validator(mode="after") # El mode en este caso indica que se lleva a cabo la validación una vez se han validado cada uno de los campos individuales
    def long_username_if_age_ge_50(cls, instance):
        if instance.age >= 50:
            if len(instance.username) < 20:
                raise ValueError("El nombre debe ser mas largo que 20 caracteres")
        return instance 
    

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
    
    db = SessionLocal()
    existing = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing:
        db.close()
        logger.error("El email ya existe en la base de datos")
        raise HTTPException(status_code=400, detail="El email ya existe en la base de datos")
    
    user_db = UserDB(username=user.username, email=user.email, age=user.age)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    db.close()
    # Registramos al usuario en la BBDD
    logger.info(f"Usuario guardado en la BBDD: {user_db.username}")
    
    return {
        "msg": "Usuario registrado correctamente",
        "usuario": user.username
    }
