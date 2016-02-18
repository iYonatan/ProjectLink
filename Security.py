from Crypto.PublicKey import RSA

KEY_LENGTH = 1024


class Security:
    def __init__(self):
        self.public_key = None

    def encrypt(self, raw):
        return self.public_key.encrypt(raw, 32)

    def decrypt(self, raw):
        pass

    def export_public_key(self):
        return self.public_key.exportKey()

    @staticmethod
    def import_key(keystr):
        return RSA.importKey(keystr)
