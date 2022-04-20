
from mission_control.data_model.ihtn import AbstractTask
from resources.world_lab_samples import pickup_ihtn
from resources.world_lab_samples import poi 

def test_create_ihtn():
    root, enum = pickup_ihtn(poi.ic_room_1.value)
    assert isinstance(root, AbstractTask)
