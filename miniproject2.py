# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

# 1. initialize global variable
num_range = 100
remaining_guesses = 7
user_guesses = 0
secret_number = random.randrange(0, num_range)

# 2. helper function to start and restart the game
def new_game():
    global secret_number
    secret_number = random.randrange(0, num_range)
    print_new_game_message()
    
def print_new_game_message():
    print "New game. Range is from 0 to ", num_range
    print "Number of remaining guesses is ", remaining_guesses
    print ""
    
def print_lose_message():
    print "You ran out of guesses. The number was ", secret_number
    print ""

def start_game_by_range():
    if num_range == 100:
        range100()
    elif num_range == 1000:
        range1000()

def is_number(number):
    try:
        int(number)
        return True
    except ValueError:
        return False
    
def setGuessesRange(range, countOfGuesses):
    global num_range, remaining_guesses
    num_range = range
    remaining_guesses = countOfGuesses
    
    
# 4. define event handlers for control panel
def range100():    
    setGuessesRange(100, 7)
    new_game()
    
def range1000(): 
    setGuessesRange(1000, 10)
    new_game()
    
def input_guess(guess):
    global remaining_guesses, user_guesses
    
    if not is_number(guess):
        print "Please input a valid integer\n"
        return
    
    user_guesses = int(guess)
    remaining_guesses = remaining_guesses - 1

    print "Guess was ", user_guesses
    print "Number of remaining guesses is ", remaining_guesses
    
    if user_guesses == secret_number:
        print "Correct!\n"
        start_game_by_range()
    elif remaining_guesses == 0:
        print_lose_message()
        start_game_by_range()
    elif user_guesses < secret_number:
        print "Higher!\n"
    elif user_guesses > secret_number:
        print "Lower!\n"     
        
# 5. create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# 6. egister event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

# 7. call new_game 
new_game()


# always remember to check your completed program against the grading rubric
