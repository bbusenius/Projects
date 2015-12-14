import unittest

"""
Let us solve the following puzzle: 
If you multiply my grand-son age by four, you know how old I am. Now, if you exchange the two digits of our ages then you have to multiply by three my age to get the age of my grand-son!

1. Write a function exchange of type int -> int that takes an integer x between 10 and 99 and returns an integer which is x whose digits have been exchanged. For instance, exchange 73 = 37.

2. Define is_valid_answer of type int * int -> bool such that is_valid_answer (grand_father_age, grand_son_age) returns true if and only if grand_father_age and grand_son_age verify the constraints of the puzzle.

3. Write a function find : (int * int) -> (int * int) that takes a pair (max_grand_father_age, min_grand_son_age) and returns a solution (grand_father_age, grand_son_age) to the problem, where min_grand_son_age <= grand_son_age < grand_father_age <= max_grand_father_age or (-1, -1) if there was no valid answer in the given range.
"""


def exchange(k):
    return int(str(k)[::-1])

def is_valid_answer(answer):
    grand_father_age, grand_son_age = answer
    if grand_son_age * 4 == grand_father_age and exchange(grand_father_age) * 3 == exchange(grand_son_age):
        return True
    else:
        return False

def find_DEPRECTATED(answer):

    max_grand_father_age, min_grand_son_age = answer
    numlist = [i for i in range(min_grand_son_age, max_grand_father_age + 1)]
    for gsa in numlist:
        for gfa in numlist:
            ages = (gfa, gsa)
            if is_valid_answer(ages):
                return ages
 
    return (-1, -1)

def find(answer):

    max_grand_father_age, min_grand_son_age = answer

    def helper(gsa):
        gfa = gsa * 4
        if gfa > max_grand_father_age:
            return (-1, -1)
        elif is_valid_answer((gfa, gsa)):
            return (gfa, gsa)
        else:
            return helper(gsa + 1)
        
    return helper(min_grand_son_age)


class test_multiple_upto(unittest.TestCase):
    """
    Unit test.
    """
    def test_find(self):
        assert find((99, 10)) != (-1, -1)
        assert find((96, 41)) == (-1, -1)
        assert find((87, 17)) != (-1, -1)
        assert find((78, 27)) == (-1, -1)
        assert find((84, 20)) == (-1, -1)
        assert find((97, 10)) != (-1, -1)
        assert find((63, 11)) == (-1, -1)
        assert find((93, 34)) == (-1, -1)
        assert find((96, 31)) == (-1, -1)
        assert find((74, 20)) == (-1, -1)


# Run unit tests
if __name__ == "__main__":
    unittest.main()

