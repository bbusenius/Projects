"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2

if DESKTOP:
    import matplotlib.pyplot as plt
    #import alg_project4_solution as student
    import Dynamic_Programming as student
else:
    import simpleplot
    import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string    representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list



# Load the needed files
human_eyeless_prot = read_protein(HUMAN_EYELESS_URL)
fly_eyeless_prot = read_protein(FRUITFLY_EYELESS_URL)
scoring_matrix = read_scoring_matrix(PAM50_URL)
pax_prot = read_protein(CONSENSUS_PAX_URL)

# Question 1 - Compute local alignment for human eyless protein and fly eyeless protein
#print student.compute_local_alignment(human_eyeless_prot, fly_eyeless_prot, scoring_matrix, student.compute_alignment_matrix(human_eyeless_prot, fly_eyeless_prot, scoring_matrix, False))

# Question 2 
dashless_human = 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQ'
dashless_fly = 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ'
# Human vs. PAX Domain
human_pax = student.compute_global_alignment(dashless_human, pax_prot, scoring_matrix, student.compute_alignment_matrix(dashless_human, pax_prot, scoring_matrix, True))
# Fly vs. PAX Domain
fly_pax = student.compute_global_alignment(dashless_fly, pax_prot, scoring_matrix, student.compute_alignment_matrix(dashless_fly, pax_prot, scoring_matrix, True))

def compute_agreement(seq_x, seq_y):

    len_x = len(seq_x)
    len_y = len(seq_y)

    assert len_x == len_y

    similarities = 0
    for char in range(len_x):
        if seq_x[char] == seq_y[char]:
            similarities += 1

    return (float(similarities) / len_x) * 100

#print compute_agreement(human_pax[1], human_pax[2])


# Question 7

def compute_edit_dist(seq_x, seq_y):
    len_x = len(seq_x)
    len_y = len(seq_y)

    #assert len_x == len_y

    s_matrix = student.build_scoring_matrix(set(['a','b','c']), 1, -1, -1)

    score = student.compute_global_alignment(seq_x, seq_y, s_matrix, student.compute_alignment_matrix(seq_x, seq_y, s_matrix, True)) 
    
    return (len_x + len_y) - score[0]
    
print compute_edit_dist('aab', 'aaa')
