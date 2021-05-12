from queue import SimpleQueue
from deeco.runnable import NodePlugin

class RequestsQueue(NodePlugin):
    DEFAULT_STEP_MS = 100

    def __init__(self, node, initial_requests = None):
        super().__init__(node)
        node.requests_queue = []
        if initial_requests:
            for request in initial_requests:
                node.requests_queue.append(request)
