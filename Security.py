import base64

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random

KEY_LENGTH = 1024
BS = 16 # Block Size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class Security:
    def __init__(self):
        self.private_key = RSA.generate(KEY_LENGTH, Random.new().read)
        self.public_key = self.private_key.publickey()
        self.aes_KEY = '\x07\xf2\xdeq_\xe9S<\n\xd78\xe6\x1a\xad7\xeb\xb7\xfd\xf3_Y\xa3\x0b\n;\x9eP"\xfez\xa2\xa6'

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.aes_KEY, AES.MODE_CBC, iv)

        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = self.private_key.decrypt(enc)
        enc = base64.b64decode(enc)
        iv = enc[:BS]
        cipher = AES.new(self.aes_KEY, AES.MODE_CBC, iv)

        return unpad(cipher.decrypt(enc[BS:]))

    def export_public_key(self):
        return self.public_key.exportKey()

    @staticmethod
    def import_key(keystr):
        return RSA.importKey(keystr)
