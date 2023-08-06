#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Christophe Gauge"
__email__ = "chris@videre.us"
__version__ = "1.0.2"

'''
Encrypt and decrypt data using RSA certificates
https://github.com/Christophe-Gauge/rsa-crypto

Uses pycryptodome, based on examples available at:
https://pycryptodome.readthedocs.io/en/latest/src/examples.html#generate-public-key-and-private-key

'''


# I M P O R T S ###############################################################

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import getpass
import argparse
import os
import sys
import signal
import base64
import traceback
# import shutil
if (sys.version_info > (3, 0)):
    import configparser as ConfigParser
else:
    import ConfigParser


# G L O B A L S ###############################################################

# file_path = os.path.dirname(__file__)
script_directory = os.path.dirname(os.path.abspath(__file__))
home_directory = os.path.expanduser('~/')
current_directory = os.getcwd()
search_paths = [current_directory, home_directory, script_directory]

encrypted_file_extension = '.enc'
encoded_key_extension = '.bin'
key_extension = '.pem'
key_default_prefix = 'rsa'
public_key_suffix = '_public'
private_key_suffix = '_private'
encoded_key_suffix = '_key'
encoded_key_filename = key_default_prefix + encoded_key_suffix + encoded_key_extension
private_key_filename = key_default_prefix + private_key_suffix + key_extension
public_key_filename = key_default_prefix + public_key_suffix + key_extension
config_file_name = '.' + key_default_prefix + '_values.conf'
private_key_environment_variable = key_default_prefix + private_key_suffix
public_key_environment_variable = key_default_prefix + public_key_suffix
private_key_file = os.path.expanduser(os.path.join('~/', private_key_filename))
public_key_file = os.path.expanduser(os.path.join('~/', public_key_filename))
encoded_key_file = os.path.expanduser(os.path.join('~/', encoded_key_filename))

ini_search_paths = [os.path.join(s, config_file_name) for s in search_paths]

# key_strength = 2048
key_strength = 4096


# F U N C T I O N S ###########################################################


def handler_stop_signals(signum, frame):
    """Handles the SIGTERM signal to stop script cleanly."""
    print("Received %s signal, exiting." % signum)
    sys.exit(0)


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)


def searchFile(filename):
    """Look for a file following the search path."""
    for path in search_paths:
        filePath = os.path.join(path, filename)
        if os.path.isfile(filePath):
            print(f'Using key: {filePath}')
            return filePath
    # print('NOT Found')
    return None


def get_value_config(option, section='DEFAULT', config_path='', is_required=True):
    """Get a value from the config file."""
    config = ConfigParser.ConfigParser()
    print(f'get section: {section} option:{option}')

    used = config.read(ini_search_paths)
    if not used:
        print('No configuration files found: searched for %s' % (ini_search_paths))
        sys.exit(1)
    try:
        value = config.get(section, option)
    except Exception as e:
        print('Bad or missing entry in %s file: %s' % (', '.join(used), e))
        if is_required:
            sys.exit(1)
        else:
            return None
    print('Reading from %s' % (used)[0])
    return value


def set_value_config(option, value, section='DEFAULT', config_path=''):
    """Set a value in a config file."""
    print(f'set section: {section} option:{option}')

    config = ConfigParser.ConfigParser()
    used = config.read(ini_search_paths)
    if not used:
        print('No configuration files found: searched for %s' % (ini_search_paths))
        config_file = os.path.expanduser(os.path.join('~/', config_file_name))
        used = [config_file]
        try:
            dirname = os.path.dirname(config_file)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            config = ConfigParser.RawConfigParser()
            config.read(config_file)

        except Exception as e:
            print('Error: %s' % e)
            print(traceback.format_exc())

    if section != '' and not config.has_section(section):
        # config.remove_section(args.section)
        config.add_section(section)

    config.set(section, option, value.decode("utf-8"))
    # config.write(sys.stdout)

    try:
        with open(used[0], 'w+') as configfile:
            config.write(configfile)
        os.chmod(used[0], 0o644)
        print('Updated %s' % used[0])
        return True

    except Exception as e:
        print('Error: %s' % e)
        print(traceback.format_exc())
        return False


def open_encrypted_key():
    """Open the encrypted key file."""
    global encoded_key_filename
    myFile = searchFile(encoded_key_filename)
    if not myFile:
        print(f'No key found {encoded_key_filename}')
        sys.exit(1)

    print(f'Opening encrypted key {myFile}')
    secret_code = getpass.getpass("Enter key password: ")
    if secret_code == '':
        print("Password cannot be empty")
        sys.exit(1)

    try:
        encoded_key = open(myFile, "rb").read()
        key = RSA.import_key(encoded_key, passphrase=secret_code)
        secret_code = None
        return key

    except ValueError as e:
        print("Failed to decrypt private key")
        # print('ValueError: %s' % e)
        sys.exit(1)
    except Exception as e:
        print('Error: %s' % e)
        sys.exit(1)


def encrypt_value(args):
    """Encrypt a option/value pair in a section of a configuration file."""
    global public_key_filename
    myFile = searchFile(public_key_filename)
    myEnv = os.getenv(public_key_environment_variable, None)
    if myEnv:
        public_key = RSA.import_key(myEnv)
        print(f'Using Environment Variable {public_key_environment_variable}')
    else:
        if myFile:
            public_key = RSA.import_key(open(myFile).read())
        else:
            public_key = open_encrypted_key().publickey()
    if hasattr(args, 'value') and args.value is not None:
        myValue = args.value
    else:
        myValue = getpass.getpass("Enter value: ")
    if myValue == '':
        print("Value cannot be empty")
        return False
    if hasattr(args, 'section'):
        mySection = args.section
    else:
        mySection = ''
    # print(mySection, myValue)
    try:
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_data = cipher_rsa.encrypt((myValue).encode("utf-8"))
        set_value_config(args.option, base64.urlsafe_b64encode(enc_data), section=mySection)
        return True
    except ValueError as e:
        print('Error: %s' % e)
        return False
    except Exception as e:
        print('Error: %s' % e)
        return False


def decrypt_value(args, is_required=True):
    """Decrypt a value for a given option in a section of a configuration file."""
    global private_key_filename
    myFile = searchFile(private_key_filename)

    myEnv = os.getenv(private_key_environment_variable, None)
    if myEnv:
        private_key = RSA.import_key(myEnv)
        print(f'Using Environment Variable {private_key_environment_variable}')
    else:
        if myFile:
            private_key = RSA.import_key(open(myFile).read())
        else:
            private_key = open_encrypted_key()
    if hasattr(args, 'section'):
        if args.section == '':
            mySection = 'DEFAULT'
        else:
            mySection = args.section
    else:
            mySection = 'DEFAULT'
    enc_data = get_value_config(args.option, mySection, is_required=is_required)

    try:
        cipher_rsa = PKCS1_OAEP.new(private_key)
        dec_data = cipher_rsa.decrypt(base64.urlsafe_b64decode(enc_data))
        # print(mySection, args.option, dec_data.decode("utf-8"))
        return dec_data.decode("utf-8")
    except ValueError as e:
        print("Failed to decrypt entry, wrong key file used?")
        sys.exit(1)
    except Exception as e:
        print('Error: %s' % e)
        sys.exit(1)


def encrypt_file(args):
    """Encrypt a file."""
    global public_key_filename

    file_name = os.path.realpath(args.file)
    if os.path.isdir(file_name):
        print("Directory exists, zipping")
        shutil.make_archive(file_name, 'zip', file_name)
        file_name = file_name + '.zip'
    else:
        file_name = args.file

    if not os.path.isfile(file_name):
        print("File does not exist")
        sys.exit(1)
    encrypted_file_name = os.path.realpath(file_name) + encrypted_file_extension

    myEnv = os.getenv(public_key_environment_variable, None)
    if myEnv:
        public_key = RSA.import_key(myEnv)
        print(f'Using Environment Variable {public_key_environment_variable}')
    else:
        myFile = searchFile(public_key_filename)
        if myFile:
            public_key = RSA.import_key(open(myFile).read())
        else:
            public_key = open_encrypted_key().publickey()

    try:
        with open(file_name, mode='rb') as file:
            fileContent = file.read()

        with open(encrypted_file_name, "wb") as file_out:
            session_key = get_random_bytes(16)

            # Encrypt the session key with the public RSA key
            cipher_rsa = PKCS1_OAEP.new(public_key)
            enc_session_key = cipher_rsa.encrypt(session_key)

            # Encrypt the data with the AES session key
            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(fileContent)
            [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
        return encrypted_file_name
    except Exception as e:
        print('Error: %s' % e)
        sys.exit(1)


def decrypt_file(args):
    """Decrypt an encrypted file."""
    global private_key_filename
    if not os.path.isfile(args.file):
        print("File does not exist")
        sys.exit(1)
    decrypted_file_name = '.'.join(os.path.realpath(args.file).split(".")[:-1])

    myEnv = os.getenv(private_key_environment_variable, None)
    if myEnv:
        private_key = RSA.import_key(myEnv)
        print(f'Using Environment Variable {private_key_environment_variable}')
    else:
        myFile = searchFile(private_key_filename)
        if myFile:
            private_key = RSA.import_key(open(myFile).read())
        else:
            private_key = open_encrypted_key()

    try:
        with open(args.file, "rb") as file_in:

            enc_session_key, nonce, tag, ciphertext = [file_in.read(x)
                                                       for x in (private_key.size_in_bytes(),
                                                                 16, 16, -1)]

            # Decrypt the session key with the private RSA key
            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)

            # Decrypt the data with the AES session key
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            # print(data.decode("utf-8"))

        with open(decrypted_file_name, mode='wb') as file:
            fileContent = file.write(data)
        return decrypted_file_name
    except ValueError as e:
        print("Failed to decrypt file")
        # print('ValueError: %s' % e)
        sys.exit(1)
    except Exception as e:
        print('Error: %s' % e)
        sys.exit(1)

    # if os.path.splitext(decrypted_file_name)[1] == '.zip':
    #     shutil.unpack_archive(decrypted_file_name, os.path.splitext(decrypted_file_name)[0], 'zip')


def extract_keys(args):
    """Save private and public keys to file."""
    global public_key_file
    global private_key_file
    key = open_encrypted_key()

    if os.path.isfile(private_key_file):
        os.remove(private_key_file)
    if os.path.isfile(public_key_file):
        os.remove(public_key_file)

    with open(private_key_file, "wb") as file_out:
        file_out.write(key.export_key())

    with open(public_key_file, "wb") as file_out:
        file_out.write(key.publickey().export_key())

    os.chmod(private_key_file, 0o400)
    print(f'Created private key file {private_key_file} (File can decrypt data and is not password-protected, keep it safe!)')
    print(f'Created public key file {public_key_file} (distribute this one to anyone who needs to encrypt data, it cannot be used for decryption!)')


def create_keys(args):
    """Generate a new Key and save file."""
    global encoded_key_file
    if os.path.isfile(encoded_key_file):
        print(f"File {encoded_key_file} already exists, aborting.")
        sys.exit(1)
    secret_code = getpass.getpass("Enter key password: ")
    if secret_code == '':
        print("Password cannot be empty")
        sys.exit(1)
    secret_code2 = getpass.getpass("Re-enter key password: ")
    if secret_code != secret_code2:
        print("Passwords are not the same, please try again.")
        sys.exit(1)
    print("Creating key...")

    key = RSA.generate(key_strength)
    # private_key = key.export_key()
    # with open(private_key_filename, "wb") as file_out:
    #     file_out.write(private_key)
    #
    # public_key = key.publickey().export_key()
    # with open(public_key_filename, "wb") as file_out:
    #     file_out.write(public_key)

    encrypted_key = key.export_key(passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC")
    # print(encrypted_key)
    secret_code = None
    secret_code2 = None

    with open(encoded_key_file, "wb") as file_out:
        file_out.write(encrypted_key)

    os.chmod(encoded_key_file, 0o400)
    # os.chmod(private_key_filename, 0o400)
    print(f'Created password-protected private/public keys file {encoded_key_file}')
    print('Use the "extract" keyword to create public and private key files.')


def delete_key(args):
    """Delete the private key."""
    global private_key_filename
    myFile = searchFile(private_key_filename)
    if myFile:
        if os.path.isfile(myFile):
            os.remove(myFile)
            print('Private key deleted:', myFile)


def main():
    """Main function."""
    global private_key
    global public_key

    p = argparse.ArgumentParser()
    subparser = p.add_subparsers(title="commands",
                                 metavar='')

    get_apps_p = subparser.add_parser('encrypt',
                                      description='Encrypt a file',
                                      help='Encrypt a file using an RSA certificate')
    get_apps_p.set_defaults(func=encrypt_file)
    get_apps_p.add_argument('-f', '--file', action='store',
                            required=True, help='The name of the file to encrypt')
    get_apps_p.add_argument('-k', '--key', action='store',
                            required=False,
                            help='The encryption/decryption key file to use')

    get_apps_p = subparser.add_parser('decrypt',
                                      description='Decrypt a file',
                                      help='Decrypt a file using an RSA certificate')
    get_apps_p.set_defaults(func=decrypt_file)
    get_apps_p.add_argument('-f', '--file', action='store',
                            required=True, help='The name of the file to decrypt')
    get_apps_p.add_argument('-k', '--key', action='store',
                            required=False,
                            help='The encryption/decryption key file to use')

    get_apps_p = subparser.add_parser('extract',
                                      description='Extract public and private keys from encrypted RSA key',
                                      help='Extract public and private keys')
    get_apps_p.set_defaults(func=extract_keys)
    get_apps_p.add_argument('-k', '--key', action='store',
                            required=False,
                            help='The encryption/decryption key file to use')

    get_apps_p = subparser.add_parser('create',
                                      description='Create new public, private and encrypted key trio',
                                      help='Create new keys')
    get_apps_p.set_defaults(func=create_keys)
    get_apps_p.add_argument('-k', '--key', action='store',
                            required=False,
                            help='The encryption/decryption key file to use')

    get_apps_p = subparser.add_parser('set',
                                      description='Encrypt a value',
                                      help='Encrypt a value in a configuration file using an RSA certificate')
    get_apps_p.set_defaults(func=encrypt_value)
    get_apps_p.add_argument('-v', '--value', action='store',
                            required=False, help='The value to encrypt')
    get_apps_p.add_argument('-s', '--section', action='store',
                            default='', required=False,
                            help='The Section where the option is located.')
    get_apps_p.add_argument('-o', '--option', action='store',
                            default='', required=True,
                            help='The option name.')
    get_apps_p.add_argument('-k', '--key', action='store',
                            required=False,
                            help='The encryption/decryption key file to use')

    get_apps_p = subparser.add_parser('get',
                                      description='Decrypt a value',
                                      help='Decrypt a value in a configuration file using an RSA certificate')
    get_apps_p.set_defaults(func=decrypt_value)
    get_apps_p.add_argument('-o', '--option', action='store',
                            required=True,
                            help='The option name.')
    get_apps_p.add_argument('-s', '--section', action='store',
                            default='', required=False,
                            help='The Section where the option is located.')
    get_apps_p.add_argument('-k', '--key', action='store',
                            required=False,
                            help='The encryption/decryption key file to use')

    get_apps_p = subparser.add_parser('clear',
                                      description='Delete the unencrypted private key',
                                      help='Delete the unencrypted private key')
    get_apps_p.set_defaults(func=delete_key)
    get_apps_p.add_argument('-k', '--key', action='store',
                            required=False,
                            help='The encryption/decryption key file to use')

    args = p.parse_args()
    try:
        if args.key:
            # print('Looking for key:', args.key)
            global public_key_filename
            global private_key_filename
            global encoded_key_filename
            global public_key_file
            global private_key_file
            global encoded_key_file
            global private_key_environment_variable
            global public_key_environment_variable
            public_key_filename = args.key + public_key_suffix + key_extension
            private_key_filename = args.key + private_key_suffix + key_extension
            encoded_key_filename = args.key + encoded_key_suffix + encoded_key_extension
            private_key_file = os.path.expanduser(os.path.join('~/', private_key_filename))
            public_key_file = os.path.expanduser(os.path.join('~/', public_key_filename))
            encoded_key_file = os.path.expanduser(os.path.join('~/', encoded_key_filename))
            private_key_environment_variable =  args.key + '_private'
            public_key_environment_variable =  args.key + '_public'
    except AttributeError as e:
        print("Invalid parameters, use -h for help.")
        sys.exit(1)
    except Exception as e:
        print('Error: %s' % e)
        sys.exit(1)

    if len(vars(args)) > 0:
        sys.exit(args.func(args))
    else:
        print('No arguments passed, use the "-h" argument for usage help')
        sys.exit(0)

###############################################################################


if __name__ == "__main__":
    main()

# E N D   O F   F I L E #######################################################
