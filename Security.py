import os
import base64

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA

KEY_LENGTH = 1024  # RSA private key length
BS = 16  # AES block size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)  # AES Padding
unpad = lambda s: s[:-ord(s[len(s) - 1:])]  # AES unpadding


class Security:
    def __init__(self):
        self.server_public_key = None  # Server public key

        self.aes_key = os.urandom(BS)  # Randoms string in 16 bytes
        self.iv = Random.new().read(AES.block_size)  # IV is a data block to be transmitted to the receiver (16 bytes)
        self.mode = AES.MODE_CFB  # AES FeedBack mode
        self.cipher = AES.new(self.aes_key, self.mode, self.iv)  # Creates a new AES cipher

    def encrypt(self, raw):
        """
        Encrypes the data by AES cipher
        :param raw: data (string)
        :return: encrypted data (string)
        """
        raw = pad(raw)  # Padding the data
        aes_encryption = base64.b64encode(self.iv + self.cipher.encrypt(raw))  # Encoding the encrypted data
        return aes_encryption

    def decrypt(self, raw):
        """
        Decrypes the data
        :param raw: data
        :return: decrypted data (string)
        """
        enc = base64.b64decode(raw)  # Decoding the AES key
        return unpad(self.cipher.decrypt(enc[16:]))  # decrypting and unpadding the data from 16 bytes (iv is 16 bytes)

    @staticmethod
    def import_key(keystr):
        """
        Makes a string key to an object key
        :param keystr: key (string)
        :return: key (object)
        """
        return RSA.importKey(keystr)

