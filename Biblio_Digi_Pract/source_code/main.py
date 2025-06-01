from .database import *
from .models import *
from .validators import *
from fastapi import FastAPI, Body, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
import bcrypt

Base.metadata.create_all(bind=engine)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="My_Digital_Library",
    description="API para la Gestión de la Biblioteca Digital",
    version="1.0.0"
)

# Esta función (get_db) servirá como generador de sesiones de nuestra BD además de asegurarse su correcta gestion en los diferentes
# endpoints que requieran del uso de conexión. Se indica con Depends
def get_db():
    db = Local_Session()
    try:
        yield db
    finally:
        db.close()
        


@app.post("/usuarios/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: Session = Depends(get_db)):
    logger.info("Petición recibida para crear un nuevo usuario con los datos indicados")
    # Verificamos primero si su nombre o correo ya estan dados ya existen en la BDD.
    if db.query(UserDB).filter(UserDB.contact_mail==user.contact_mail).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario o el correo proporcionados ya existen en la base de datos.")
    logger.info("Cifrando contraseña del usuario...")
    # para la contraseña del usuario la cifraremos haciendo uso de la librería bcrypt
    pwd = user.password.encode("utf-8")
    sal = bcrypt.gensalt()
    encripted_pwd = bcrypt.hashpw(pwd, sal)
    passwd_str=encripted_pwd.decode("utf-8")
    usr_toadd = UserDB(name=user.name, mail=user.contact_mail, passwd=passwd_str, age=user.age)
    db.add(usr_toadd)
    db.commit()
    db.refresh(usr_toadd)
    logger.info(f"Usuario {user.name} registrado en la BDD correctamente")
    
    return usr_toadd


@app.get("/usuarios/{name}")
def get_user(name: str, db: Session = Depends(get_db)):
    logger.info("Petición recibida para obtener la información de un usuario")
    existing = db.query(UserDB).filter(UserDB.full_name==name).first()
    if not(existing):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return existing