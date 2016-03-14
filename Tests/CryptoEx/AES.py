# region ----------   ABOUT   -----------------------------
"""
##################################################################
# Created By:                                                    #
# Date: 16/09/2014                                               #
# Name: AES Encryption & Decryption Script                       #
# Version: 1.0                                                   #
# Windows Tested Versions: Win 7 64-bit                          #
# Python Tested Versions: 2.7 32-bit                             #
# Python Environment  : PyCharm                                  #
# pyCrypto Tested Versions: Python 2.7 32-bit                    #
##################################################################
"""
# endregion

# region ----------   IMPORTS   -----------------------------

from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import sys

# endregion

# region ----------   CONSTANTS   -----------------------------

# Define the block size (as AES is a block cipher encryption algorithm).
# Valid options are:
# 16 - for AES128 bit
# 24 - for AES196 bit
# 32 - for AES256 bit
BLOCK_SIZE = 16

# Your input has to fit into a block of BLOCK_SIZE.
# To make sure the last block to encrypt fits in the block, you may need to pad the input.
# This padding must later be removed after decryption so a standard padding would help.
# The idea is to separate the padding into two concerns: interrupt and then pad
# First you insert an interrupt character and then a padding character
# On decryption, first you remove the padding character until you reach the interrupt character
# and then you remove the interrupt character
INTERRUPT = u'\u0001'
PAD = u'\u0000'


# endregion

# region ----------   FUNCTION   -----------------------------

# Strip your data after decryption (with pad and interrupt_
def StripPadding(data):
    return data.rstrip(PAD).rstrip(INTERRUPT)


''' Or in one line:
StripPadding = lambda data, interrupt, pad: data.rstrip(pad).rstrip(interrupt)
'''


# Decrypt the given encrypted data with the decryption cypher
def DecryptWithAES(decrypt_cipher, encrypted_data):
    decoded_encrypted_data = b64decode(encrypted_data)
    decrypted_data = decrypt_cipher.decrypt(decoded_encrypted_data)
    return StripPadding(decrypted_data)


''' Or in one line:
DecryptWithAES = lambda decrypt_cipher, encrypted_data: StripPadding(decrypt_cipher.decrypt(b64decode(encrypted_data)), INTERRUPT, PAD)
'''


# Pad your data before encryption (with pad and interrupt_
def AddPadding(data):
    new_data = ''.join([data, INTERRUPT])
    new_data_len = len(new_data)
    remaining_len = AES.block_size - new_data_len
    to_pad_len = remaining_len % BLOCK_SIZE
    pad_string = PAD * to_pad_len
    return ''.join([new_data, pad_string])


''' Or in one line:
AddPadding = lambda data, interrupt, pad, block_size: ''.join([''.join([data, interrupt]), (pad * ((block_size - (len(''.join([data, interrupt])))) % block_size))])
'''


# Encrypt the given data with the encryption cypher
def EncryptWithAES(encrypt_cipher, plaintext_data):
    plaintext_padded = AddPadding(plaintext_data)
    encrypted = encrypt_cipher.encrypt(plaintext_padded)
    return b64encode(encrypted)


''' Or in one line:
EncryptWithAES = lambda encrypt_cipher, plaintext_data: b64encode(encrypt_cipher.encrypt(AddPadding(plaintext_data, INTERRUPT, PAD, BLOCK_SIZE)))
'''


# endregion

# region ----------   CLASSES   -----------------------------

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


# endregion

# region ----------   MAIN   -----------------------------

def encryptAES(secretKEY, data_to_encrypt):
    try:
        # region ----------   CODE   -----------------------------

        # Let's create our encryption & decryption cipher objects
        # MODE - optional
        # IV - optional
        encryption_cypher = AES.new(secretKEY)

        # We are now ready to encrypt and decrypt our data
        encrypted_data = EncryptWithAES(encryption_cypher, data_to_encrypt)
        return encrypted_data
        # endregion

    # Catch any general exception
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return None


def decryptAES(secretKEY, encrypted_data):
    try:
        # region ----------   CODE   -----------------------------

        # Let's create our encryption & decryption cipher objects
        # MODE - optional
        # IV - optional
        decryption_cypher = AES.new(secretKEY)

        #  And let's decrypt our data
        decrypted_data = DecryptWithAES(decryption_cypher, encrypted_data)
        return decrypted_data
        # endregion

    # Catch any general exception
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return None

        # endregion
