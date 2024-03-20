from logging import info
from os import environ
from random import Random

from parcs.server import Runner, serve


class PollardRunner(Runner):
    def run(self):
        random = Random(int(environ["seed"]))
        number = int(environ["number"])
        worker_count = int(environ["worker_count"])

        info(f"Factoring {number} on {worker_count} workers")

        tasks = []

        for _ in range(worker_count):
            task = self.engine.run("kharacternyk/pollard")
            seed = random.randint(0, 2048)
            task.send_all(number, seed)
            tasks.append(task)

            info(f"Spawned a worker with seed {seed}")

        results = [task.recv() for task in tasks]

        for task in tasks:
            task.shutdown()

        info(f"Results: {results}")


serve(PollardRunner())
