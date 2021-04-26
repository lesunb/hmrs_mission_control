class PowerSource:
    def __init__(self):
        pass

class PowerGrid(PowerSource):
    def __init__(self):
        pass

class Battery(PowerSource):
    def __init__(self, capacity, charge):
        pass

class PowerConsumptionModel:
    def __init__():
        pass

class ConstantPowerConsumptionModel:
    def __init__(self, consumption_rate):
        self.consumption_rate = consumption_rate

    def estimate(self, time):
        return consumption_rate * time