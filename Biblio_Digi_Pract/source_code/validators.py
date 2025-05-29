from .database import *

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

class Book(BaseModel):
    pass
    
class User(BaseModel):
    pass

class Loan(BaseModel):
    pass