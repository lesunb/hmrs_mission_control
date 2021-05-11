import logging

from abc import abstractclassmethod
from deeco.runnable import NodePlugin

from typing import TypeVar, Generic

logger = logging.getLogger('service')

T = TypeVar('T')
def filter_pkg(method, on_error, messagType):
    def filtered_call(packet):
        if isinstance(packet, messagType):
            try:
                method(packet)
            except Exception as e:
                on_error(packet, e)
                logger.error(e)
    return filtered_call

class Server(Generic[T], NodePlugin):
    def __init__(self, node, messagType):
        super().__init__(node)
        self.node.networkDevice.add_receiver(filter_pkg(self.receive, self.handle_error, messagType=messagType))
        logger = logging.getLogger(f'[{messagType} service')

    @abstractclassmethod
    def receive(self, request: T):
        pass

    @abstractclassmethod
    def handle_error(self, request: T, error):
        pass
