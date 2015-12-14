import unittest
import math

def multiple_upto(n, r):
    def helper(n, r, divisor):
        # Base case
        if r < 2:
            return False
        elif n % divisor == 0:
            return True
        elif divisor >= r:
            return False
        # Recursive case
        else:
            return helper(n, r, divisor + 1)
    return helper(n, r, 2)


def is_prime(n):
    def helper(n, i):
        if (n % i == 0 and n != 2 and n != i) or n < 2:
            return False
        else:
            if i < math.sqrt(n):
                return helper(n, i+1)
            else:
                return True
    return helper(n, 2)


class test_multiple_upto(unittest.TestCase):
    """
    Unit test.
    """
    def test_multiple_upto(self):
        assert multiple_upto(10, 3) == True
        assert multiple_upto(30, 2) == True
        assert multiple_upto(25, 6) == True
        assert multiple_upto(11, 10) == False
        assert multiple_upto(2, 10) == True
        assert multiple_upto(9, 5) == True
        assert multiple_upto(7, 6) == False
        assert multiple_upto(4, 3) == True
        assert multiple_upto(1, 4) == False
        assert multiple_upto(8, 9) == True
        assert multiple_upto(9, 2) == False
        assert multiple_upto(1, 2) == False


class test_is_prime(unittest.TestCase):
    """
    Unit test.
    """
    def test_is_prime(self):
        assert is_prime(1) == False
        assert is_prime(2) == True
        assert is_prime(19) == True
        assert is_prime(41) == True
        assert is_prime(67) == True
        assert is_prime(4) == False
        assert is_prime(3) == True
        assert is_prime(5) == True


# Run unit tests
if __name__ == "__main__":
    unittest.main()

