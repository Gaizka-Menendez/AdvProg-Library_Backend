# Ya usábamos orientación a objetos:
my_set = set([1,2,3]) # Class
print(my_set)
my_set.add(4) # Method
print(my_set)

# =========================================

class Category:

    def __init__(self, name, description=None):
        self.name = name
        self.description = description or "" # Esto, ¿por qué? -->

# --> Explicación:
def agregar_elemento(elemento, lista=[]): # Hay que fijarse en el parámetro opcional, 
# con valor por defecto.
    lista.append(elemento)
    return lista

def agregar_elemento_solved(elemento, lista=None): # Mejor inicializar tras recibir None:
    if lista is None:
        lista = []
    lista.append(elemento)
    return lista

# Llamadas a la función
a = agregar_elemento(1)
print(a)

b = agregar_elemento(2)
print(b) # Comportamiento inesperado!

c = agregar_elemento(3)
print(c) # Comportamiento más inesperado aún!



a = agregar_elemento_solved(1)
print(a)

b = agregar_elemento_solved(2)
print(b)

c = agregar_elemento_solved(3)
print(c)