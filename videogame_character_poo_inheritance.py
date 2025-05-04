class Character:
    
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
        print(f"Damage per attack: {self.__damage_per_attack}")
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

    def __add_hitpoints(self, new_hitpoints: int):
        self.__hitpoints += new_hitpoints

    def _add_lives(self, new_lives: int):
        self.__num_lives += new_lives
        
    def __add_damage_per_attack(self, new_damage: int):
        self.__damage_per_attack += new_damage

    def evolve(self):   
        self.__add_hitpoints(100)                       
        self._add_lives(1)
        self.__add_damage_per_attack(5)
        
    def greeting(self):
        print("Hi! I am a standard character!")
        

class Warrior(Character):
    
    def __init__(self, hitpoints, num_lives, damage_per_attack):
        super().__init__(hitpoints=hitpoints, num_lives=num_lives, damage_per_attack=damage_per_attack)
     
    # Estamos haciendo override del show data de la clase padre   
    def show_data(self):
        print("Special Character: Warrior")
        super().show_data()
        
    def greeting(self):
        print("Hi! I am a Warrior!")
        

class Wizard(Character):
    
    def __init__(self, hitpoints, num_lives, damage_per_attack, mana):
        super().__init__(hitpoints=hitpoints, num_lives=num_lives, damage_per_attack=damage_per_attack)
        self.__mana = mana
     
    # Estamos haciendo override del show data de la clase padre   
    def show_data(self):
        print("Special Character: Wizard")
        super().show_data()
        print(f"Currrent mana: {self.__mana}")
        
    def greeting(self):
        print("Hi there! Lets do some magical stuff ...")
    
    # self._add_lives(1) no se puede usar porque es un método privado de la clase padre. La solución sería rebajar su 
    # protección de privado a protected (sería pasar de __ a _)    
    def use_mana_for_life(self):
        if self.__mana >= 100:
            self.__mana -= 100
            self._add_lives(1)
        else:
            print("Not enough mana to use for life!")


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
    my_character.greeting()
    
    separator()
    
    print("Evolution!!")
    my_character.evolve()
    my_character.show_data()
    
    separator()
    
    my_warrior = Warrior(
        hitpoints=100,
        num_lives=3,
        damage_per_attack=20
    )
    my_warrior.show_data()
    my_warrior.greeting()
    
    separator()
    
    my_wizard = Wizard(
        hitpoints=100,
        num_lives=3,
        damage_per_attack=20,
        mana=100
    )
    my_wizard.show_data()
    my_wizard.greeting()
    my_wizard.use_mana_for_life()
    my_wizard.show_data()   

   
if __name__=="__main__":
    main()