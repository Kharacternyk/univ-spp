from logging import info
from os import environ
from random import Random
from select import select

from parcs.network import recv
from parcs.server import Runner, serve


class PollardRunner(Runner):
    def run(self):
        random = Random(int(environ["seed"]))
        number = int(environ["number"])
        worker_count = int(environ["worker_count"])

        info(f"Searching for a prime factor of {number} on {worker_count} workers")

        tasks = []

        for _ in range(worker_count):
            task = self.engine.run("kharacternyk/pollard")
            initial_x = random.randint(0, number - 1)
            task.send_all(number, initial_x)
            tasks.append(task)

            info(f"Spawned a worker with initial x = {initial_x}")

        (socket, *_), *_ = select([task.client for task in tasks], [], [])

        info(f"Factor: {recv(socket)}")

        for task in tasks:
            task.shutdown()


serve(PollardRunner())
