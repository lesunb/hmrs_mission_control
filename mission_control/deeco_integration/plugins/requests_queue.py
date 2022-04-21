from deeco.core import NodePlugin
from typing import List
from mission_control.data_model.restrictions import Request

def request_sequence_gen(requests: List[Request]):
    requests.sort(key=lambda req: req.timestamp)
    for req in requests:
        yield req
    yield None

class RequestsQueue(NodePlugin):
    DEFAULT_STEP_MS = 100

    def __init__(self, node, initial_requests = None):
        super().__init__(node)
        node.requests_queue = []

        self.requests_sequence = request_sequence_gen(initial_requests) # generator for workload
        self.next = next(self.requests_sequence) # next request to be triggered

    def run(self, scheduler):
        scheduler.set_periodic_timer(self.trigger_request, period_ms=self.DEFAULT_STEP_MS)

    def trigger_request(self, time_ms):
        # while didn't get to the end of the gen, and the next is due
        while self.next is not None and self.next.timestamp <= time_ms:
            request = self.next
            self.node.requests_queue.append(request)
            self.next = next(self.requests_sequence)
        # TODO if self.next is None, remove the timer
