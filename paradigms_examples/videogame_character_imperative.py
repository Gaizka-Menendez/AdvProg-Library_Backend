# This type of paradigm is based on the idea of a sequence of instructions that are executed in order.
# Is little resistent to changes, because if you change the order of the instructions, the program will not work as expected.


# Check abilities of the videogame character:
my_character = [100, 3, 20] # Hitpoints, lives, damage per attack
# Show hitpoints:
print(f"Hitpoints: {my_character[0]}")
if my_character[0] > 500:
    print("Hitpoints are high")
# Show number of lives:
print(f"Lives: {my_character[1]}")
if my_character[1] > 1:
    print("Wow!! More than one life!")
# Show damage per attack
print(f"Damage per attack: {my_character[2]}")
if my_character[2] > 50:
    print("Strong player!")