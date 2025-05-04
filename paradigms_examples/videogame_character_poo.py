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




def main():
    #Create a videogame character with hitpoints, lives, and damage per attack
    my_character = Character(
        hitpoints=100,
        num_lives=3,
        damage_per_attack=20
    )
    
    my_character.show_data()
    
if __name__=="__main__":
    main()