from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import * 
from abc import ABC, abstractmethod



class UserDB(Base):
    
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    hashed_password = Column(String)
    contact_mail = Column(String, unique=True, index=True)
    age = Column(Integer, index=True)
    

# La idea es que tanto CD como los libros tengan atributos en comun y aplicando herencia posteriormente cada uno tenga sus particularidades
class Library_Item(ABC):
    pass



class BookDB(Base):
    
    __tablename__ = "books"
    
    ref_number = Column(Integer, primary_key=True, index=True)
    # It is typically not desirable to have “autoincrement” enabled on a column that refers to another via foreign key, as such a column is required to refer to a value that originates from elsewhere.
    b_name = Column(String, unique=True, index=True)
    author = Column(String, index=True)
    available = Column(Boolean, default=True) # Inicialmente lo declaramos a true porque si lo hemos añadido a la BDD es porque lo tenemos
    date_registered = Column(DateTime(timezone=True), server_default=func.now())
    
    

    
    