"""
Tests for some launcher commands.
"""
import pytest
import os.path
import tempfile
from test_common.fs.temp import temp_dir
import cifra.cifra_launcher as cifra_launcher
import cifra.cipher.substitution as substitution
from cifra.tests.test_dictionaries import loaded_dictionaries, LoadedDictionaries
from cifra.tests.test_caesar import ORIGINAL_MESSAGE as caesar_ORIGINAL_MESSAGE
from cifra.tests.test_caesar import CIPHERED_MESSAGE_KEY_13 as caesar_CIPHERED_MESSAGE_KEY_13
from cifra.tests.test_caesar import TEST_KEY as caesar_TEST_KEY
from cifra.tests.test_substitution import ORIGINAL_MESSAGE as substitution_ORIGINAL_MESSAGE
from cifra.tests.test_substitution import CIPHERED_MESSAGE as substitution_CIPHERED_MESSAGE
from cifra.tests.test_substitution import TEST_KEY as substitution_TEST_KEY
from cifra.tests.test_substitution import TEST_CHARSET as substitution_TEST_CHARSET


@pytest.mark.quick_slow
def test_cipher_caesar(temp_dir, loaded_dictionaries: LoadedDictionaries):
    with tempfile.NamedTemporaryFile(mode="w") as message_file:
        message_file.write(caesar_ORIGINAL_MESSAGE)
        message_file.flush()
        output_file_pathname = os.path.join(temp_dir, "ciphered_message.txt")
        provided_args = f"cipher caesar {caesar_TEST_KEY} {message_file.name} --ciphered_file {output_file_pathname}".split()
        cifra_launcher.main(provided_args, loaded_dictionaries.temp_dir)
        with open(output_file_pathname, mode="r") as output_file:
            recovered_content = output_file.read()
            assert caesar_CIPHERED_MESSAGE_KEY_13 == recovered_content


@pytest.mark.quick_slow
def test_decipher_caesar(temp_dir, loaded_dictionaries: LoadedDictionaries):
    with tempfile.NamedTemporaryFile(mode="w") as message_file:
        message_file.write(caesar_CIPHERED_MESSAGE_KEY_13)
        message_file.flush()
        output_file_pathname = os.path.join(temp_dir, "deciphered_message.txt")
        provided_args = f"decipher caesar {caesar_TEST_KEY} {message_file.name} --deciphered_file {output_file_pathname}".split()
        cifra_launcher.main(provided_args, loaded_dictionaries.temp_dir)
        with open(output_file_pathname, mode="r") as output_file:
            recovered_content = output_file.read()
            assert caesar_ORIGINAL_MESSAGE == recovered_content


@pytest.mark.quick_slow
def test_cipher_substitution(temp_dir, loaded_dictionaries: LoadedDictionaries):
    with tempfile.NamedTemporaryFile(mode="w") as message_file:
        message_file.write(substitution_ORIGINAL_MESSAGE)
        message_file.flush()
        output_file_pathname = os.path.join(temp_dir, "ciphered_message.txt")
        provided_args = f"cipher substitution {substitution_TEST_KEY} {message_file.name} --ciphered_file {output_file_pathname} --charset {substitution_TEST_CHARSET}".split()
        cifra_launcher.main(provided_args, loaded_dictionaries.temp_dir)
        with open(output_file_pathname, mode="r") as output_file:
            recovered_content = output_file.read()
            assert substitution_CIPHERED_MESSAGE == recovered_content


@pytest.mark.quick_slow
def test_decipher_substitution(temp_dir, loaded_dictionaries: LoadedDictionaries):
    with tempfile.NamedTemporaryFile(mode="w") as message_file:
        message_file.write(substitution_CIPHERED_MESSAGE)
        message_file.flush()
        output_file_pathname = os.path.join(temp_dir, "deciphered_message.txt")
        provided_args = f"decipher substitution {substitution_TEST_KEY} {message_file.name} --deciphered_file {output_file_pathname} --charset {substitution_TEST_CHARSET}".split()
        cifra_launcher.main(provided_args, loaded_dictionaries.temp_dir)
        with open(output_file_pathname, mode="r") as output_file:
            recovered_content = output_file.read()
            assert substitution_ORIGINAL_MESSAGE == recovered_content


@pytest.mark.quick_slow
def test_attack_caesar(temp_dir, loaded_dictionaries: LoadedDictionaries):
    with tempfile.NamedTemporaryFile(mode="w") as message_file:
        message_file.write(caesar_CIPHERED_MESSAGE_KEY_13)
        message_file.flush()
        output_file_pathname = os.path.join(temp_dir, "recovered_message.txt")
        provided_args = f"attack caesar {message_file.name} --deciphered_file {output_file_pathname}".split()
        cifra_launcher.main(provided_args, loaded_dictionaries.temp_dir)
        with open(output_file_pathname, mode="r") as output_file:
            recovered_content = output_file.read()
            assert caesar_ORIGINAL_MESSAGE == recovered_content


@pytest.mark.quick_slow
def test_attack_substitution(temp_dir, loaded_dictionaries: LoadedDictionaries):
    with tempfile.NamedTemporaryFile(mode="w") as message_file, \
            open(os.path.join(os.getcwd(), "cifra", "tests", "resources/english_book_c1.txt")) as english_book:
        original_message = english_book.read()
        ciphered_text = substitution.cipher(original_message, substitution_TEST_KEY, substitution_TEST_CHARSET)
        message_file.write(ciphered_text)
        message_file.flush()
        output_file_pathname = os.path.join(temp_dir, "recovered_message.txt")
        provided_args = f"attack substitution {message_file.name} --deciphered_file {output_file_pathname} --charset {substitution_TEST_CHARSET}".split()
        cifra_launcher.main(provided_args, loaded_dictionaries.temp_dir)
        with open(output_file_pathname, mode="r") as output_file:
            recovered_content = output_file.read()
            assert original_message == recovered_content

