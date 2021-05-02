

import logging

from .plugins.service import Server

from .request import Request
from mission_control.manager.coalition_formation import CoalitionFormationProcess
from mission_control.mission.ihtn import Task


logging
logging.basicConfig(filename='xx.logx', filemode='w', encoding='utf-8', level=logging.DEBUG)

class HandleRequestServer(Server[Request]):
    def __init__(self, node, cf_manager: CoalitionFormationProcess):
        super().__init__(node, Request) # register to listen
        self.cf_manager = cf_manager

    def receive(self, request: Request): # TODO response
        print(f'received request id: {request.id}')
        task = request.content
        mission_context = self.cf_manager.create_coalition(task)
        # TODO send to supervisor
        print(f'request id: {request.id} ended')


    def handle_error(self, request: Request, exception):
        print('error handling request - request content is not a task instance')
        print(exception)