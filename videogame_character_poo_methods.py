class Character:
    
    # Encapsular es tener todos aquellos atributos y métodos privados y públicos dentro de clases. Y que proteja aquellos datos
    # se deban proteger. Que no se puedan tocar atributos directamente por parte del usuario sin las facilidades que
    # otorga la clase
    
    # Abstracción se refiere a que cualquier usuario de este código sea capaz de utilizar una clase sin necesidad de 
    # conocer la implementación de la misma, es decir, sin saber que hay por detrás.
    
    def __init__(self, hitpoints: int, num_lives:int, damage_per_attack: int): # Método constructor
        self.__hitpoints = hitpoints
        self.__num_lives = num_lives
        self.__damage_per_attack = damage_per_attack
        
    def show_hitpoints(self):
        print(f"Hitpoints: {self.__hitpoints}")
        if self.__hitpoints > 500:
            print("Hitpoints are high")
            
    def show_lives(self):
        print(f"Number of lives: {self.__num_lives}")
        if self.__num_lives > 1:
            print("Wow!! More than one life!")
            
    def show_damage(self):
        print(f"Damage per attack. {self.__damage_per_attack}")
        if self.__damage_per_attack > 50:
            print("Strong player!")
            
    def show_data(self):
        """Show the abilities of the character."""
        print(f"Hitpoints: {self.__hitpoints}")
        self.show_hitpoints()
        print(f"Lives: {self.__num_lives}")
        self.show_lives()
        print(f"Damage per attack: {self.__damage_per_attack}")
        self.show_damage()

    # Estos métodos incluyen el __ delante de su nombre porque son métodos privados, lo mismo ocurre con los atributos
    # Esto está pensado para que otros desarrolladores utilicen nuestra clase de forma correcta y no modifiquen los atributos
    # de los personajes directamente, sino usando los métodos públicos que les proporcionamos. 

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


def separator():
    print("\n")
    print("=" * 20)
    print("\n")

def main():
    #Create a videogame character with hitpoints, lives, and damage per attack
    my_character = Character(
        hitpoints=100,
        num_lives=3,
        damage_per_attack=20
    )
    
    my_character.show_data()
    
    separator()
    
    print("Evolution!!")
    my_character.evolve()
    my_character.show_data()
    
if __name__=="__main__":
    main()