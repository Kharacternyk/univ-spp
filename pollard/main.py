from logging import info
from math import gcd

from parcs.server import Service, serve


class Pollard(Service):
    def run(self):
        number = self.recv()
        seed = self.recv()
        info(f"Factoring {number} with seed {seed}")

        y = x = 2
        divisor = 1
        while divisor == 1:
            x = polynomial(x, number)
            y = polynomial(polynomial(y, number), number)
            divisor = gcd(abs(x - y), number)

        info(f"Found {divisor}")
        self.send(divisor)


def polynomial(x, modulus):
    return (x * x + 1) % modulus


serve(Pollard())
