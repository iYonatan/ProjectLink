import socket
import random
import math


class diffy_hallen(socket.socket):
    def __init__(self, y, location):

        super(diffy_hallen, self).__init__()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_RAW)
        self.location = location
        self.g = 2065559669 ** 2
        self.y = y
        self.n = self.generate_n()  # the mod number
        # self.other_send=other_send
        self.limit = 10000
        self.key = None

    def generate_n(self):
        if self.location == "server":
            count = 10000

            while True:
                isprime = True

                for x in range(2, int(math.sqrt(count) + 7)):
                    if count % x == 0:
                        isprime = False
                        break

                if isprime and count > self.limit:
                    return count
                    break

                count += 1
                # else:
                #   self.n = ask_n(str(self.limit))

    def generate_y(self):
        n = self.n - 1
        y = random.randrange(0, n)
        self.y = y

    def is_prime(self, n):
        if n == 2 or n == 3: return True
        if n < 2 or n % 2 == 0: return False
        if n < 9: return True
        if n % 3 == 0: return False
        r = int(n ** 0.5)
        f = 5
        while f <= r:
            # print '\t',f
            if n % f == 0: return False
            if n % (f + 2) == 0: return False
            f += 6
        return True


diff = diffy_hallen(0, "server")