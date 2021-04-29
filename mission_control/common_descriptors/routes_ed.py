from ..estimate.core import EnvironmentDescriptor
from mission_control.core import POI

class Edge:
    pass

class Nodes:
    pass

class Segment:
    def __init__(self, label, origin:Edge, dest:Edge, len, **properties):
        pass

class Map:
    def __init__(self, pois:[POI], segments: [Segment]):
        pass

class Route:
    def __init__(self, origin: POI, destination: POI, segments = []):
        self.origin = origin
        self.destination = destination
        self.total_distance = 100 # calculate from segments
        pass

    def get_way_points(self) -> [Nodes]:
        # TODO
        pass

    def get_route_progress(self, next_way_point, curr_position):
        # TODO
        pass

    def get_distance(self):
        # TODO
        return self.total_distance


class RoutesEnvironmentDescriptor(EnvironmentDescriptor):
    def __init__(self, map:Map):
        self.map = map

    def block_segment(label):
        pass

    def get(self, origin: POI, destination: POI) -> Route:
        # TODO calculate route
        route = Route(origin=origin, destination=destination)
        return route

    
