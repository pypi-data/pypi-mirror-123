from time import time_ns


class Profiler:
    def __init__(self):
        self.time_start = None
        self.time_stop = None
        self.time_delta = None

    def __enter__(self):
        self.time_start = time_ns()
        self.time_stop = None
        self.time_delta = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.time_stop = time_ns()
        self.time_delta = (self.time_stop - self.time_start) / 1000000000
        return exc_type is None
