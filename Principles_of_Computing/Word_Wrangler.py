"""
Student code for Word Wrangler game
"""

import urllib2
#import codeskulptor
#import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    # Loop over the list and add elements to a new list if 
    # they don't already exist in the new list.
    list2 = []
    for item in list1:
        if item not in list2:
            list2.append(item)
    return list2

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    return [val for val in list1 if val in list2] 

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    #Make copies of the list arguments 
    list1 = list(list1)
    list2 = list(list2) 
    # Use numbers to compare. 
    # We'll have to assign number values to letters later.
    list3 = []
    # Merge algorithm
    while list1 and list2:
        if list1[0] <= list2[0]:
            item = list1.pop(0)
            list3.append(item)
        else:
            item = list2.pop(0)
            list3.append(item)
    # Add anything remaining from the longer list
    list3.extend(list1 if list1 else list2)
    return list3
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    # Split the list into two
    split_point = len(list1) / 2
    lista = list1[:split_point]
    listb = list1[split_point:]

    # Base case
    if len(list1) < 2:
        return list1
    # Recursive case
    else:
        return merge(merge_sort(lista), merge_sort(listb)) 


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    # Base case
    if word == '':
        return ['']
    # Recursive case
    else:
        # Split the first letter and the rest of 
        # the word into seperate strings. 
        first = word[0]
        rest = word[1:]
        # Recurstion.
        rest_strings = gen_all_strings(rest)
        temp = []
        for string in rest_strings:
            # Len + 1 because we need to append the first variable 
            # to the end of the last string (I think)  
            for indx in range(len(string) + 1):
                # Make new strings by inserting the first character 
                # at all positions in the original (rest) string and
                # append the new strings to the temp list.
                new_string = string[:indx] + first + string[indx:]
                temp.append(new_string)
        # Concatonate rest_strings and the temp list
        rest_strings += temp
        return rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    retval = []
    for line in netfile.readlines():
        retval.append(line[:-1])
    return retval

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

#import poc_word_wrangler_testsuite as testsuite
#testsuite.run_test1(remove_duplicates)
#testsuite.run_test2(intersect)
#testsuite.run_test3(merge)
#testsuite.run_test4(merge_sort)
#testsuite.run_test5(gen_all_strings)
#testsuite.run_all(remove_duplicates, intersect, merge, merge_sort, gen_all_strings)

# Uncomment when you are ready to try the game
# run()
