from mission_control.common_descriptors.routes_ed import RoutesEnvironmentDescriptor
from mission_control.data_model import POI

from hospital_world.hospital_map import create_hospital_scenario_map
import math

def test_routes():
    map = create_hospital_scenario_map()
    routes_ed: RoutesEnvironmentDescriptor = RoutesEnvironmentDescriptor(map)
    route = routes_ed.get(POI("Respiratory Control"), POI("IC Room 1"))
    assert route is not None


def test_routes_going_and_back_should_be_same_distance():
    map = create_hospital_scenario_map()
    routes_ed: RoutesEnvironmentDescriptor = RoutesEnvironmentDescriptor(map)
    route1 = routes_ed.get(POI("IC Room 3"), POI("IC Room 1"))
    route2 = routes_ed.get(POI("IC Room 1"), POI("IC Room 3"))
    assert route1.get_distance() == route2.get_distance()


def test_routes_going_and_back_should_be_same_distance_2():
    map = create_hospital_scenario_map()
    routes_ed: RoutesEnvironmentDescriptor = RoutesEnvironmentDescriptor(map)
    route1 = routes_ed.get(POI("IC Room 2"), POI("PC Room 5"))
    route2 = routes_ed.get(POI("PC Room 5"), POI("IC Room 2"))
    assert route1.get_distance() == route2.get_distance()


def test_routes_going_and_back_should_be_same_distance_2():
    map = create_hospital_scenario_map()
    routes_ed: RoutesEnvironmentDescriptor = RoutesEnvironmentDescriptor(map)
    route1 = routes_ed.get(POI("PC Room 7"), POI("PC Room 8"))
    route2 = routes_ed.get(POI("PC Room 8"), POI("PC Room 7"))
    assert route1.get_distance() == route2.get_distance()


def dist(coorda, coordb):
    return math.sqrt((coorda[0]-coordb[0]) ** 2 + (coorda[1]-coordb[1])**2)

def test_no_diagonal_routes():
    map = create_hospital_scenario_map()
    routes_ed: RoutesEnvironmentDescriptor = RoutesEnvironmentDescriptor(map)
    errors = []
    for origin in map:
        for dest in map:
            if origin == dest or 'Corridor' in origin.label+dest.label:
                continue
            route = routes_ed._get(origin, dest)
            assert route.get_distance() > 0, f'error in {origin.label} to {dest.label}'
            wps = route.get_all_waypoints()
            prev = None
            last_dist = float('inf')
            for wp in wps[1:-1]:
                if (prev and (prev[0] != wp[0] and prev[1] != wp[1])):
                    errors.append(f'error in {origin.label} to {dest.label}, {prev, wp}')
                    print(f'error in {origin.label} to {dest.label} {routes_ed._get(origin, dest).get_all_waypoints()}')
                prev = wp
    assert not errors, errors



    
# def test_always_getting_closer():
#     map = create_hospital_scenario_map()
#     routes_ed: RoutesEnvironmentDescriptor = RoutesEnvironmentDescriptor(map)
#     errors = []
#     for origin in map:
#         for dest in map:
#             if origin == dest or 'Corridor' in origin.label+dest.label:
#                 continue
#             route = routes_ed._get(origin, dest)
#             wps = route.get_all_waypoints()
#             last_dist = route.get_distance()
#             for poi in wps[1:-1]:
#                 new_dist = dist(poi, dest.coords)
#                 if (new_dist >= last_dist):
#                     errors.append(f'error in {origin.label} to {dest.label} |{poi}| {route.get_all_waypoints()}')
#                     print(f'error in {origin.label} to {dest.label}   {routes_ed._get(origin, dest).get_all_waypoints()}')
#                 last_dist = new_dist
#     assert not errors, errors


def test_origin_is_the_fist_waypoint():
    def dist(coorda, coordb):
        return math.sqrt((coorda[0]-coordb[0]) ** 2 + (coorda[1]-coordb[1])**2)

    map = create_hospital_scenario_map()
    routes_ed: RoutesEnvironmentDescriptor = RoutesEnvironmentDescriptor(map)
    errors = []
    for origin in map:
        for dest in map:
            if origin == dest or 'Corridor' in origin.label+dest.label:
                continue
            route = routes_ed._get(origin, dest)
            wps = route.get_all_waypoints()
            assert wps[0] == tuple(origin.coords)
            assert wps[-1] == tuple(dest.coords)

    assert not errors, errors