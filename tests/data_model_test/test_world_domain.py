import pytest

from ..world_collector import *
from mission_control.data_model.world_model import InvalidWorldModelSymbolError, WorldModelDomain


def test_one():
    assert 1

def test_world_model_raise_not_found(collector_world_model_domain: WorldModelDomain):
    with pytest.raises(InvalidWorldModelSymbolError) as e_info:
        room = collector_world_model_domain.get('ROOM', 'location')


def test_world_model_find_location(collector_world_model_domain: WorldModelDomain):
    room = collector_world_model_domain.get('IC Corridor', 'location')
    assert room.label == 'IC Corridor' 

def test_world_model_query_enum(collector_world_model_domain: WorldModelDomain):
    task_type = collector_world_model_domain.get('navigation', 'task_type')
    assert task_type.value == 'navigation' 


    