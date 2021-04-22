from mission_control.coordinator import coordinator_factory

def test_create_coordinator():
    environment_descriptors = None
    skill_descriptors = None
    coordinator = coordinator_factory(id = 'Mission_Coordinator')
    assert coordinator.id == 'Mission_Coordinator'