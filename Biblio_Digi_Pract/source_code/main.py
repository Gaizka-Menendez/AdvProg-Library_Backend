from .database import *
from .models import *
from .validators import *
from fastapi import FastAPI, Body, BackgroundTasks, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging
import bcrypt
from sqlalchemy import or_, and_, DateTime

Base.metadata.create_all(bind=engine)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="My_Digital_Library",
    description="API para la Gestión de la Biblioteca Digital",
    version="1.0.0", 
    debug=True
)

# Esta función (get_db) servirá como generador de sesiones de nuestra BD además de asegurarse su correcta gestion en los diferentes
# endpoints que requieran del uso de conexión. Se indica con Depends
def get_db():
    db = Local_Session()
    try:
        yield db
    finally:
        db.close()
        


@app.post("/Usuarios/", status_code=status.HTTP_201_CREATED)
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
    usr_toadd = UserDB(full_name=user.name, contact_mail=user.contact_mail, hashed_password=passwd_str, age=user.age)
    db.add(usr_toadd)
    db.commit()
    db.refresh(usr_toadd)
    logger.info(f"Usuario {user.name} registrado en la BDD correctamente")
    
    return usr_toadd


@app.get("/Usuarios/{name}", status_code=status.HTTP_200_OK)
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
def create_book(book: Book, genre_name: Optional[str] = Query(None, description="Nombre del género a añadir (opcional)"), db: Session = Depends(get_db)):
    logger.info(f"Recibida petición para añadir a la BDD el libro {book.name}")
    logger.info("Procesando el genero del libro pasado por parámetro")
    if genre_name:
        genre = db.query(Genre_DB).filter(Genre_DB.genre_name==genre_name).first()
        if genre is None:
            logger.info(f"El género '{genre_name}' no existe. Creando nuevo género.")
            new_genre = Genre_DB(genre_name=genre_name)
            db.add(new_genre)
            db.commit()
            db.refresh(new_genre)
            logger.info(f"El género '{genre_name}' se ha registrado correctamente.")
        else:
            new_genre = genre
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Debe especificarse el género de la nueva película")
    
    existing = db.query(Book_DB).filter(Book_DB.name==book.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este libro ya se ha registrado")
    b = Book_DB(name=book.name, author=book.author)
    b.genre_id = new_genre.genre_id
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



# /Peliculas/?genre_name=Accion el parámetro genre_name lo que hace es que se pase ese parámetro en la ruta también de forma

@app.post("/Peliculas/", status_code=status.HTTP_201_CREATED)
def create_film(film: Film, genre_name: Optional[str] = Query(None, description="Nombre del género a añadir (opcional)"), db: Session = Depends(get_db)):
    logger.info(f"Recibida petición para añadir a la BDD la pelicula {film.name}")
    logger.info("Procesando el genero pasado por parámetro")
    if genre_name:
        genre = db.query(Genre_DB).filter(Genre_DB.genre_name==genre_name).first()
        if genre is None:
            logger.info(f"El género '{genre_name}' no existe. Creando nuevo género.")
            new_genre = Genre_DB(genre_name=genre_name)
            db.add(new_genre)
            db.commit()
            db.refresh(new_genre)
            logger.info(f"El género '{genre_name}' se ha registrado correctamente.")
        else:
            new_genre = genre
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Debe especificarse el género de la nueva película")
    # Ahora que ya hemos gestionado el tema del género vamos a ver que hacemos con la película
    
    existing = db.query(Film_DB).filter(Film_DB.name==film.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Esta pelicula ya se encuentra registrada")

    # film.genre_id=new_genre.genre_id 
    f = Film_DB(name=film.name, actors=film.actors)
    f.genre_id = new_genre.genre_id
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
    g = Genre_DB(genre_name=gen.genre_name)
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
    if book is None and film is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error, el recurso con nombre {book.name} no existe o no se encuentra disponible")
    existing_user = db.query(UserDB).filter(and_(UserDB.full_name==user.name, UserDB.contact_mail==user.contact_mail)).first()
    if existing_user:
        logger.info("Analisis del libro solicitado")
        if book:
            existing_book = db.query(Book_DB).filter(Book_DB.name==book.name).first()
            if not(existing_book) or not(existing_book.available):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error, el recurso con nombre {book.name} no existe o no se encuentra disponible")
            existing_book.item_took() # con las funciones de la clase abstaracte decimos que han cogido ese item
            db.add(existing_book)
            # db.refresh(existing_book)
            ref_book = existing_book.ref_number
        logger.info("Analisis de la película solicitada") 
        if film:  
            existing_film = db.query(Film_DB).filter(Film_DB.name==film.name).first()
            if not(existing_film) or not(existing_film.available):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error, el recurso con nombre {film.name} no existe o no se encuentra disponible")
            existing_film.item_took()
            db.add(existing_film)
            # db.refresh(existing_film)
            ref_film = existing_film.ref_number
        logger.info("Analisis completado. Procediendo a registrar el prestamo")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario que se indica que realiza el préstamo no existe")
    id_user = existing_user.user_id
    l = Loan_DB(user_id=id_user, book_ref_number=ref_book, film_ref_number=ref_film)
    db.add(l)
    db.commit()
    db.refresh(l)
    
    return l


@app.put("Devolver_prestamo", status_code=status.HTTP_200_OK)
def loan_returned(loan: Loan, db: Session = Depends(get_db)):
    logger.info("Petición recibida para devolver un préstamo")
    if loan.film_ref_number and loan.book_ref_number:
        existing_loan = db.query(Loan_DB).filter(and_(Loan_DB.user_id==loan.user_id, Loan_DB.book_ref_number==loan.book_ref_number, Loan_DB.film_ref_number==loan.film_ref_number)).first()
    elif loan.film_ref_number and loan.book_ref_number is None:
        existing_loan = db.query(Loan_DB).filter(and_(Loan_DB.user_id==loan.user_id, Loan_DB.film_ref_number==loan.film_ref_number)).first()
    elif loan.film_ref_number is None and loan.book_ref_number:
        existing_loan = db.query(Loan_DB).filter(and_(Loan_DB.user_id==loan.user_id, Loan_DB.book_ref_number==loan.book_ref_number)).first()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puede existir un préstamo donde no se haya prestado nada!!")
    if(existing_loan):
        if existing_loan.book_ref_number:
            existing_book = db.query(Book_DB).filter(Book_DB.ref_number==existing_loan.book_ref_number).first()
            existing_book.item_returned()
            db.add(existing_book)
            db.refresh(existing_book)
        if existing_loan.film_ref_number:
            existing_film = db.query(Film_DB).filter(Film_DB.ref_number==existing_loan.film_ref_number).first()
            existing_film.item_returned()
            db.add(existing_film)
            db.refresh(existing_film)
    else:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el prestamo")       
    existing_loan.return_date = func.now()
    db.add(existing_loan)
    db.commit()
    db.refresh(existing_loan)
    
    return existing_loan