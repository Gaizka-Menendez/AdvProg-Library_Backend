from .database import *

Base.metadata.create_all(bind=engine)