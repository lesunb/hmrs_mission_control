from typing import List, Tuple
from ..coordination import EnvironmentDescriptor
from ..data_model import POI

class Edge:
    def __init__(self, origin, dest):
        self.origin = origin
        self.dest = dest


class Nodes:
    def __init__(self, label, coords):
        self.label = label
        self.edges = []
        self.coords = coords

    def add_edges(self, edges: List[Edge]):
        for edge in edges:
            self.edges.append(Edge(self, edge))


class Map:
    def __init__(self):
        self.nodes = []

    def add_nodes(self, nodes: List[Nodes]):
        for node in nodes:
            self.nodes.append(node)

    def get_all_waypoints(self) -> List[POI]:
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

    def __iter__(self):
        for node in self.nodes:
            yield node
        return



class Route:
    def __init__(self, origin: Nodes, destination: Nodes, nodes=[Nodes]):
        self.origin = origin
        self.destination = destination
        self.total_distance = None
        self.nodes = [origin] + nodes

    def get_all_waypoints(self) -> List[Tuple[float, float]]:
        pois = []
        for node in self.nodes:
            pois.append(tuple(node.coords))
        return pois

    def get_node(self, label) -> Nodes:
        for node in self.nodes:
            if label == node.label:
                return node

    def get_waypoint(self, poi: POI) -> Nodes:
        return self.get_node(poi.label)

    def get_route_progress(self,  curr_position: Nodes):
        curr_index = self.nodes.index(curr_position)
        if curr_index == len(self.nodes) - 1:
            return 1
        return sum(self.euclidean_distance(x, y) for x, y in
                   zip(self.nodes[curr_index:], self.nodes[curr_index+1:])) / self.total_distance

    def euclidean_distance(self, a: Nodes, b: Nodes):
        return (sum((x0 - x1) ** 2 for x0, x1 in zip(a.coords[:2], b.coords[:2]))) ** 0.5

    def get_distance(self):
        self.total_distance = sum(self.euclidean_distance(x, y) for x,y in zip(self.nodes, self.nodes[1:]))
        return self.total_distance

    def simplify(self):
        index = 1
        while index < len(self.nodes)-1:
            if (self.nodes[index-1].coords[0] == self.nodes[index].coords[0] == self.nodes[index+1].coords[0]
                or self.nodes[index-1].coords[1] == self.nodes[index].coords[1] == self.nodes[index+1].coords[1]):
                self.nodes.pop(index)
            else:
                index += 1


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
        route.simplify()
        route.get_distance()
        return route

    def get_position(self, poi: POI):
        return self.nodes_dict[poi.label]

    def get(self, origin:POI, destination:POI) -> Route:
        return self._get(self.nodes_dict[origin.label], \
             self.nodes_dict[destination.label])
