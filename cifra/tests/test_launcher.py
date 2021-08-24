"""
Tests for some launcher commands.
"""
import pytest
import os.path
import tempfile
from test_common.fs.temp import temp_dir
import cifra.cifra_launcher as cifra_launcher
from cifra.tests.test_dictionaries import loaded_dictionaries, LoadedDictionaries
from cifra.tests.test_caesar import ORIGINAL_MESSAGE, CIPHERED_MESSAGE_KEY_13, \
    TEST_KEY


@pytest.mark.quick_slow
def test_cipher_caesar(temp_dir, loaded_dictionaries: LoadedDictionaries):
    with tempfile.NamedTemporaryFile(mode="w") as message_file:
        message_file.write(ORIGINAL_MESSAGE)
        message_file.flush()
        output_file_pathname = os.path.join(temp_dir, "ciphered_message.txt")
        provided_args = f"cipher caesar {TEST_KEY} {message_file.name} --ciphered_file {output_file_pathname}".split()
        cifra_launcher.main(provided_args, loaded_dictionaries.temp_dir)
        with open(output_file_pathname, mode="r") as output_file:
            recovered_content = output_file.read()
            assert CIPHERED_MESSAGE_KEY_13 == recovered_content


@pytest.mark.quick_slow
def test_decipher_caesar(temp_dir, loaded_dictionaries: LoadedDictionaries):
    with tempfile.NamedTemporaryFile(mode="w") as message_file:
        message_file.write(CIPHERED_MESSAGE_KEY_13)
        message_file.flush()
        output_file_pathname = os.path.join(temp_dir, "deciphered_message.txt")
        provided_args = f"decipher caesar {TEST_KEY} {message_file.name} --deciphered_file {output_file_pathname}".split()
        cifra_launcher.main(provided_args, loaded_dictionaries.temp_dir)
        with open(output_file_pathname, mode="r") as output_file:
            recovered_content = output_file.read()
            assert ORIGINAL_MESSAGE == recovered_content


@pytest.mark.quick_slow
def test_attack_caesar(temp_dir, loaded_dictionaries: LoadedDictionaries):
    with tempfile.NamedTemporaryFile(mode="w") as message_file:
        message_file.write(CIPHERED_MESSAGE_KEY_13)
        output_file_pathname = os.path.join(temp_dir, "recovered_message.txt")
        provided_args = f"attack caesar {message_file.name} --deciphered_file {output_file_pathname}".split()
        cifra_launcher.main(provided_args, loaded_dictionaries.temp_dir)
        with open(output_file_pathname, mode="r") as output_file:
            recovered_content = output_file.read()
            assert ORIGINAL_MESSAGE == recovered_content
