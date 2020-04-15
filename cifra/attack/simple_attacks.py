""" Module to keep common functions used by caesar and transposition attacks. """
import multiprocessing
import os
from typing import Callable

from cifra.attack.dictionaries import IdentifiedLanguage, identify_language, get_best_result


def _brute_force(assess_function: Callable, **assess_function_args) -> int:
    """ Get ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should not use this function. Use *brute_force_mp* instead.** This
    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.

    :param assess_function: Analysis function to be used.
    :param assess_function_args: Arguments to be used with given *assess_function*.
    :return: key found.
    """
    key_space_length = assess_function_args.pop("key_space_length")
    results = []
    for key in range(1, key_space_length):
        assess_function_args["key"] = key
        results.append(assess_function(**assess_function_args))
    best_key = get_best_result(results)
    return best_key


def _brute_force_mp(assess_function: Callable, **assess_function_args) -> int:
    """ Get ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should use this function instead of *brute_force*.**

    Whereas *brute_force* uses a sequential approach, this function uses
    multiprocessing to improve performance.

    :param assess_function: Analysis function to be used.
    :param assess_function_args: Arguments to be used with given *assess_function*.
    :return: Transposition key found.
    """
    key_space_length = assess_function_args.pop("key_space_length")
    results = []
    with multiprocessing.Pool(_get_usable_cpus()) as pool:
        nargs = ((assess_function_args["ciphered_text"],
                  key,
                  assess_function_args["charset"],
                  assess_function_args["_database_path"])
                 if "charset" in assess_function_args else
                 (assess_function_args["ciphered_text"],
                  key,
                  assess_function_args["_database_path"])
                 for key in range(1, key_space_length))
        results = pool.map(assess_function, nargs)
    best_key = get_best_result(results)
    return best_key


def _assess_key(decipher_function: Callable, **decipher_functions_args) -> (int, IdentifiedLanguage):
    """Decipher text with given key and try to find out if returned text can be identified with any
    language in our dictionaries.

    :param decipher_function: Function to decipher given text.
    :param decipher_functions_args: Key to decipher *ciphered_text*.
    :return: A tuple with used key and an *IdentifiedLanguage* object with assessment result.
    """
    database_path = decipher_functions_args.pop("_database_path")
    deciphered_text = decipher_function(**decipher_functions_args)
    identified_language = identify_language(deciphered_text,
                                            _database_path=database_path)
    return decipher_functions_args["key"], identified_language


def _get_usable_cpus() -> int:
    """Get the number of CPUs the current process can use.

    :return: Number of CPUs the current process can use.
    """
    return len(os.sched_getaffinity(0))