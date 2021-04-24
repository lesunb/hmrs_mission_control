from abc import abstractclassmethod
from deeco.runnable import NodePlugin

from typing import TypeVar, Generic, List


T = TypeVar('T')
def filter_pkg(method, messagType):
    def filtered_call(packet):
        if isinstance(packet, messagType):
            method(packet)
    return filtered_call

class Server(Generic[T], NodePlugin):
    def __init__(self, node, messagType):
        super().__init__(node)
        self.node.networkDevice.add_receiver(filter_pkg(self.receive, messagType=messagType))

    @abstractclassmethod
    def receive(self, request: T):
        pass
        