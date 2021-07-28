class ConstantsProvider:
    def __init__(self):
        self.constants  ={}
    
    def get(self, key, default):
        return self.constants.get(key, default)
    
    def set(self, key, value):
        self.constants[key] = value