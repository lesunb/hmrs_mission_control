from mission_control.core import MissionContext, LocalMission, Worker
from mission_control.deeco_integration.coordinator import Coordinator

def test_get_free_workers():
    w1 = Worker(position=None, capabilities = [], skills = [])
    w2 = Worker(position=None, capabilities = [], skills = [])
    w3 = Worker(position=None, capabilities = [], skills = [])

    mission1 = MissionContext(global_plan=None)
    mission1.local_missions = [LocalMission(None, None, None, worker=w1)]
    
    coord = Coordinator(node = None, required_skills = None, cf_process = None)
    coord.knowledge.missions = [mission1]
    coord.knowledge.active_workers = [w1, w2, w3]

    assert set([w2, w3]) == coord.get_free_workers()

    
