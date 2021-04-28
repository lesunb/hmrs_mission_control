class MissionContext:
    pass

class POI:
    def __init__(self, label):
        self.label = label

class Capability:
    class Property:
        def __init__(self, key: str, value, u: str=None, *kwargs):
            self.key = key
            self.value = value
            self.u = u
    
    def __init__(self, **kwargs):
        self.properties = []
        for key, value in kwargs.items():
            params = None
            if key == 'u': continue
            if kwargs['u'] is not None:
                params = {'u': kwargs['u']}
            self.properties.append(Capability.Property(key=key, value = value, **params))


class Worker:
    """
    Entities that can realize tasks on missions. 
    Minimal representation or robots for realizing the task allocation. 
    Snapshot view for realizing a short living evaluation
    """
    def __init__(self, position=None, capabilities = [], skills = []):
        self.position = position
        self.skills = skills
        self.properties_register = {}
        for capability in capabilities:
            self.register(capability)

    def get(self, prop):
        return self.properties_register[prop]

    def register(self, capability: Capability):
        for prop in capability.properties:
            self.properties_register[prop.key]=prop.value

def worker_factory(position, capabilities, skills):
    # TODO check if have the required capabilities
    unit = Worker(position=position, capabilities=capabilities, skills=skills)
    return unit
