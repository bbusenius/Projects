# Rock-paper-scissors-lizard-Spock template
import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    # convert name to number using if/elif/else
    if name.lower() == "rock":
        value = 0
    elif name.lower() == "spock":
        value = 1
    elif name.lower() == "paper":
        value = 2
    elif name.lower() == "lizard":
        value = 3
    elif name.lower() == "scissors":
        value = 4
    else:
        value = None
        print "\"%s\" is not a valid option. Choose a different word." % name
        
    return value


def number_to_name(number):
    # convert number to a name using if/elif/else
    if number == 0:
        value = "rock"
    elif number == 1:
        value = "Spock"
    elif number == 2:
        value = "paper"
    elif number == 3:
        value = "lizard"
    elif number == 4:
        value = "scissors"
    else:
        value = None
        print "\"%s\" is not a valid option. Choose a number between 0 and 4." % number
        
    return value    
    

def rpsls(player_guess): 
    
    # print a blank line to separate consecutive games
    print

    # print out the message for the player's choice
    print "Player chooses %s" % player_guess

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_guess)
    
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)

    # convert comp_number to comp_choice using the function number_to_name()
    computer_guess = number_to_name(comp_number)
    
    # print out the message for computer's choice
    print "Computer chooses %s" % computer_guess
    
    # compute difference of comp_number and player_number modulo five
    difference = (comp_number - player_number) % 5

    # use if/elif/else to determine winner, print winner message
    if difference == 0:
        print "Player and computer tie!"
    elif difference > 2:
        print "Player wins!"
    elif difference < 3:
        print "Computer wins!"
    else:
        print "Something went wrong!"
            
    
# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")



