# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
status_message = "Hit or Stand?"
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        msg = "Hand contains: "
        for i in range(len(self.cards)):
            msg += str(self.cards[i]) + " "
        return msg

    def add_card(self, card):
        # add a card object to a hand
        return self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        
        # Compute the base value of a hand
        ace = False
        self.hand_value = 0
        for card in self.cards:
            card_value = VALUES[card.get_rank()]
            self.hand_value += card_value
            if card.rank == "A":
                ace = True
                
        # Change the value of the hand if the hand has an ace
        if ace == False:
            self.hand_value = self.hand_value
        elif ace:
            if self.hand_value + 10 <= 21:
                self.hand_value = self.hand_value + 10
            else:
                self.hand_value = self.hand_value
                
        return self.hand_value
           
    def draw(self, canvas, pos):
        # Draw a hand on the canvas, use the draw method for cards
        for c in self.cards:
            c.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        return random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()           
    
    def __str__(self):
        # return a string representing the deck
        msg = "Deck contains: "
        for i in range(len(self.deck)):
            msg += str(self.deck[i]) + " "
        return msg


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score, status_message
    
    # Reset global variables :-(
    outcome = ""
    status_message = "Hit or Stand?"
    
    # If the player is in the middle of a hand when he tries to 
    # deal, he loses a point
    if in_play:
        outcome = "You forfeit. You lose!"
        status_message = "Deal again?"
        in_play = False
        score -= 1

    # Create a deck of cards with the Deck class
    deck = Deck()
    
    # Create new hands for the dealer and player 
    player_hand = Hand()
    dealer_hand = Hand()
    
    # Shuffle the deck
    deck.shuffle()
    
    # Deal hands, store player and dealer hands in a global variable
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    #print deck
    #print "Player hand: " + str(player_hand)
    #print "Dealer hand: " + str(dealer_hand)
    #print
    
    in_play = True

def hit():
    global outcome, in_play, status_message, score
    # if the hand is in play, hit the player
    if in_play and player_hand.get_value() < 21:
        player_hand.add_card(deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = "You busted! You Lose!"
            status_message = "Try again?"
            in_play = False
            score -= 1
       
def stand():
    global in_play, outcome, score, status_message
    in_play = True
    # If hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while in_play and dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
        
        if dealer_hand.get_value() > 21:
            outcome = "The dealer busted!"
            status_message = "Play again?"
            in_play = False
            score += 1
    
    # Assign a message to outcome, update in_play and score
    if in_play:
        if player_hand.get_value() <= dealer_hand.get_value():
            outcome = "You lose!"
            status_message = "Would you like to try again?"
            in_play = False
            score -= 1
        else:
            outcome = "You win!"
            status_message = "New deal?"
            in_play = False
            score += 1

# draw handler    
def draw(canvas):
    global outcome
    
    #Draw game title, outcome, status_message and score 
    canvas.draw_text("Blackjack", (20, 35), 20, 'White')
    canvas.draw_text(outcome + " " + status_message, (100, 440), 16, 'Yellow')
    canvas.draw_text("Score: " + str(score), (485, 35), 21, 'Yellow')
    
    # Draw player and dealer hands on the canvas
    canvas.draw_text("Dealer hand:", (100, 115), 16, 'White')
    dealer_hand.draw(canvas, [100, 130])
    canvas.draw_text("Player hand:", (100, 285), 16, 'White')
    player_hand.draw(canvas, [100, 300])
    
    # Draw debugging strings
    #canvas.draw_text("Player hand: " + str(player_hand) + "--- " + str(player_hand.get_value()), (20, 555), 14, 'White')
    #canvas.draw_text("Dealer hand: " + str(dealer_hand) + "--- " + str(dealer_hand.get_value()), (20, 575), 14, 'White')

    # Cover the dealer's card in the hole
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_SIZE[0] / 2, 130 + CARD_SIZE[1] / 2], CARD_BACK_SIZE)
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Black")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()