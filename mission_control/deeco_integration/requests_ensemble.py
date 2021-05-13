from deeco.core import EnsembleDefinition, BaseKnowledge, ComponentRole
from deeco.packets import Packet, PacketType

from .client import MissionClient
from .requests_server_component import RequestsHandler

class RequestPacket(Packet):
    def __init__(self, id, timestamp = None, content=None):
        super().__init__(PacketType.RAW)
        self.id = id
        self.timestamp = timestamp
        self.content = content

class MissionRequestsRole(ComponentRole):
    def __init__(self):
        self.requests = []


class MissionRequestsEnsemble(EnsembleDefinition):
    class MissionKnowledge(BaseKnowledge, MissionRequestsRole):
        def __init__(self):
            super().__init__()

        def __str__(self):
            return self.__class__.__name__ + " with component ids " + str(list(map(lambda x: x.id, self.members)))

    def __init__(self):
        super().__init__(coordinator=RequestsHandler, member=MissionClient)
        pass

    def fitness(self, coord: RequestsHandler, member: MissionClient):
        return 1

    def membership(self, coord: RequestsHandler, member: MissionClient):
        assert isinstance(coord, RequestsHandler)
        assert isinstance(member, MissionClient)

        return True
        

    def knowledge_exchange(self, coord: RequestsHandler, member: MissionClient):
        knowledge = self.MissionKnowledge()
        coord.requests.extend(member.requests)
        knowledge.members = [coord, member]
        return coord, None

    def __str__(self):
        return self.__class__.__name__
