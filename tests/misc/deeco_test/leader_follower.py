from deeco.plugins.ensemblereactor import EnsembleMember
from random import Random

from deeco.core import BaseKnowledge
from deeco.core import Component
from deeco.core import Node
from deeco.core import ComponentRole
from deeco.core import process
from deeco.position import Position

from deeco.core import EnsembleDefinition, BaseKnowledge
from deeco.mapping import SetValue

# Role
class Rover(ComponentRole):
    def __init__(self):
        super().__init__()
        self.position = None
        self.goal = None

class LeaderRole(ComponentRole):
    pass

# Component
class Leader(Component):
    SPEED = 0.01
    random = Random(0)
    
    @staticmethod
    def gen_random_position():
        return Position(Leader.random.uniform(0, 1), Leader.random.uniform(0, 1))

    # Knowledge definition
    class Knowledge(LeaderRole, Rover, BaseKnowledge):
        def __init__(self):
            super().__init__()

    # Component initialization
    def __init__(self, node: Node):
        super().__init__(node)

        # Initialize knowledge
        self.knowledge.position = node.positionProvider.get()
        self.knowledge.goal = self.gen_random_position()

    @process(period_ms=10)
    def update_time(self, node: Node):
        self.knowledge.time = node.runtime.scheduler.get_time_ms()

    @process(period_ms=100)
    def sense_position(self, node: Node):
        self.knowledge.position = node.positionProvider.get()

    @process(period_ms=1000)
    def set_goal(self, node: Node):
        if self.knowledge.position == self.knowledge.goal:
            self.knowledge.goal = self.gen_random_position()
            node.walker.set_target(self.knowledge.goal)
        node.walker.set_target(self.knowledge.goal)


class FollowerRole(ComponentRole):
    pass

class Follower(Component):
    SPEED = 0.02
    # Knowledge definition
    class Knowledge(FollowerRole, Rover, BaseKnowledge):
        def __init__(self):
            super().__init__()

    # Component initialization
    def __init__(self, node: Node):
        super().__init__(node)

        # Initialize knowledge
        self.knowledge.position = node.positionProvider.get()
        self.knowledge.goal = None

    @process(period_ms=10)
    def update_time(self, node: Node):
        self.knowledge.time = node.runtime.scheduler.get_time_ms()

    @process(period_ms=100)
    def sense_position(self, node: Node):
        self.knowledge.position = node.positionProvider.get()

    @process(period_ms=100)
    def set_goal(self, node: Node):
        node.walker.set_target(self.knowledge.goal)


# Role
class Group(ComponentRole):
    def __init__(self):
        super().__init__()
        self.center = None
        self.members = []


class LeaderFollowingGroup(EnsembleDefinition):
    
    class RobotGroupKnowledge(BaseKnowledge, Group):
        def __init__(self):
            super().__init__()

        def __str__(self):
            return self.__class__.__name__ + " centered at " + str(self.center) + " with component ids " + str(list(map(lambda x: x.id, self.members)))

    def __init__(self):
        super().__init__(coordinator=LeaderRole, member=FollowerRole)
 
    def fitness(self, a: Leader.Knowledge, b: Follower.Knowledge):
        return 1.0 / a.position.dist_to(b.position)

    def membership(self, a: Leader.Knowledge, b: Follower.Knowledge):
        assert isinstance(a, LeaderRole)
        assert isinstance(b, FollowerRole)
        return True

    def knowledge_exchange(self, coord: Leader.Knowledge, member: EnsembleMember[Follower.Knowledge]):
        set_goal = SetValue('goal', coord.position)
        return (coord, [set_goal])

    def __str__(self):
        return self.__class__.__name__


