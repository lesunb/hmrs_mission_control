

from .service import Server

from ..requests_ensemble import RequestPacket


class HandleRequestServer(Server[RequestPacket]):
    def __init__(self, node):
        super().__init__(node, RequestPacket) # register to listen

    def receive(self, request: RequestPacket, time_ms): # TODO response
        print(f'received request id: {request.id} at {time_ms}')
        request = request.content
        mission_context = self.cf_manager.create_coalition(request.task)
        # TODO send to supervisor
        print(f'request id: {request.id} ended')


    def handle_error(self, request: RequestPacket, exception):
        print('error handling request - request content is not a task instance')
        print(exception)