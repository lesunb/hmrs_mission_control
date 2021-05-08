
class Mapping:
    op = None
    def apply():
        pass
    
    @staticmethod
    def apply_all(mappings: [], objs):
        for mapping in mappings:
            mapping.apply(objs)

class AddToSet(Mapping):
    op = 'add_to_set'
    def __init__(self, path, value):
        self.path = path
        self.value = value
    
    def apply(self, obj):
        target = getattr(obj, self.path)
        target.append(obj)

class SetValue(Mapping):
    op = 'set_value'
    def __init__(self, path, value):
        self.path = path
        self.value = value
    
    def apply(self, obj):
        setattr(obj, self.path, self.value)