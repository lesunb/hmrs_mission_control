from deeco.packets import Packet, PacketType

class Request(Packet):
    def __init__(self, id, timestamp = None, content=None):
        super().__init__(PacketType.RAW)
        self.id = id
        self.timestamp = timestamp
        self.content = content
