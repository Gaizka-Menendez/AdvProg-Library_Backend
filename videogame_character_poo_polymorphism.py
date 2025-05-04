from videogame_character_poo_inheritance import *

def main():
    
    character_list = [
        Warrior(
            hitpoints=100,
            num_lives=3,
            damage_per_attack=20
        ),
        Wizard(
            hitpoints=100,
            num_lives=3,
            damage_per_attack=20,
            mana=100
        ),
        Character(
            hitpoints=100,
            num_lives=3,
            damage_per_attack=20
        )
    ]
    
    print(f"Longitud de la lista: {len(character_list)}")
    
    # assert son funciones que nos permiten llevar a cabo comprobaciones
    assert(len(character_list) == 3)
    assert(type(character_list) == type([1,2,3]))
    
    for character in character_list:
        character.show_data()
        character.greeting()
        separator()
    

if __name__ == "__main__":
    main()
    