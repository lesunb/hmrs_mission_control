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
    def __init__(self, routes_map: Map):
        self.routes_map = routes_map
        self.nodes_dict = self.init_nodes_dict(routes_map)

    @staticmethod
    def init_nodes_dict(routes_map):
        nodes_dict = {}
        for node in routes_map.nodes:
            nodes_dict[node.label] = node
        return nodes_dict
            
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

    def _get(self, origin: Nodes, destination: Nodes) -> Route:
        path = self.calculate_route(origin, destination, set(), [])
        route = Route(origin=origin, destination=destination, nodes=path)
        route.get_distance()
        return route

    def get(self, origin:POI, destination:POI):
        return self._get(self.nodes_dict[origin.label], \
             self.nodes_dict[destination.label])


