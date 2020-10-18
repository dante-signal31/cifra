# Cryptomath Module
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
from typing import Optional, List, Set


def gcd(a: int, b: int) -> int:
    """ Return the GCD of a and b using Euclid's algorithm.

    :param a: First integer.
    :param b: Second integer.
    :return: The Greatest Common Divisor between two given numbers.
    """
    while a != 0:
        a, b = b % a, a
    return b


def find_mod_inverse(a: int, m: int) -> Optional[int]:
    """ Return the modular inverse of a % m

    Modular inverse is the number x such that a*x % m = 1.

    :param a: First integer.
    :param m: Second integer.
    :return:  Module inverse integer.
    """
    if gcd(a, m) != 1:
        return None  # No mod inverse if a & m aren't relatively prime.
    else:
        # Calculate using the extended Euclidean algorithm:
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3  # Note that // is the integer division operator.
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        result = u1 % m
        return result


def find_factors(number: int) -> List[int]:
    """ Get math factors for this number.

    Number 1 is not returned as factor, because is evident.

    :param number: Number to get factors from.
    :return: A list with found factors.
    """
    factors = []
    for candidate in range(2, number+1):
        if number % candidate == 0:
            factors.append(candidate)
    return factors


def find_common_factors(*factor_lists: List[int]) -> Set[int]:
    """ Get a sequence of lists of factors and return factors common for them all.

    :param factor_lists: A variable length sequence of list. Every list has factors for a number:
    :return: A set with common factors
    """
    common_factors = set(factor_lists[0])
    common_factors.intersection_update(*(set(factors) for factors in factor_lists))
    return common_factors
