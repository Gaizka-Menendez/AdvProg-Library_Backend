from fastapi import FastAPI

app = FastAPI(
        title = "Mi primera API de FastASPI",
        description = "Una API de ejemplo",
        version = "1.0.0"
    ) 

# de la librería fastapi importamos la clase FastAPI y la instanciamos


# Definimos un endpoint, en la raiz del path definimos que al ser llamado con un método get te contesta con un json 
# con un msg
@app.get("/hello")
def initial_greeting():
    return {"msg": "Hello world, I'm using FastAPI!!!"}

@app.get("/hello/{name}")
def custom_greeting(name:str):
    processed_name = name.capitalize()
    return {"msg": f"Hello, {processed_name}!!!!"}