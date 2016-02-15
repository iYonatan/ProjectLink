from Crypto.PublicKey import RSA
from Crypto import Random

KEY_LENGTH = 1024


class Security:
    def __init__(self):
        self.private_key = RSA.generate(KEY_LENGTH, Random.new().read)
        self.public_key = self.private_key.publickey()

    def encrypt(self, data):
        return self.public_key.encrypt(data, 32)

    def decrypt(self):
        pass

    def export_public_key(self):
        return self.public_key.exportKey()

    @staticmethod
    def import_key(keystr):
        return RSA.importKey(keystr)


# sec = Security()
# print type(sec.public_key) # instance
# ek = sec.export_public_key()
# print type(ek) # str
# iek = Security.import_key(ek)
# print type(iek) # instance
# print sec.export_key()
