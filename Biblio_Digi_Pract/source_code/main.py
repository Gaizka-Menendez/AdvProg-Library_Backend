from .database import *
from .models import *

Base.metadata.create_all(bind=engine)

# Esta función (get_db) servirá como generador de sesiones de nuestra BD además de asegurarse su correcta gestion en los diferentes
# endpoints que requieran del uso de conexión. Se indica con Depends
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()