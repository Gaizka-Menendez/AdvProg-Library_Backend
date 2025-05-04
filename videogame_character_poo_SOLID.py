class Character:
    
    # Para que esta clase cumpla el principio de responsabilidad única en esta clase solo dejaremos aquellos métodos que 
    # tengan que ver con datos
    
    def __init__(self, hitpoints: int, num_lives:int, damage_per_attack: int): # Método constructor
        self.__hitpoints = hitpoints
        self.__num_lives = num_lives
        self.__damage_per_attack = damage_per_attack

    def __add_hitpoints(self, new_hitpoints: int):
        self.__hitpoints += new_hitpoints

    def __add_lives(self, new_lives: int):
        self.__num_lives += new_lives
        
    def __add_damage_per_attack(self, new_damage: int):
        self.__damage_per_attack += new_damage

    def evolve(self):   
        self.__add_hitpoints(100)                       
        self.__add_lives(1)
        self.__add_damage_per_attack(5)
 
    # Incluimos los getters       
    def get_hitpoints(self):
        return self.__hitpoints
    
    def get_num_lives(self):
        return self.__num_lives
    
    def get_damage_per_attack(self):
        return self.__damage_per_attack

# Para cumplir el principio de responsabilidad única crearemos una clase aparte para todos aquellos métodos que se encarguen
# de mostrar los atributos por pantalla.
class CharacterPresenterConsole:

    def __init__(self, character: Character):
        self.character = character
             
    def show_hitpoints(self):
        hitpoints = self.character.get_hitpoints()
        print(f"Hitpoints: {hitpoints}")
        if hitpoints > 500:
            print("Hitpoints are high")
            
    def show_lives(self):
        num_lives = self.character.get_num_lives()
        print(f"Number of lives: {num_lives}")
        if num_lives > 1:
            print("Wow!! More than one life!")
            
    def show_damage(self):
        damage_per_attack = self.character.get_damage_per_attack()
        print(f"Damage per attack. {damage_per_attack}")
        if damage_per_attack > 50:
            print("Strong player!")
            
    def show_data(self):
        hitpoints = self.character.get_hitpoints()
        num_lives = self.character.get_num_lives()
        damage_per_attack = self.character.get_damage_per_attack()
        """Show the abilities of the character."""
        print(f"Hitpoints: {hitpoints}")
        print(f"Lives: {num_lives}")
        print(f"Damage per attack: {damage_per_attack}")


def separator():
    print("\n")
    print("=" * 20)
    print("\n")

def main():

    my_character = Character(hitpoints=100, num_lives=3, damage_per_attack=20)
    presenter = CharacterPresenterConsole(my_character)
    presenter.show_data()
    
    separator()
    
    print("Evolving character...")
    my_character.evolve()
    presenter.show_data()
    
    
if __name__=="__main__":
    main()
    
    
# SOLID principles:
# S: Single Responsibility Principle (SRP): A class should have only one reason to change.
# O: Open/Closed Principle (OCP): Software entities should be open for extension but closed for modification.
# L: Liskov Substitution Principle (LSP): Objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program.
# I: Interface Segregation Principle (ISP): Clients should not be forced to depend on interfaces they do not use.
# D: Dependency Inversion Principle (DIP): High-level modules should not depend on low-level modules. Both should depend on abstractions.

# Extra notes:

'''El principio Abierto/Cerrado lo que nos dice es que debemos evitar en la medida de lo posible modifcar el código ya existente
Esto quiere decir que en todo caso será mejor aplicar Herencia o Composición (que una clase contenga otra) para realizar los cambios
solicitados.'''

'''El principio de sustitución de liskov nos asegura que se sustituimos los objetos hijo por objetos de la clase padre no 
debería romperse la ejecución, es decir debe de tener sentido. En este caso si sutituimos Guerrero o Mago por Personaje 
o viceversa todo tendría sentido.'''

'''EL principio de segregación de interfaces nos obliga a que las plantillas utilizadas para cada clase sean lo más exactas
posibles, es decir no vamos a definir métodos que no se vayan a utilizar o no tengan sentido. Se puede solucionar haciendo
uso de herencia múltiple de varias interfaces.'''

