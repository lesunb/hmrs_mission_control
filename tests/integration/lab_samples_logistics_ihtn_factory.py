mport pytest

from gmrs.model.mission import Mission
from gmrs.model.goal import Goal
from gmrs.model.task import Task

from gmrs.model.location import Location

from gmrs.model.robot import Robot

from gmrs.model.capability import Capability

from gmrs.operators.operators import SEQ
from gmrs.utils.task_refinement_utils import rft
from gmrs.environment.map_of_distance import MapOfDistance


from ..minimal_world.skill_visit import VisitWithMoveBase


# world
# locations
class world:
    robots_room = Location('robots_room')
    room = Location('room')
    map = MapOfDistance()

    map.add_direct_segment(robots_room, room, 100)


class mission:

    # Task Refinement
    # tidy
    identify_out_of_place_objects = Task('Identify out of place objects')
    move_objects = Task('Move Objects')
    tidy_objects = rft(Task('Tidy Objects of [room]'),
                       SEQ, identify_out_of_place_objects, move_objects)

    # clean
    sweep_floor = Task('Sweep Floor')
    uv_light_sterilize = Task('UV-Light Sterilize')

    clean_room = rft(Task('Clean [room]'),
                     SEQ, sweep_floor, uv_light_sterilize)

    # root
    clean_and_tidy_room = rft(Task('Clean and Tidy [room]'),
                              SEQ, tidy_objects, clean_room)

    goal = Goal(clean_and_tidy_room)
    objective = None


class robots:
    move_configurations = {
        'slow': {'speed': 10},
        'default': 'slow',
    }

    move = Capability('move', configs=move_configurations)

    skill = VisitWithMoveBase()

    r1 = Robot('r1',
               location=world.robots_room,
               capabilities=[move],
               skills=None)


class scenario:
    world = world
    mission = mission
    robots = robots


@pytest.fixture
def clean_room_scenario():
    return scenario