from utils.timer import Timer
from deeco.sim import SimScheduler

class DeecoTimer(Timer):
    
    def __init__(self):
        self.scheduler:SimScheduler = None

    def now(self):
        return self.scheduler.get_time_ms()