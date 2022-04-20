from mission_control.data_model.core import MissionContext, LocalMission, Worker
from mission_control.deeco_integration.coordinator import Coordinator

class NodeMock():
    def __init__(self):
        self.id = 0

def test_get_free_workers():
    w1 = Worker(location=None, capabilities = [], skills = [])
    w2 = Worker(location=None, capabilities = [], skills = [])
    w3 = Worker(location=None, capabilities = [], skills = [])

    mission1 = MissionContext(request_id=0, global_plan=None)
    mission1.local_missions = [LocalMission(None, None, None, worker=w1)]
    
    coord = Coordinator(node = NodeMock(), required_skills = None, cf_process = None)
    coord.knowledge.missions = [mission1]
    coord.knowledge.active_workers = dict(map(lambda w: (w.uuid, w), [w1, w2, w3]))


    w2_and_w3 = dict(map(lambda w: (w.uuid, w), [w2, w3]))

    assert w2_and_w3 == dict(coord.get_free_workers())

    
