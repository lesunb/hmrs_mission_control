
class Role:
    pass

class Runnable():
    
    def run(self):
        pass

class Node(Runnable):
    def __init__(self, components=[]):
        pass

    def run(self):
        pass

class Component():
    def __init__(self, id, features = [], knowledge = None, processes = []):
        self.id = id

class Ensemble():
    def __init__(self, id, coordinator_role = [], member_role = [], membership = [], knowledge_exchange = []):
        self.id = id

class Process():
    def __init__(self, func, scheduling):
        pass

def process():
    pass

def fun(args):
    return InjectedOutjectedFunc(args)


class Knowledge:
    def __init__(self, **kwargs):
        pass
