import json
from abc import abstractclassmethod

from deeco.runnable import NodePlugin
from deeco.plugins.simplenetwork import SimpleNetwork

from ..request import Request

def read(path):
    data = None
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def workload_gen(workload):
    workload.sort(key=lambda req: req['timestamp'])
    id_count = 0
    for req in workload:
        id_count += 1
        request = Request(id = id_count)
        for key in req:
            setattr(request, key, req[key])
        yield request
    yield None

class WorkloadLoader(NodePlugin):
    DEFAULT_STEP_MS = 100

    def __init__(self, node, destination, workload: [Request] = None, file_paht:str = None):
        super().__init__(node)
        self.destination_id = destination.id # node that will receive the requests

        workload_raw: [Request] = workload if workload is not None else read(file_paht)

        self.workload = workload_gen(workload_raw) # generator for workload
        self.next = next(self.workload) # next request to be triggered
        self.network: SimpleNetwork = node.networkDevice

    def run(self, scheduler):
        scheduler.set_periodic_timer(self.trigger_request, period_ms=self.DEFAULT_STEP_MS)

    def trigger_request(self, time_ms):
        # while didn't get to the end of the gen, and the next is due
        while self.next is not None and self.next.timestamp <= time_ms:
            request = self.next
            self.network.send(self.destination_id, request)
            self.next = next(self.workload)
        # TODO if self.next is None, remove the timer





        