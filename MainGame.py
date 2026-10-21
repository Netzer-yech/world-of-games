# The entry point of World Of Games
from Live import welcome, load_game

# if statement run only if this file is executed. for other imports of this file the if statement is skipped
if __name__ == "__main__":
    
# input function write a message to the console and stored user input in the mane variable
    name = input("Please enter your name: ")   # input function write a message to the console and stored user input in the mane variable

# printing the welcome message with the name variable
    print(welcome(name))                       

# execute load game function within the if statement
    load_game()