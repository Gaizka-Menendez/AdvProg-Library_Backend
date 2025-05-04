def show_character_hitpoints(hitpoints: int):
    """Show the hitpoints of the character."""
    print(f"Hitpoints: {hitpoints}")
    if hitpoints > 500:
        print("Hitpoints are high")

def show_character_lives(lives: int):
    """Show the number of lives of the character."""
    print(f"Lives: {lives}")
    if lives > 1:
        print("Wow!! More than one life!")

def show_character_damage(damage: int):
    """Show the damage per attack of the character."""
    print(f"Damage per attack: {damage}")
    if damage > 50:
        print("Strong player!")
        
def show_character_abilities(hitpoints: int, num_lives: int, damage_per_attack: int):
    """Show the abilities of the character."""
    show_character_hitpoints(hitpoints)
    show_character_lives(num_lives)
    show_character_damage(damage_per_attack)

def main():
    # Check the abilities of the videogame character:
    my_character = [100, 3, 20]  # Hitpoints, lives, damage per attack
    # Show hitpoints:
    show_character_hitpoints(my_character[0])
    # Show number of lives:
    show_character_lives(my_character[1])
    # Show damage per attack
    show_character_damage(my_character[2])
    # Show all:
    show_character_abilities(my_character[0], my_character[1], my_character[2])
    
if __name__ == "__main__":
    main()