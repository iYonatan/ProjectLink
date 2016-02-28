import os
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA

KEY_LENGTH = 1024
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class Security:
    def __init__(self):
        self.private_key = RSA.generate(KEY_LENGTH, Random.new().read)
        self.public_key = self.private_key.publickey()

        self.server_public_key = None

        self.aes_key = os.urandom(BS)
        self.iv = Random.new().read(AES.block_size)
        self.mode = AES.MODE_CFB
        self.cipher = AES.new(self.aes_key, self.mode, self.iv)

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.aes_key, self.mode, iv)
        aes_encryption = base64.b64encode(iv + cipher.encrypt(raw))
        return self.server_public_key.encrypt(aes_encryption, 32)

    def decrypt(self, raw):
        raw = self.private_key.decrypt(raw)
        enc = base64.b64decode(raw)
        iv = enc[:16]
        cipher = AES.new(self.aes_key, self.mode, iv)
        return unpad(cipher.decrypt(enc[16:]))

    def export_public_key(self):
        return self.public_key.exportKey()

    @staticmethod
    def import_key(keystr):
        return RSA.importKey(keystr)
