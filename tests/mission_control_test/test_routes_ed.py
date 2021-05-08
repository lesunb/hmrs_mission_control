from mission_control.common_descriptors.routes_ed import RoutesEnvironmentDescriptor
from mission_control.core import POI

from ..hospital_map import create_hospial_scenario_map

def test_routes():
    map = create_hospial_scenario_map()
    routes_ed: RoutesEnvironmentDescriptor = RoutesEnvironmentDescriptor(map)
    route = routes_ed.get(POI("Respiratory Control"), POI("IC Room 1"))
    assert route is not None

# def test_routes_going_and_back_should_be_same_distance():
#     map = create_hospial_scenario_map()
#     routes_ed: RoutesEnvironmentDescriptor = RoutesEnvironmentDescriptor(map)
#     route1 = routes_ed.get(POI("IC Room 3"), POI("IC Room 1"))
#     route2 = routes_ed.get(POI("IC Room 1"), POI("IC Room 3"))
#     assert route1.get_distance() == route2.get_distance()

