import base64

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class Security:
    def __init__(self, public_key):
        self.public_key = Security.import_key(public_key)
        self.aes_KEY = '\x07\xf2\xdeq_\xe9S<\n\xd78\xe6\x1a\xad7\xeb\xb7\xfd\xf3_Y\xa3\x0b\n;\x9eP"\xfez\xa2\xa6'
        self.aes_in_pbk = self.public_key.encrypt(self.encrypt(self.aes_KEY), 32)

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.aes_KEY, AES.MODE_CBC, iv)

        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.aes_KEY, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))

    @staticmethod
    def import_key(key_str):
        return RSA.importKey(key_str)
