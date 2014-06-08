import random, time

# Helper functions
def get_responses(bad):
    """
    Returns a list of possible answers from the mystical octosphere.
    Answers are based on whether we want to be nice or not.
    
    Args:
        bad: Boolean
    """
    
    if bad == False:
        responses = ["Yes, for sure!", "Probably yes.", "Seems like yes...", \
             "Definitely not!", "Maybe", \
             "Probably not.", "I really doubt it...", \
             "Not sure, check back later!", "I really can't tell"]
    elif bad == True:
        responses = ["No...", "Hell no!", "Oh God no!", "Fuck no!", \
                     "Fuck you!", "Are you fucking kidding me?"]
    
    return responses

# Delay for suspense during printing
def delay(delay):
    current_time = time.time()
    while time.time() < current_time + delay:
        pass
    
# Main function
def mystical_octosphere(question):
    
    # Add a question mark to the end of the question if it isn't present
    if question[len(question) -1] != "?":
        question = question + "?"
    
    # Ensure the first letter is upper case, trim whitespace
    question = question[0].upper() + question[1: ]
    question = question.strip()
    
    # Get the response list
    responses = get_responses(bad = True)
    
    # Choose a random answer from the response list 
    answer_number = random.randrange(0,len(responses))
    answer_fortune = responses[answer_number]
    
    # Print the output to screen
    print question    
    print "The mystical octosphere is shaken."
    
    print "Waiting..."
    delay(3)
    print "The cloudy liquid swirls, and a reply comes into view..."
    delay(3)
    print "The mystical octosphere says..."
    delay(3)
    print answer_fortune
    print

mystical_octosphere(raw_input("What is your question?"))
