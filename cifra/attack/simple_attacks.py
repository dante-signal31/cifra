""" Module to keep common functions used by caesar and transposition attacks. """
import math
import multiprocessing
import os
from typing import Callable, Iterator, Optional, Union

from cifra.attack.dictionaries import IdentifiedLanguage, identify_language, get_best_result, Dictionary


def _integer_key_generator(maximum_key: int) -> Iterator[int]:
    """ Iterate through a range from 1 to maximum_key. """
    for i in range(1, maximum_key):
        yield i


def _dictionary_word_key_generator(_database_path: Optional[str] = None) -> Iterator[str]:
    """ Iterate through every word in our dictionaries. """
    available_languages = Dictionary.get_available_languages(_database_path)
    for language in available_languages:
        with Dictionary.open(language, False, _database_path) as language_dictionary:
            words = language_dictionary.get_all_words()
            for word in words:
                yield word


def _brute_force(key_generator: Union[Iterator[int], Iterator[str]],
                 assess_function: Callable,
                 **assess_function_args) -> Union[int, str]:
    """ Get ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should not use this function. Use *brute_force_mp* instead.** This
    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.

    :param key_generator: Generator to produce keys. To attack a Caesar Cipher
        you will use an _integer_key_generator() while when you attack a Vigenere
        you will use _word_key_generator().
    :param assess_function: Analysis function to be used.
    :param assess_function_args: Arguments to be used with given *assess_function*.
    :return: key found.
    """
    # key_space_length = assess_function_args.pop("key_space_length")
    results = []
    # for key in range(1, key_space_length):
    for key in key_generator:
        assess_function_args["key"] = key
        (word, identified_language) = assess_function(**assess_function_args)
        if identified_language.winner is not None and math.isclose(identified_language.winner_probability, 1, abs_tol=0.01):
            # Early return. We've found a result good enough to not continue searching
            # any further.
            return word
        else:
            results.append((word, identified_language))
    best_key = get_best_result(results)
    return best_key


def _brute_force_mp(key_generator: Union[Iterator[int], Iterator[str]],
                    assess_function: Callable,
                    **assess_function_args) -> int:
    """ Get ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should use this function instead of *brute_force*.**

    Whereas *brute_force* uses a sequential approach, this function uses
    multiprocessing to improve performance.

    :param key_generator: Generator to produce keys. To attack a Caesar Cipher
        you will use an _integer_key_generator() while when you attack a Vigenere
        you will use _word_key_generator().
    :param assess_function: Analysis function to be used.
    :param assess_function_args: Arguments to be used with given *assess_function*.
    :return: Transposition key found.
    """
    # key_space_length = assess_function_args.pop("key_space_length")
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
                 for key in key_generator)
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
    in_memory = decipher_functions_args.pop("in_memory")
    deciphered_text = decipher_function(**decipher_functions_args)
    identified_language = identify_language(deciphered_text,
                                            in_memory=in_memory,
                                            _database_path=database_path)
    return decipher_functions_args["key"], identified_language


def _assess_key_in_memory(decipher_function: Callable, **decipher_functions_args) -> (int, IdentifiedLanguage):
    """Decipher text with given key and try to find out if returned text can be identified with any
    language in our dictionaries.

    :param decipher_function: Function to decipher given text.
    :param decipher_functions_args: Key to decipher *ciphered_text*.
    :return: A tuple with used key and an *IdentifiedLanguage* object with assessment result.
    """
    database_path = decipher_functions_args.pop("_database_path")
    deciphered_text = decipher_function(**decipher_functions_args)
    identified_language = identify_language_in_memory(deciphered_text,
                                            _database_path=database_path)
    return decipher_functions_args["key"], identified_language


def _get_usable_cpus() -> int:
    """Get the number of CPUs the current process can use.

    :return: Number of CPUs the current process can use.
    """
    return len(os.sched_getaffinity(0))