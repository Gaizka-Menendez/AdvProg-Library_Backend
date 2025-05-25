import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from fastapi import BackgroundTasks

import time



# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)



# --- DB Pilots and Races setup ---
DATABASE_URL = "sqlite:///./formula_1.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class PilotsDB(Base):
    __tablename__ = "pilots"

    pilot_id = Column(Integer, primary_key=True, index= True, autoincrement=True) #incrementamos el ID en uno cada vez que añadimos un nuevo registro
    pilot_name = Column(String, unique= True, index=True) # decimos que el nombre del piloto debe ser único, no puede estar repetido
    victories = Column(Integer, index=True)
    active_years = Column(String, nullable=True)
    races_won = relationship("RacesDB", back_populates="winner")
    

class RacesDB(Base): 
    __tablename__ = "races"
    
    race_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    winner_id = Column(Integer, ForeignKey("pilots.pilot_id"), index=True)
    year = Column(Integer, index=True)
    race_name = Column(String, index=True)
    winner = relationship("PilotsDB", back_populates="races_won")

Base.metadata.create_all(bind=engine)




# --- Pydantic models ---   
class Races(BaseModel):
    race_id: int = Field(..., description="Id de la carrera")
    name: str = Field(..., min_length=3, max_length=20, description="Nombre de la carrera (de 3 a 20 caracteres)")
    year: int = Field(None, description="Año de la carrera")
    winner_id: int = Field(..., description="Id del piloto ganador de la carrera")

    @field_validator("name")
    def racename(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("There must be vowels in the race name!")
        return value
    
    @field_validator("year")
    def valid_year(cls, value):
        y = int(time.strftime("%Y", time.gmtime()))
        if value > y:
            raise ValueError("The year of the race can't be higher than nowadays!!!")
        return value
    

class Pilots(BaseModel):
    pilot_id: int = Field(..., description="Id del piloto")
    name: str = Field(..., min_length=3, max_length=20, description="Nombre del piloto (de 3 a 20 caracteres)")
    vict: int = Field(..., description="Numero de victorias del piloto")
    active_years: int = Field(None, description="Años que ha estado en activo el piloto (opcional)")
    races_won: list[Races] = Field([], description="Lista de carreras ganadas por un piloto")

    @field_validator("name")
    def username_with_values(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("There must be vowels in the pilot name!")
        return value
    
    @field_validator("active_years")
    def active_pilot(cls, value):
        if value <=0:
            raise ValueError("The pilot hasn't been active for at least one year")
        return value
    
    @model_validator(mode="after")
    def victory_validation(cls, instance):
        if instance.vict != len(instance.races_won):
            raise ValueError("It's not possible to have a discrepancy between the number of won races and victories")
        return instance   
    





# --- FastAPI setup ---
app = FastAPI(
    title="API para la práctica de clase sobre Formula 1",
    description="API de ejemplo",
    version="1.0.0"
)



#  Quiero preguntar si estos métodos al declarar sus respectivos ids con autoincrement es necesario pasarle algo al método como param
@app.post("/pilots/")
async def create_user(pilot: Pilots):
    # pilot_id = pilot.pilot_id
    pilot_name = pilot.name
    victories = pilot.vict
    active_years = pilot.active_years
    races_won = pilot.races_won
    return {
        "msg": "Información del piloto recibida correctamente",
        "PiloT name": pilot_name,
        "Victories": victories,
        "active_years": active_years,
        "races_won": races_won
    }
    
@app.post("/races/")
async def create_user(race: Races):
    # race_id = race.race_id
    name = race.name
    year = race.year
    winner_id = race.winner_id
    return {
        "msg": "Información de la carrera recibida correctamente",
        "Race name": name,
        "Year of the race": year,
        "Winner of the race": winner_id
    }


# método que va a devolver todas las carreras ganadas por un piloto
@app.get("/pilots/{pilot_name}/races")
def amount_of_won_races_by_pilot(pilot_name: str):
    logger.info(f"Petición de la lista de carreras del piloto {pilot_name}")
    db = SessionLocal()
    existing = db.query(PilotsDB).filter(PilotsDB.pilot_name == pilot_name).first()
    if existing:
        db.close()
        logger.info(f"Envío del número de carreras ganadas por el piloto {pilot_name}")
        return {
            "msg": "Piloto encontrado",
            "races_won": f"{existing.pilot_name} ha ganado un total de {len(existing.races_won)} carreras",
            "races": existing.races_won
            }
    else: 
        db.close()
        logger.warning(f"Envío del número de carreras ganadas por el piloto {pilot_name}")
        raise HTTPException(status_code=404, detail=f"El piloto {pilot_name} no esta registrado en la BBDD")
    

@app.get("/pilots/{name}")
def custom_greeting(name: str):
    logger.info(f"Recibida petición obtener el piloto con nombre: {name}")
    db = SessionLocal()
    processed_name_wth_spaces = name.replace("_", " ")
    processed_name = processed_name_wth_spaces.title()
    pilot = db.query(PilotsDB).filter(PilotsDB.pilot_name == processed_name).first()
    db.close()
    if pilot:
        return {
            "msg": "Pilot found",
            "name": pilot.pilot_name,
            "Victories": pilot.victories,
            "active_years": pilot.active_years,
            "races_won": pilot.races_won
            }
    else:
        raise HTTPException(status_code=404, detail=f"El piloto {processed_name} no esta registrado en la BBDD")
    

@app.get("/pilots/maxGanador/")
def get_best_pilot():
    logger.info("Petición para conocer al máximo ganador solicitada")
    db = SessionLocal()
    pilot_with_most_wins = db.query(PilotsDB).order_by(PilotsDB.victories.desc()).first()
    db.close()
    if pilot_with_most_wins:
        logger.info("Petición para conocer al máximo ganador concluida")
        return {
            "msg": "Piloto con mayor número de victorias encontrado",
            "name": pilot_with_most_wins.pilot_name,
            "Victories": pilot_with_most_wins.victories,
            "active_years": pilot_with_most_wins.active_years,
            "races_won": pilot_with_most_wins.races_won
            }
    else:
        raise HTTPException(status_code=404, detail=f"No hay pilotots en la BBDD")


# def enviar_email_bienvenida(email: str):
#     logger.info(f"📧 Simulando envío de email a {email}...")
#     import time
#     time.sleep(10)  # Simular retardo para ver la asincronía
#     logger.info(f"✅ Email de bienvenida enviado a {email}")

# @app.post("/pilotos/")
# def create_user(pilotos: Pilotos):
#     logger.info(f"📥 Registro de usuario recibido: {pilotos}")
    
#     # db = SessionLocal()
#     # existing = db.query(PilotosDB).filter(PilotosDB.pilotos == pilotos.pilotos).first()
#     # if existing:
#     #     db.close()
#     #     raise HTTPException(status_code=400, detail="El piloto ya está registrado")
#     #
#     # pilotos_db = PilotosDB(pilotosname=pilotos.pilotosname, victorias=pilotos.victorias, anosactivo=pilotos.anosactivo)
#     # db.add(pilotos_db)
#     # db.commit()
#     # db.refresh(pilotos_db)
#     # db.close()
#     # logger.info(f"✅ Piloto guardado: {pilotos_db.pilotosname}")
#     # Tarea en segundo plano
#     # background_tasks.add_task(enviar_email_bienvenida, pilotos.email)
#     return {
#         "msg": "Usuario registrado correctamente",
#         # "pilotos": {
#         #     "piloto": pilotos_db.pilotos,
#         #     "victorias": pilotos_db.victorias,
#         #     "anosactivo": pilotos_db.anosactivo
#         # }
#     }
