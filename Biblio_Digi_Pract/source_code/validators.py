from .database import *
from .models import *

from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr
from typing import Optional

class Book(BaseModel):
    
    # book_ref: int = Field(..., description="Referencia del libro en el sistema")
    # esta validación no es correcta porque al ser primary key esta la auto genera la BD y no es un campo pediod al ussuario
    
    name: str = Field(..., min_length=3, max_length=40, description="Nombre del libro")
    author: str = Field(..., min_length=10, max_length=40, description="Autor del libro")
    genres_ids: list[int] = Field(..., min_items=1, description="IDs de los géneros a los que pertenece el libro")
    
    @field_validator("name")
    def bookname_with_vowels(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("El nombre del libro debe contener vocales!")
        return value
    
    @field_validator("author")
    def author_requirements(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("El nombre del autor debe contener vocales!")
        if len(value.split(" "))!=3:
            raise ValueError("El campo autor debe estar compuesto de tres cadenas de caracteres, una para su nombre y las dos siguientes sus dos primeros apellidos")
        return value

class Film(BaseModel):
    
    # film_ref: int = Field(..., description="Referencia de la película en el sistema")
    name: str = Field(..., min_length=3, max_length=40, description="Nombre de la película")
    actors: str = Field(..., description="Actores de la película")
    genres_ids: list[int] = Field(..., min_items=1, description="IDs de los géneros a los que pertenece la película")
    
    @field_validator("name")
    def actor_str_requirements(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("Los actores de la película deben contener vocales!")
        return value
    
class User(BaseModel):
    
    # user_id: int = Field(..., description="Id del usuario en el sistema")
    name: str = Field(..., min_length=3, max_length=40, description="Nombre del usuario")
    age: Optional[int] = Field(None, min=5, description="Edad (opcional) del usuario")
    password: str = Field(..., min_length=8, max_length=20, description="Contraseña del usuario. Será cifrada antes de guardarse.")
    contact_mail: EmailStr
    
    @field_validator("name")
    def author_requirements(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("El nombre del usuario debe contener vocales!")
        if len(value.split(" "))!=3:
            raise ValueError("El campo usuario debe estar compuesto de tres cadenas de caracteres, una para su nombre y las dos siguientes sus dos primeros apellidos")
        return value

class Loan(BaseModel):
    
    # loan_id: int = Field(..., description="Id del préstmo en el sistema")
    user_id: int = Field(..., description="Id del usuario que ha realizado el préstamo")
    book_ref_number: Optional[int] = Field(default=None, description="Referencia del libro (opcional) alquilado")
    film_ref_number: Optional[int] = Field(default=None, description="Referencia de la película (opcional) alquilada")
    
    @model_validator(mode= "after")
    def loan_minimum_items(cls, instance):
        if not(instance.book_ref_number) and not(instance.film_ref_number):
            raise ValueError("Un préstamo debe ser por lo menos de un libro o de una película")
        return instance

class Genre(BaseModel):
    
    # genre_id: int = Field(..., description="Id del usuario en el sistema")
    genre_name: str = Field(..., min_length=3, max_length=40, description="Nombre del género")
    
    @field_validator("genre_name")
    def genrename_with_vowels(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("El nombre del libro debe contener vocales!")
        return value