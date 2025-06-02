from .database import *
from .models import *
from .validators import *
from fastapi import FastAPI, Body, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
import bcrypt
from sqlalchemy import or_, and_

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
    logger.info("Contraseña cifrada!")
    usr_toadd = UserDB(name=user.name, mail=user.contact_mail, passwd=passwd_str, age=user.age)
    db.add(usr_toadd)
    db.commit()
    db.refresh(usr_toadd)
    logger.info(f"Usuario {user.name} registrado en la BDD correctamente")
    
    return usr_toadd


@app.get("/usuarios/{name}", status_code=status.HTTP_200_OK)
def get_user(name: str, db: Session = Depends(get_db)):
    logger.info("Petición recibida para obtener la información de un usuario")
    existing = db.query(UserDB).filter(UserDB.full_name==name).all()
    # Aqui indico que coja todos, ya que puede haber un caso en el que existan dos usuarios que comiencen por el mismo nombre pero que no tengan nada que ver
    # y en ese caso entiendo que lo mejor es sacar todos los que se llamen de esa forma y ya decidir con cual te quedas.
    if not(existing):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe en la BDD")
    logger.info("Petición resuelta")
    return existing


@app.post("/Libros/", status_code=status.HTTP_201_CREATED)
def create_book(book: Book, db: Session = Depends(get_db)):
    logger.info(f"Recibida petición para añadir a la BDD el libro {book.name}")
    existing = db.query(Book_DB).filter(Book_DB.name==book.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este libro ya se ha registrado")
    b = Book_DB(name=book.name, author=book.author)
    db.add(b)
    db.commit()
    db.refresh(b)
    logger.info(f"Libro {b.name} registrado en la BDD correctamente")
    
    return b


@app.get("/libros/{name}", status_code=status.HTTP_200_OK)
def get_book(name: str, db: Session = Depends(get_db)):
    logger.info("Petición recibida para obtener la información de un libro")
    existing = db.query(Book_DB).filter(Book_DB.name==name).first()
    if not(existing):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro no esta registrado en la BDD")
    logger.info("Petición resuelta")
    return existing



@app.post("/Peliculas/", status_code=status.HTTP_201_CREATED)
def create_film(film: Film, db: Session = Depends(get_db)):
    logger.info(f"Recibida petición para añadir a la BDD la pelicula {film.name}")
    existing = db.query(Film_DB).filter(Film_DB.name==film.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Esta pelicula ya se encuentra registrado")
    f = Book_DB(name=film.name, actors=film.actors)
    db.add(f)
    db.commit()
    db.refresh(f)
    logger.info(f"Pelicula {f.name} registrada en la BDD correctamente")
    
    return f


@app.get("/Peliculas/{name}", status_code=status.HTTP_200_OK)
def get_film(name: str, db: Session = Depends(get_db)):
    logger.info("Petición recibida para obtener la información de una pelicula")
    existing = db.query(Film_DB).filter(Film_DB.name==name).first()
    if not(existing):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La pelicula no esta registrada en la BDD")
    logger.info("Petición resuelta")
    return existing


@app.post("/Generos/", status_code=status.HTTP_201_CREATED)
def create_genre(gen: Genre, db: Session = Depends(get_db)):
    logger.info(f"Recibida petición para añadir a la BDD la pelicula {gen.genre_name}")
    existing = db.query(Genre_DB).filter(Genre_DB.genre_name==gen.genre_name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este género ya se encuentra registrado")
    g = Genre_DB(name=gen.genre_name)
    db.add(g)
    db.commit()
    db.refresh(g)
    logger.info(f"Género {g.genre_name} registrado en la BDD correctamente")
    
    return g


@app.get("/Peliculas/{name}", status_code=status.HTTP_200_OK)
def get_genre(name: str, db: Session = Depends(get_db)):
    logger.info("Petición recibida para obtener la información de un genero en concreto")
    existing = db.query(Genre_DB).filter(Genre_DB.genre_name==name).first()
    if not(existing):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Este género no esta registrado en la BDD")
    logger.info("Petición resuelta")
    return existing


@app.post("/Realizar_un_prestamo/", status_code=status.HTTP_201_CREATED)
def loan_articles( user: User, book: Book = None, film: Film = None, db: Session = Depends(get_db)):
    logger.info("Petición recibida para realizar un préstamo")
    ref_book = None
    ref_film = None
    existing_user = db.query(UserDB).filter(and_(UserDB.full_name==user.name, UserDB.contact_mail==user.contact_mail)).first()
    if existing_user:
        logger.info("Analisis del libro solicitado")
        if book:
            existing_book = db.query(Book_DB).filter(Book_DB.name==book.name).first()
            if not(existing_book) or not(existing_book.available):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error, el recurso con nombre {book.name} no existe o no se encuentra disponible")
            db.query(Book_DB).filter(Book_DB.name==book.name).update({"available": False})
            ref_book = existing_book.ref_number
        logger.info("Analisis de la película solicitada") 
        if film:  
            existing_film = db.query(Film_DB).filter(Film_DB.name==film.name).first()
            if not(existing_film) or not(existing_film.available):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error, el recurso con nombre {film.name} no existe o no se encuentra disponible")
            db.query(Film_DB).filter(Film_DB.name==film.name).update({"available": False})
            ref_film = existing_film.ref_number
        logger.info("Analisis completado. Procediendo a registrar el prestamo")
    id_user = existing_user.user_id
    l = Loan_DB(id_user, ref_book, ref_film)
    db.add(l)
    db.commit()
    db.refresh(l)
    
    return l