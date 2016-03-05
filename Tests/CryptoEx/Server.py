import socket
import time

from MyCrypto import *

# region ----------   C O N S T A N T S  ------------------------------------------------------------------
PORT = 6070
LEN_UNIT_BUF = 2048  # Min len of buffer for receive from server socket
MAX_ENCRYPTED_MSG_SIZE = 128
MAX_SOURCE_MSG_SIZE = 128
END_LINE = "\r\n"  # End of line


# endregion

# ==========================================================================================================
class Server(object):
    def __init__(self):

        self.socket = socket.socket()
        self.client_keys = {}
        self.crypto = Crypto()

    # ======================================================================================================
    def start(self):
        self.socket.bind(("0.0.0.0", PORT))
        self.socket.listen(1)
        self._run()

    # ======================================================================================================
    def _run(self):
        print "running"
        client_socket, client_address = self.socket.accept()
        self.key_exchange(client_socket)

    # ======================================================================================================
    def key_exchange(self, client_socket):
        if self.crypto.private_key.can_encrypt():
            # --------------------  1 ------------------------------------------------------------------------
            # ------------  Send  server publicKey
            client_socket.send(pickle.dumps(self.crypto.private_key.publickey()) + END_LINE)
            time.sleep(0.5)
            # -----------  send  Base64 Hash of self.crypto.private_key.publickey()
            client_socket.send(
                b64encode(SHA256.new(pickle.dumps(self.crypto.private_key.publickey())).hexdigest()) + END_LINE)
            time.sleep(0.5)

            # --------------------  2 ------------------------------------------------------------------------
            # --------------  Wait client private key  --------------------------------------------------------
            # get Pickled private  key
            pickled_client_private_key = client_socket.recv(LEN_UNIT_BUF).split(END_LINE)[0]
            client_private_key = pickle.loads(pickled_client_private_key)

            # --------------  Wait client hash private key  ---------------------------------------------------------------------------
            # Hashing original  client private key
            calculated_hash_client_pickled_private_key = SHA256.new(pickle.dumps(client_private_key)).hexdigest()
            declared_hash_client_pickled_private_key = b64decode(client_socket.recv(LEN_UNIT_BUF).split(END_LINE)[0])
            if calculated_hash_client_pickled_private_key != declared_hash_client_pickled_private_key:
                print "Error : hash and original"
                return

            client_private_key = RSA.importKey(client_private_key)

            ''' Due to a bug in pyCrypto, it is not possible to decrypt RSA messages that are longer than 128 byte.
                        To overcome this problem, the following code receives  the encrypted data in chunks of 128 byte.
                        We need to think how to tell the students about this behavior (another help message?)
                        And maybe we should implemented this approach in level 3 as well...
             '''

            # --------------------  3 ------------------------------------------------------------------------
            #  -------------- Receive from client in parts message
            #  -------------- encrypted by server public key info containing symmetric key and hash symmetric key encrypted by client public key
            pickled_client_key = ''
            pickled_encrypted_client_key = ''
            #   Recieve from client number of encrypted message parts
            msg_parts = client_socket.recv(LEN_UNIT_BUF).split(END_LINE)[0]
            for i in xrange(int(msg_parts)):
                # Wait from client current part of encrypt client_key
                part_pickled_encrypted_client_key = client_socket.recv(LEN_UNIT_BUF).split(END_LINE)[0]
                pickled_encrypted_client_key += part_pickled_encrypted_client_key
                # Decryption current part of encrypt client_key
                part_encrypt_client_key = pickle.loads(part_pickled_encrypted_client_key)
                part_pickled_client_key = self.crypto.private_key.decrypt(part_encrypt_client_key)
                pickled_client_key += part_pickled_client_key
            items = pickled_client_key.split('#')
            client_sym_key_original = b64decode(items[0])
            print 'Client Sym Key Original :     ' + client_sym_key_original
            # --------   Extract Client Hash Sym Key
            client_encrypted_hash_sym_key = b64decode(items[1])
            client_encrypted_hash_sym_key = pickle.loads(client_encrypted_hash_sym_key)

            splitted_client_encrypted_hash_sym_key = [client_encrypted_hash_sym_key[i:i + MAX_ENCRYPTED_MSG_SIZE] for i
                                                      in xrange(0, len(client_encrypted_hash_sym_key),
                                                                MAX_ENCRYPTED_MSG_SIZE)]
            msg_parts = len(splitted_client_encrypted_hash_sym_key)
            client_hash_sym_key = ''
            for i in xrange(int(msg_parts)):
                # Decryption current part of encrypt client_key
                part_client_encrypted_hash_sym_key = client_private_key.decrypt(
                    splitted_client_encrypted_hash_sym_key[i])
                client_hash_sym_key += part_client_encrypted_hash_sym_key
            print 'Client Hash Sym Key  :     ' + client_hash_sym_key
            calculated_client_sym_key_original = SHA256.new(client_sym_key_original).hexdigest()
            if calculated_client_sym_key_original != client_hash_sym_key:
                print "Error : hash and original"
                return

                # ==========================================================================================================


def main():
    server = Server()
    server.start()


if __name__ == "__main__":
    main()
