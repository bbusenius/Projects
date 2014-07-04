"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)
from collections import Counter as count

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def average(numbers):
    """
    Calculates the average or mean of a list of numbers
    """
    return float(sum(numbers)) / len(numbers)


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    retval = 0
    counter = count(hand).most_common()
    if len(hand) > 0:
        for item in counter:
            if item[0] * item[1] > retval:
                retval = item[0] * item[1]
    return retval


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    scores = []
    possible_sequences = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    dummy_values = [scores.append(score(held_dice + hand)) for hand in possible_sequences] 
    return average(scores)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    # Generate a set of all possible bitmasks (binary combinations) for the 
    # given length of the hand e.g. set([(0, 1), (1, 0), (0, 0), (1, 1)]) 
    masks = gen_all_sequences((0,1), len(hand))

    # Loop over the bitmasks and build a set of tuples
    # Only add a number to the tuple if the bitmask shows a 1
    retval = []
    for sequence in masks:
        temp = []
        counter = 0
        for bit in sequence:
            if bit == 1:
                temp.append(hand[counter])
            counter += 1
        retval.append(tuple(temp))

    return set(retval)



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand, tuple
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    # 1. Get all of the possible holds for the hand.
    holds = gen_all_holds(hand)

    # 2. Loop over all possible holds and calculate the expected
    ev_holds = []
    for possible_hold in holds:
        exp_value = expected_value(possible_hold, num_die_sides, len(hand) - len(possible_hold))
        ev_holds.append([exp_value, possible_hold])
     
    # 3. Retun the hold with the highest expected value as a tuple with its 
    # corresponding expected value as the first element in e.g.: (0.0, ())
    return tuple(max(ev_holds))


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    #num_die_sides = 6
    #hand = (1, 1, 1, 5, 6)
    #hand_score, hold = strategy(hand, num_die_sides)
    #print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    pass
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
#import poc_yahtzee_testsuite as score_testsuite
#score_testsuite.run_score(score)
#score_testsuite.run_ev(expected_value)
#score_testsuite.run_strategy(strategy)
#import  poc_yahtzee_testsuite as expected_value_testsuite
#expected_value_testsuite.run_suite(expected_value)
