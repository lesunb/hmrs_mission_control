from abc import abstractmethod

from mission_control.coordination.assingment import Channel
from .local_mission import SkillImplementation, TickStatus
from ..coordination.coordination import Coordination
from utils.logger import Logger
from typing import Generic, List, TypeVar

T = TypeVar("T")

class CoordinationSkill(SkillImplementation, Generic[T]):
    """ Abstract implementation of a skill that requires 
    coordination with other components to realize a task """
    
    def __init__(self, coordination: T, logger: Logger):
        self.coordination = coordination
        self.channels: dict[int, Channel] = {}
        self.l = logger

    def load(self, task, host):
        self.host = host
        self.task = task
    
    def tick(self) -> TickStatus:
        next(run(self.procedure))

    @abstractmethod
    def procedure(self):
        pass

    @abstractmethod
    def on_complete(self):
        pass

    def queue_task(self, task):
        # TODO create Promise
        self.host.enque_task(
            Wrapper(task, on_complete)
        )

    async def request(self, channel, **kargs):
        """ get a channel specified by the coordination """
        if not self.channels[channel]:
            self.l.info('instantiating channel')
            self.channels[channel] = self.lookup(self.coordination, channel)

        return self.channels[channel].request(**kargs)
            

class SkillWrapper:
    pass