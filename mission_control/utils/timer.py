from abc import abstractmethod

class Timer:
    def __init__(self):
        pass

    @abstractmethod
    def now(self):
        pass
