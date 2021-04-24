from mission_control.plugins.service import Server
from .request import Request

class HandleRequestServer(Server[Request]):
    def __init__(self, node):
        super().__init__(node, Request)
        pass

    def receive(self, request: Request): # TODO response
        print(request)


