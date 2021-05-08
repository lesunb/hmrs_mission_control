from ..estimate.core import EnvironmentDescriptor
from mission_control.core import POI


class Edge:
    def __init__(self, origin, dest):
        self.origin = origin
        self.dest = dest


class Nodes:
    def __init__(self, label, coords):
        self.label = label
        self.edges = []
        self.coords = coords

    def add_edges(self, edges: [Edge]):
        for edge in edges:
            self.edges.append(Edge(self, edge))


class Map:
    def __init__(self):
        self.nodes = []

    def add_nodes(self, nodes: [Nodes]):
        for node in nodes:
            self.nodes.append(node)

    def get_all_waypoints(self) -> [POI]:
        pois = []
        for node in self.nodes:
            pois.append(POI(node.label))
        return pois

    def get_node(self, label) -> Nodes:
        for node in self.nodes:
            if label == node.label:
                return node

    def get_waypoint(self, poi: POI) -> Nodes:
        return self.get_node(poi.label)


class Route:
    def __init__(self, origin: Nodes, destination: Nodes, nodes=[Nodes]):
        self.origin = origin
        self.destination = destination
        self.total_distance = None
        self.nodes = nodes

    def get_all_waypoints(self) -> [POI]:
        pois = []
        for node in self.nodes:
            pois.append(POI(node.label))
        return pois

    def get_node(self, label) -> Nodes:
        for node in self.nodes:
            if label == node.label:
                return node

    def get_waypoint(self, poi: POI) -> Nodes:
        return self.get_node(poi.label)

    def get_route_progress(self,  curr_position: Nodes):
        curr_index = self.nodes.index(curr_position)
        return sum(self.euclidean_distance(x, y) for x, y in
                   zip(self.nodes, self.nodes[1:curr_index+1])) / self.total_distance

    def euclidean_distance(self, a: Nodes, b: Nodes):
        return (sum((x0 - x1) ** 2 for x0, x1 in zip(a.coords, b.coords))) ** 0.5

    def get_distance(self):
        self.total_distance = sum(self.euclidean_distance(x, y) for x,y in zip(self.nodes, self.nodes[1:]))
        return self.total_distance


class RoutesEnvironmentDescriptor(EnvironmentDescriptor):
    def __init__(self, map: Map):
        self.map = map

    def block_segment(label):
        pass

    def calculate_route(self, origin: Nodes, destination: Nodes, visited=set(), path=[]):
        if origin not in visited:
            visited.add(origin)
            if origin.label == destination.label:
                return True
            for edge in origin.edges:
                if self.calculate_route(edge.dest, destination, visited, path):
                    path.insert(0, edge.dest)
                    break
            return path

    def get(self, origin: Nodes, destination: Nodes) -> Route:
        path = self.calculate_route(origin, destination)
        route = Route(origin=origin, destination=destination, nodes=path)
        route.get_distance()
        return route


def create_hospial_scenario_map() -> Map:
    map = Map()
    respiratory_control = Nodes("Respiratory Control", [-37, 35])
    ic_corridor = Nodes("IC Corridor", [-37, 15])
    ic_room_1 = Nodes("IC Room 1", [-38, 35])
    ic_room_2 = Nodes("IC Room 2", [-34, 35])
    ic_room_3 = Nodes("IC Room 3", [-38, 23])
    ic_room_4 = Nodes("IC Room 4", [-34, 17.5])
    ic_room_5 = Nodes("IC Room 5", [-38, 21.5])
    ic_room_6 = Nodes("IC Room 6", [-38, 10])
    pc_corridor = Nodes("PC Corridor", [-19, 16])
    pc_room_1 = Nodes("PC Room 1", [-28.5, 18])
    pc_room_2 = Nodes("PC Room 2", [-27.4, 18])
    pc_room_3 = Nodes("PC Room 3", [-21, 18])
    pc_room_4 = Nodes("PC Room 4", [-19, 18])
    pc_room_5 = Nodes("PC Room 5", [-13.5, 18])
    pc_room_6 = Nodes("PC Room 6", [-11.5, 18])
    pc_room_7 = Nodes("PC Room 7", [-4, 18])
    pc_room_8 = Nodes("PC Room 8", [-27, 13])
    pc_room_9 = Nodes("PC Room 9", [-26, 13])
    pc_room_10 = Nodes("PC Room 10", [-18, 13])
    reception = Nodes("Reception", [-1, 20])
    pharmacy_corridor = Nodes("Pharmacy Corridor", [0, 8])
    pharmacy = Nodes("Pharmacy", [-2, 2.6])

    respiratory_control.add_edges([ic_corridor])

    ic_corridor.add_edges([respiratory_control, ic_room_1, ic_room_2, ic_room_3,
                           ic_room_4, ic_room_5, ic_room_6, pc_corridor])

    ic_room_1.add_edges([ic_corridor])
    ic_room_2.add_edges([ic_corridor])
    ic_room_3.add_edges([ic_corridor])
    ic_room_4.add_edges([ic_corridor])
    ic_room_5.add_edges([ic_corridor])
    ic_room_6.add_edges([ic_corridor])

    pc_corridor.add_edges([ic_corridor, pharmacy_corridor, pc_room_1,
                           pc_room_2, pc_room_3, pc_room_4, pc_room_5,
                           pc_room_6, pc_room_7, pc_room_8, pc_room_9,
                           pc_room_10])

    pc_room_1.add_edges([pc_corridor])
    pc_room_2.add_edges([pc_corridor])
    pc_room_3.add_edges([pc_corridor])
    pc_room_4.add_edges([pc_corridor])
    pc_room_5.add_edges([pc_corridor])
    pc_room_6.add_edges([pc_corridor])
    pc_room_7.add_edges([pc_corridor])
    pc_room_8.add_edges([pc_corridor])
    pc_room_9.add_edges([pc_corridor])
    pc_room_10.add_edges([pc_corridor])

    pharmacy_corridor.add_edges([reception, pc_corridor, pharmacy])
    reception.add_edges([pharmacy_corridor])
    pharmacy.add_edges([pharmacy_corridor])

    map.add_nodes([respiratory_control, ic_corridor, ic_room_1, ic_room_2,
                   ic_room_3, ic_room_4, ic_room_5, ic_room_6, pc_corridor,
                   pc_room_1, pc_room_2, pc_room_3, pc_room_4, pc_room_5,
                   pc_room_6, pc_room_7, pc_room_8, pc_room_9, pc_room_10,
                   pharmacy_corridor, reception, pharmacy])
    return map
