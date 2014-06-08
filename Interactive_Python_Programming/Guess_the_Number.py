# Guess the number game

import simplegui, random

# Initialize global variables
count = 0
remaining_guesses = 7
secret_number = random.randint(0, 100)
player_guess = ""	
state = ""
level = "0 to 100"

# Helper functions
# Helper function to start and restart the game
def new_game(number): 
    """Resets global variables and starts a new game."""
    global secret_number, state, count, player_guess
    count = 0
    secret_number = number
    player_guess = ""
    state  = ""
    output()    

# Helper function for printing to the screen 
def output():
    """Prints game messages to the console."""   
    if count == 0:
        print "<---------- New Game ---------->"
        print "Range is from %s" %level
    elif count != 0:
        print "Guess was " + str(player_guess)
        
    if remaining_guesses != 0 and float(player_guess) != float(secret_number):
        print "Number of remaining guesses is " + str(remaining_guesses)
    
    # Only print the state if it's not empty
    if len(state) != 0:    
        print state
        
    print
    
# Event handlers
def range100():
    """Generates a random number between 
    0 and 100 and starts a new game
    """
    global level, remaining_guesses
    level = "0 to 100"
    remaining_guesses = 7
    new_game(random.randrange(0, 100))

def range1000():
    """Generates a random number between 
    0 and 1000 and starts a new game.
    """
    global level, remaining_guesses
    level = "0 to 1000"
    remaining_guesses = 10
    new_game(random.randrange(0, 1000))
    
def input_guess(guess):
    """ Updates the global variables 
    every time the user makes a guess.
    """
    global count, remaining_guesses, player_guess, secret_number, state
    player_guess = int(guess)
    count += 1
    remaining_guesses = remaining_guesses - 1

    if level == "0 to 100" and count > 6 and player_guess != secret_number:
        state = "You lose! Try again?"
        output()
        range100()
    elif level == "0 to 1000" and count > 9 and player_guess != secret_number: 
        state = "You lose! Try again?"
        output()
        range1000()    
    elif player_guess < secret_number:
        state = "Higher!"
        output()
    elif player_guess > secret_number:
        state = "Lower!"
        output()
    elif player_guess == secret_number:
        state = "You are correct! You win!"
        output()
        
        # Start a new game
        if level == "0 to 100":
            range100()
        elif level == "0 to 1000":
            range1000()
    else:
        state = "Sad programmer"
    
    # Clear the input after submission    
    input_box.set_text("");
    
# Create frame
frame = simplegui.create_frame("Testing", 200, 200, 250)
frame.set_canvas_background("#000")

# Register event handlers for control elements
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
input_box = frame.add_input("Guess the number", input_guess, 200)

# Call new_game and start frame
frame.start()
output()