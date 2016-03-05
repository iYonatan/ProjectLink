# region ----------   ABOUT   -----------------------------
"""
##################################################################
# Created By: Michael Chernovilski                               #
# Date: 23/09/2014                                               #
# Name: Encryption & Decryption Script                           #
# Version: 1.0                                                   #
# Windows Tested Versions: Win 7 64-bit                          #
# Python Tested Versions: 2.7 32-bit                             #
# Python Environment  : PyCharm                                  #
# pyCrypto Tested Versions: Python 2.7 32-bit                    #
##################################################################
"""
# endregion

# region--------------------------------------------IMPORTS-----------------------------------------
import pickle
from base64 import b64decode
from Crypto import Random
from Crypto.PublicKey import RSA

# endregion

# region-------------------------------------------CONSTANTS----------------------------------------
KEY_LENGTH = 1024


# endregion

class Security:
    private_key = None

    # ----------------------------------------------------------
    def __init__(self):
        self.private_key = RSA.generate(KEY_LENGTH, Random.new().read)

    # region-----------------FUNCTIONS--------------------------
    # ----------------------------------------------------------
    def encrypt(self, data, public_key):
        pack_data = self.pack(data)

        if not public_key:
            public_key = self.private_key.publickey()

        return public_key.encrypt(pack_data, 32)[0]

    # ----------------------------------------------------------
    def decode(self, data, private_key):
        if not private_key:
            private_key = self.private_key

        decrypt_data = private_key.decrypt(data)

        return self.unpack(decrypt_data)

    # ----------------------------------------------------------
    def unpack(self, data):
        return pickle.loads(b64decode(data))

    # ----------------------------------------------------------
    def pack(self, data):
        return b64decode(pickle.dumps(data))

    # -----------------------------------------------------------------------------------------------
    #  Key Exchange
    #
    # Description: 
    # -----------------------------------------------------------------------------------------------
    def key_exchange(self, client_sock):
        print 'key_exchange'
        # endregion
