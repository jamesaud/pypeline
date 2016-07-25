import concurrent.futures


class Parallel:

    def __init__(self):
        self.future_to_add = []
        self.executor = concurrent.futures.ThreadPoolExecutor()

    def add(self, function, *args, **kwargs):
        self.future_to_add.append(self.executor.submit(function, *args, *kwargs))

    def run(self):
        for future in concurrent.futures.as_completed(self.future_to_add):
            if future.exception() is not None:
                raise future.exception()