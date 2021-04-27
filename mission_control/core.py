class MissionContext:
    pass

class POI:
    def __init__(self, label):
        self.label = label

class Worker:
    """
    Entities that can realize tasks on missions. 
    Minimal representation or robots for realizing the task allocation. 
    Snapshot view for realizing a short living evaluation
    """
    def __init__(self, position=None, components = [], skills = []):
        self.position = position
        self.components = components
        self.skills = skills
