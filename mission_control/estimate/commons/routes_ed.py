from ..core import EnvironmentDescriptor

class Edge:
    pass

class Segment:
    def __init__(self, label, origin:Edge, dest:Edge, len, **properties):
        pass

class POI:
    def __init__(self, label, edge: Edge):
        pass

class Waypoint:
    def __init__(self, x, y):
        pass

class Map:
    def __init__(self, pois:[POI], segments: [Segment]):
        pass

class Route:
    def __init__(self, segments, destination):
        self.total_distance = 0 # calculate from segments
        pass

    def get_way_points(self) -> [Waypoint]:
        pass

    def get_route_progress(self, next_way_point, curr_position):
        pass


class RoutesEnvironmentDescriptor(EnvironmentDescriptor):
    def __init__(self, map):
        self.map = map

    def block_segment(label):
        pass

    def get(self, point_a: POI, point_b: POI) -> Route:
        return [Waypoint(0, 0), Waypoint(1, 1), Waypoint(2, 2)]

    
