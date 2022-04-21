import shortuuid

class UUID(str):
    pass

class Identifiable:

    def __init__(self, uuid = None):
        super().__init__()
        if uuid:
            self.__uuid = uuid
        else:
            self.__uuid: UUID = self.gen_new_uuid()
    
    @staticmethod
    def gen_new_uuid() -> UUID:
        return shortuuid.uuid()

    @property
    def uuid(self):
        return self.__uuid

    def isid(self, uuid: str) -> bool:
        return self.__uuid == uuid

    def same_uuid(self, other: Any):
        return other.uuid and other.uuid == self.uuid
