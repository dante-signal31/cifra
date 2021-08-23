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

import argparse
import os
import sys
import tempfile
from typing import List, Dict

import cifra.cipher.common
from cifra.attack.dictionaries import Dictionary

if os.getenv("CIFRA_DEBUG", 0) == "1":
    # TODO: Check Travis CI sets it corresponding CIFRA_DEBUG env var to 1.
    DICTIONARY_FOLDER = tempfile.mkdtemp()
else:
    DICTIONARY_FOLDER = "~/.cifra/"

CIPHERING_ALGORITHMS = ["caesar", "substitution", "transposition", "affine",
                        "vigenere"]

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
    dictionary_create_parser = dictionary_actions_subparser.add_parser(name="create")
    dictionary_create_parser.add_argument("dictionary_name",
                                          type=str,
                                          help="Name for the dictionary to create.",
                                          metavar="NEW_DICTIONARY_NAME")
    dictionary_create_parser.add_argument("-i", "--initial_words_file",
                                          type=_check_is_file,
                                          help="Optionally you can load in the dictionary words located in a file",
                                          metavar="PATH_TO FILE_WITH_WORDS")
    #   DICTIONARY REMOVAL.
    dictionary_delete_parser = dictionary_actions_subparser.add_parser(name="delete")
    dictionary_delete_parser.add_argument("dictionary_name",
                                          type=str,
                                          help="Name for the dictionary to delete.",
                                          metavar="DICTIONARY_NAME_TO_DELETE")
    #   DICTIONARY UPDATING.
    dictionary_update_parser = dictionary_actions_subparser.add_parser(name="update")
    dictionary_update_parser.add_argument("dictionary_name",
                                          type=str,
                                          help="Name for the dictionary to update with additional words.",
                                          metavar="DICTIONARY_NAME_TO_UPDATE")
    dictionary_update_parser.add_argument("words_file",
                                          type=_check_is_file,
                                          help="Pathname to a file with words to add to dictionary",
                                          metavar="PATH_TO FILE_WITH_WORDS")
    #   DICTIONARY LISTING.
    _ = dictionary_actions_subparser.add_parser(name="list")
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
                               help="Path to output file to place ciphered text. If not used "
                                    "ciphered text will be dumped to console.",
                               metavar="OUTPUT_CIPHERED_FILE")
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
                                 help="Path to output file to place deciphered text. If not used "
                                      "deciphered text will be dumped to console.",
                                 metavar="OUTPUT_DECIPHERED_FILE")
    # ATTACK MANAGEMENT
    attack_parser = cifra_subparsers.add_parser(name="attack",
                                                help="Attack a ciphered text to get its key.")
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
                               help="Path to output file to place deciphered text. If not used "
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


def main(args: List[str] = sys.argv[1:]) -> None:
    arguments: Dict[str, str] = parse_arguments(args)
    if arguments["mode"] == "dictionary":
        if arguments["action"] == "create":
            initial_words_file = arguments.get("initial_words_file", None)
            with Dictionary.open(arguments["dictionary_name"], create=True, _database_path=DICTIONARY_FOLDER) as dictionary:
                if initial_words_file is not None:
                    dictionary.populate(initial_words_file)
        if arguments["action"] == "delete":
            Dictionary.remove_dictionary(arguments["dictionary_name"], _database_path=DICTIONARY_FOLDER)
        if arguments["action"] == "update":
            with Dictionary.open(arguments["dictionary_name"], create=False, _database_path=DICTIONARY_FOLDER) as dictionary:
                dictionary.populate(arguments["words_file"])




if __name__ == '__main__':
    main(sys.argv[1:])
