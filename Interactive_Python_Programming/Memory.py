# Implementation of card game - Memory

import simplegui
import random

canvas_height = 100
canvas_width = 800
card_width = canvas_width / 16.0
turns = 0
label_text = "Turns = "

# Helper function to initialize globals
def new_game():
    global state, deck, exposed, card1_index, card2_index, turns
    
    # State for managing turns 
    state = 0
    
    # Track cards that are clicked on
    card1_index = ""
    card2_index = ""
    
    # Create a deck of cards
    deck = range(0, 8) + range(0, 8)
    
    # List for keeping track of exposed cards
    exposed = [False] * len(deck)
    
    # Shuffle the cards
    random.shuffle(deck)
    
    # Number of turns
    turns = 0
    label.set_text(label_text + str(turns))
     
# Define event handlers
def mouseclick(pos):
    global state, card1_index, card2_index, turns
    
    # Get the index of the card under the mouse on click 
    # I barely understand why this works
    mouse_x_position = pos[0]
    current_card_index = mouse_x_position / 50
    
    # Set the exposed value to True when a card is clicked on
    # Only do stuff if an unexposed card is clicked on
    if exposed[current_card_index] != True:
        exposed[current_card_index] = True
    
        # Track the state of the game
        if state == 0:
            state = 1
            card1_index = current_card_index
            card2_index = ""
        elif state == 1:
            state = 2
            card2_index = current_card_index
            
            #Increment the turn counter and redraw the label
            turns += 1
            label.set_text("Turns = " + str(turns))
        else:
            #See if the flipped cards match
            if deck[card1_index] != deck[card2_index]:
                exposed[card1_index] = False
                exposed[card2_index] = False
                   
            state = 1
            card1_index = current_card_index
            card2_index = ""
                        
# Cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck
    
    # Position the cards
    position = [card_width / 2, 0] 
                    
    # Draw cards and values
    for card_index, card_value in enumerate(deck):
       
        # See if a card is exposed
        if exposed[card_index]:
            canvas.draw_text(str(card_value), (position[0] - 8.0, (position[1] + canvas_height / 2) + 10), 35, 'White')

        else:
            canvas.draw_line((position[0], 0), (position[0], canvas_height), card_width - 1, 'Green')
            
        # Space the cards
        position[0] += card_width
   

# Create frame and add a button and labels
frame = simplegui.create_frame("Memory", canvas_width, canvas_height)
frame.add_button("Reset", new_game)
label = frame.add_label("")
label.set_text(label_text + str(turns))

# Register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# Get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric