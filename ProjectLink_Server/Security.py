import cPickle
from Crypto.PublicKey import RSA
from Crypto import Random

KEY_LENGTH = 1024


class Security:
    def __init__(self):
        self.private_key = RSA.generate(KEY_LENGTH, Random.new().read)
        self.public_key = self.private_key.publickey()

    def encrypt(self, raw):
        pass

    def decrypt(self, raw):
        return self.private_key.decrypt(cPickle.loads(raw))

    def export_public_key(self):
        return self.public_key.exportKey()

    @staticmethod
    def import_key(keystr):
        return RSA.importKey(keystr)

