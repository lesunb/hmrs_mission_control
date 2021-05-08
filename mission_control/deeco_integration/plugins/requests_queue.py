from queue import SimpleQueue
from deeco.runnable import NodePlugin

class RequestsQueue(NodePlugin):
    DEFAULT_STEP_MS = 100

    def __init__(self, node):
        super().__init__(node)
        node.requests_queue = SimpleQueue()
