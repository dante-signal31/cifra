#!/usr/bin/env python3
"""
 Cifra

 Programmed by: Dante Signal31
 email: dante.signal31@gmail.com
 website: https://github.com/dante-signal31/cifra

 Console command to crypt and decrypt texts using classic methods. It also
 performs crypto attacks against those methods. I'm implementing this while
 I read Al Sweigart's "Cracking Codes with Python".
"""
from __future__ import annotations
import argparse
import os
import sys
# import tempfile
from typing import List, Dict, Callable, Optional
from enum import Enum, auto

import cifra.cipher.affine
import cifra.cipher.caesar
import cifra.cipher.common
import cifra.cipher.substitution
import cifra.cipher.transposition
import cifra.cipher.vigenere
import cifra.attack.affine
import cifra.attack.caesar
import cifra.attack.substitution
import cifra.attack.transposition
import cifra.attack.vigenere
from cifra.attack.dictionaries import Dictionary


# if os.getenv("CIFRA_DEBUG", 0) == "1":
#     # TODO: Check Travis CI sets it corresponding CIFRA_DEBUG env var to 1.
#     DICTIONARY_FOLDER = tempfile.mkdtemp()
# else:
#     DICTIONARY_FOLDER = "~/.cifra/"


class MessageOperation(Enum):
    """ Possible operations over text messages (bot ciphered and plain)."""
    cipher = auto()
    decipher = auto()
    attack = auto()

    @staticmethod
    def from_string(name: str) -> MessageOperation:
        """ Create an MessageOperation enum from an operation name string.

        :param name: Name string
        :return: A message operation with that name.
        """
        if name == "cipher":
            return MessageOperation.cipher
        elif name == "decipher":
            return MessageOperation.decipher
        elif name == "attack":
            return MessageOperation.attack


class Algorithm(Enum):
    """ Algorithms implemented in cifra."""
    caesar = auto()
    substitution = auto()
    transposition = auto()
    affine = auto()
    vigenere = auto()

    @staticmethod
    def from_string(name: str) -> Algorithm:
        """ Create an Algorithm enum from an algorithm name string.

        :param name: Name string
        :return: An algorithm with that name.
        """
        if name == "caesar":
            return Algorithm.caesar
        elif name == "substitution":
            return Algorithm.substitution
        elif name == "transposition":
            return Algorithm.transposition
        elif name == "affine":
            return Algorithm.affine
        elif name == "vigenere":
            return Algorithm.vigenere


# CIPHERING_ALGORITHMS = {"caesar", "substitution", "transposition", "affine",
#                         "vigenere"}
CIPHERING_ALGORITHMS = {key for key in Algorithm.__members__.keys()}

STRING_KEY_ALGORITHMS = {"substitution", "vigenere"}

INTEGER_KEY_ALGORITHMS = CIPHERING_ALGORITHMS - STRING_KEY_ALGORITHMS


def _check_is_file(_string: str) -> str:
    """ Check this string really points to a valid file.

    :param _string: Pathname to file.
    :return: Given string if its actually a file.
    """
    if os.path.isfile(_string):
        return _string
    else:
        raise argparse.ArgumentTypeError("{0} file does "
                                         "not exists.".format(_string))


def parse_arguments(args: list = None) -> Dict[str, str]:
    """ Parse given arguments to get running configuration.

    :param args: Arguments given from shell to console launcher.
    :return: A Dict with obtained values.
    """
    arg_parser = argparse.ArgumentParser(description="Console command to crypt "
                                                     "and decrypt texts using "
                                                     "classic methods. It also "
                                                     "performs crypto attacks "
                                                     "against those methods.\n",
                                         epilog="Follow cifra development at: "
                                                "<https://github.com/dante-signal31/cifra>")
    cifra_subparsers = arg_parser.add_subparsers(help="Available modes",
                                                 dest="mode",
                                                 required=True)
    # DICTIONARY MANAGEMENT.
    dictionary_parser = cifra_subparsers.add_parser(name="dictionary",
                                                    help="Manage dictionaries to "
                                                         "perform crypto attacks.")
    dictionary_actions_subparser = dictionary_parser.add_subparsers(help="Action to perform.",
                                                                    dest="action")
    #   DICTIONARY CREATION.
    dictionary_create_parser = dictionary_actions_subparser.add_parser(name="create",
                                                                       help="Create a dictionary of unique words.")
    dictionary_create_parser.add_argument("dictionary_name",
                                          type=str,
                                          help="Name for the dictionary to create.",
                                          metavar="NEW_DICTIONARY_NAME")
    dictionary_create_parser.add_argument("-i", "--initial_words_file",
                                          type=_check_is_file,
                                          help="Optionally you can load in the dictionary words located in a text file",
                                          metavar="PATH_TO FILE_WITH_WORDS")
    #   DICTIONARY REMOVAL.
    dictionary_delete_parser = dictionary_actions_subparser.add_parser(name="delete",
                                                                       help="Remove an existing dictionary.")
    dictionary_delete_parser.add_argument("dictionary_name",
                                          type=str,
                                          help="Name for the dictionary to delete.",
                                          metavar="DICTIONARY_NAME_TO_DELETE")
    #   DICTIONARY UPDATING.
    dictionary_update_parser = dictionary_actions_subparser.add_parser(name="update",
                                                                       help="Add words to an existing dictionary.")
    dictionary_update_parser.add_argument("dictionary_name",
                                          type=str,
                                          help="Name for the dictionary to update with additional words.",
                                          metavar="DICTIONARY_NAME_TO_UPDATE")
    dictionary_update_parser.add_argument("words_file",
                                          type=_check_is_file,
                                          help="Pathname to a file with words to add to dictionary",
                                          metavar="PATH_TO_FILE_WITH_WORDS")
    #   DICTIONARY LISTING.
    _ = dictionary_actions_subparser.add_parser(name="list",
                                                help="Show existing dictionaries.")
    # CIPHER MANAGEMENT.
    cipher_parser = cifra_subparsers.add_parser(name="cipher",
                                                help="Cipher a text using a key.")
    cipher_parser.add_argument("algorithm",
                               choices=CIPHERING_ALGORITHMS,
                               type=str,
                               help="Algorithm to use to cipher.",
                               metavar="ALGORITHM_NAME")
    cipher_parser.add_argument("key",
                               type=str,
                               help="Key to use to cipher.",
                               metavar="CIPHERING_KEY")
    cipher_parser.add_argument("file_to_cipher",
                               type=_check_is_file,
                               help="Path to file with text to cipher.",
                               metavar="FILE_TO_CIPHER")
    cipher_parser.add_argument("-o", "--ciphered_file",
                               type=str,
                               help="Path to output file to place ciphered text. If not used then"
                                    "ciphered text will be dumped to console.",
                               metavar="OUTPUT_CIPHERED_FILE")
    cipher_parser.add_argument("-c", "--charset",
                               type=str,
                               help=f"Default charset is: {cifra.cipher.common.DEFAULT_CHARSET}, but you can set here "
                                    f"another.",
                               metavar="CHARSET")
    # DECIPHERING MANAGEMENT
    decipher_parser = cifra_subparsers.add_parser(name="decipher",
                                                  help="Decipher a text using a key.")
    decipher_parser.add_argument("algorithm",
                                 choices=CIPHERING_ALGORITHMS,
                                 type=str,
                                 help="Algorithm to use to decipher.",
                                 metavar="ALGORITHM_NAME")
    decipher_parser.add_argument("key",
                                 type=str,
                                 help="Key to use to decipher.",
                                 metavar="CIPHERING_KEY")
    decipher_parser.add_argument("file_to_decipher",
                                 type=_check_is_file,
                                 help="Path to file with text to decipher.",
                                 metavar="FILE_TO_DECIPHER")
    decipher_parser.add_argument("-o", "--deciphered_file",
                                 type=str,
                                 help="Path to output file to place deciphered text. If not used then"
                                      "deciphered text will be dumped to console.",
                                 metavar="OUTPUT_DECIPHERED_FILE")
    decipher_parser.add_argument("-c", "--charset",
                                 type=str,
                                 help=f"Default charset is: {cifra.cipher.common.DEFAULT_CHARSET}, but you can set here "
                                      f"another.",
                                 metavar="CHARSET")
    # ATTACK MANAGEMENT
    attack_parser = cifra_subparsers.add_parser(name="attack",
                                                help="Attack a ciphered text to get its plain text")
    attack_parser.add_argument("algorithm",
                               choices=CIPHERING_ALGORITHMS,
                               type=str,
                               help="Algorithm to attack.",
                               metavar="ALGORITHM_NAME")
    attack_parser.add_argument("file_to_attack",
                               type=_check_is_file,
                               help="Path to file with text to attack.",
                               metavar="FILE_TO_ATTACK")
    attack_parser.add_argument("-o", "--deciphered_file",
                               type=str,
                               help="Path to output file to place deciphered text. If not used then"
                                    "deciphered text will be dumped to console.",
                               metavar="OUTPUT_DECIPHERED_FILE")
    attack_parser.add_argument("-c", "--charset",
                               type=str,
                               help=f"Default charset is: {cifra.cipher.common.DEFAULT_CHARSET}, but you can set here "
                                    f"another.",
                               metavar="CHARSET")

    parsed_arguments = vars(arg_parser.parse_args(args))
    filtered_parser_arguments = {key: value for key, value in parsed_arguments.items()
                                 if value is not None}
    return filtered_parser_arguments


def _output_result(result: str, arguments: Dict[str, str]) -> None:
    """ Helper generic function to output resulting content.

    :param result: String with resulting processed content. If an output file has been requested then result is
    written to that file or to screen otherwise.
    :param arguments: Console parsed arguments.
    """
    if ("ciphered_file" in arguments) or ("deciphered_file" in arguments):
        output_filename = arguments["ciphered_file"] if "ciphered_file" in arguments else arguments["deciphered_file"]
        with open(output_filename, mode="w") as output_file:
            output_file.write(result)
            output_file.flush()
    else:
        print(result)


def _process_file_with_key(_input: str, algorithm: Algorithm, key: str,
                           operation: MessageOperation, charset: str = None) -> str:
    """ Helper generic function to process files to cipher and decipher.

    :param _input: Input file pathname.
    :param algorithm: Algorithm to apply for given operation.
    :param key: Key to use with algorithm.
    :param operation: Whether cipher, decipher or attack given input.
    :param charset: Charset to use with given algorithm. If selected algorithm does not use a charset
    then this is ignored.
    :return: Processed resulting string.
    """
    with open(_input, mode="r") as input_file:
        content_to_process = input_file.read()
    process_function = _get_ciphering_function(algorithm) \
        if operation == MessageOperation.cipher \
        else _get_deciphering_function(algorithm)
    process_key = key if algorithm.name in STRING_KEY_ALGORITHMS else int(key)
    if charset is not None:
        processed_content = process_function(content_to_process,
                                             process_key,
                                             charset)
    else:
        processed_content = process_function(content_to_process,
                                             process_key)
    return processed_content


def _attack_file(input_filepath: str, algorithm: Algorithm, charset: str = None, _database_path=None) -> str:
    """ Apply crypto attack to file to get most likely plain text.

    :param input_filepath: Pathname of ciphered text file.
    :param algorithm: Algorithm to attack.
    :param charset: Charset to use with given algorithm. If selected algorithm does not use a charset
    then this is ignored.
    :param _database_path: Absolute pathname to database file. Usually you don't set this parameter,
    but it is useful for tests.
    :return: Most likely original plain text.
    """
    with open(input_filepath, mode="r") as input_file:
        ciphered_content = input_file.read()
    attack_function = _get_attack_function(algorithm)
    if algorithm == Algorithm.substitution:
        (key, _) = attack_function(ciphered_content, charset, _database_path=_database_path) \
            if charset is not None else \
            attack_function(ciphered_content, _database_path=_database_path)
    else:
        key = attack_function(ciphered_content, charset) if charset is not None else attack_function(ciphered_content,
                                                                                                     _database_path=_database_path)

    deciphered_text = _process_file_with_key(input_filepath, algorithm, key, MessageOperation.decipher, charset) \
        if charset is not None else \
        _process_file_with_key(input_filepath, algorithm, key, MessageOperation.decipher, charset)
    return deciphered_text


def _get_ciphering_function(algorithm: Algorithm) -> Callable:
    """ Get ciphering function for this algorithm.

    :param algorithm: Algorithm name.
    :return: A ciphering function. None if function with that
    name was not found.
    """
    ciphering_function = None
    if algorithm == Algorithm.caesar:
        ciphering_function = cifra.cipher.caesar.cipher
    elif algorithm == Algorithm.affine:
        ciphering_function = cifra.cipher.affine.cipher
    elif algorithm == Algorithm.substitution:
        ciphering_function = cifra.cipher.substitution.cipher
    elif algorithm == Algorithm.transposition:
        ciphering_function = cifra.cipher.transposition.cipher
    elif algorithm == Algorithm.vigenere:
        ciphering_function = cifra.cipher.vigenere.cipher
    return ciphering_function


def _get_deciphering_function(algorithm: Algorithm) -> Callable:
    """ Get deciphering function for this algorithm.

    :param algorithm: Algorithm name.
    :return: A deciphering function. None if function with that
    name was not found.
    """
    deciphering_function = None
    if algorithm == Algorithm.caesar:
        deciphering_function = cifra.cipher.caesar.decipher
    elif algorithm == Algorithm.affine:
        deciphering_function = cifra.cipher.affine.decipher
    elif algorithm == Algorithm.substitution:
        deciphering_function = cifra.cipher.substitution.decipher
    elif algorithm == Algorithm.transposition:
        deciphering_function = cifra.cipher.transposition.decipher
    elif algorithm == Algorithm.vigenere:
        deciphering_function = cifra.cipher.vigenere.decipher
    return deciphering_function


def _get_attack_function(algorithm: Algorithm) -> Callable:
    """ Get attack function for this algorithm.

    :param algorithm: Algorithm name.
    :return: A ciphering function. None if function with that
    name was not found.
    """
    attack_function = None
    if algorithm == Algorithm.caesar:
        attack_function = cifra.attack.caesar.brute_force_mp
    elif algorithm == Algorithm.affine:
        attack_function = cifra.attack.affine.brute_force_mp
    elif algorithm == Algorithm.substitution:
        attack_function = cifra.attack.substitution.hack_substitution_mp
    elif algorithm == Algorithm.transposition:
        attack_function = cifra.attack.transposition.brute_force_mp
    elif algorithm == Algorithm.vigenere:
        attack_function = cifra.attack.vigenere.brute_force_mp
    return attack_function


def main(args=sys.argv[1:], _database_path=None) -> None:
    arguments: Dict[str, str] = parse_arguments(args)

    # DICTIONARY MANAGEMENT
    if arguments["mode"] == "dictionary":
        if arguments["action"] == "create":
            initial_words_file = arguments.get("initial_words_file", None)
            with Dictionary.open(arguments["dictionary_name"], create=True, _database_path=_database_path) as dictionary:
                if initial_words_file is not None:
                    dictionary.populate(initial_words_file)
        elif arguments["action"] == "delete":
            Dictionary.remove_dictionary(arguments["dictionary_name"], _database_path=_database_path)
        elif arguments["action"] == "update":
            with Dictionary.open(arguments["dictionary_name"], create=False,
                                 _database_path=_database_path) as dictionary:
                dictionary.populate(arguments["words_file"])
        elif arguments["action"] == "list":
            dictionaries = Dictionary.get_available_languages(_database_path=_database_path)
            for dictionary in dictionaries:
                print(dictionary)

    # CIPHERING MANAGEMENT
    elif arguments["mode"] == "cipher":
        ciphered_content = _process_file_with_key(arguments["file_to_cipher"],
                                                  Algorithm.from_string(arguments["algorithm"]),
                                                  arguments["key"],
                                                  MessageOperation.from_string(arguments["mode"]),
                                                  arguments["charset"] if "charset" in arguments else None)
        _output_result(ciphered_content, arguments)

    # DECIPHERING MANAGEMENT
    elif arguments["mode"] == "decipher":
        deciphered_content = _process_file_with_key(arguments["file_to_decipher"],
                                                    Algorithm.from_string(arguments["algorithm"]),
                                                    arguments["key"],
                                                    MessageOperation.from_string(arguments["mode"]),
                                                    arguments["charset"] if "charset" in arguments else None)
        _output_result(deciphered_content, arguments)

    # ATTACK MANAGEMENT
    elif arguments["mode"] == "attack":
        recovered_content = _attack_file(arguments["file_to_attack"],
                                         Algorithm.from_string(arguments["algorithm"]),
                                         arguments["charset"] if "charset" in arguments else None,
                                         _database_path=_database_path)
        _output_result(recovered_content, arguments)


if __name__ == '__main__':
    main()
