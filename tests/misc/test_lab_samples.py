
from mission_control.data_model import AbstractTask
from hospital_world.lab_samples_mission import pickup_ihtn, poi

def test_create_ihtn():
    root, enum = pickup_ihtn(poi.ic_room_1.value)
    assert isinstance(root, AbstractTask)
