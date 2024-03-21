from logging import info
from math import gcd

from parcs.server import Service, serve


class Pollard(Service):
    def run(self):
        number = self.recv()
        initial_x = self.recv()
        info(f"Searching for a prime factor of {number} with initial x = {initial_x}")

        y = x = initial_x
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
