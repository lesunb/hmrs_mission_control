class Scenario:
    def __init__(self, experiment_code, id, code, robots, requests, factors, persons, **kargs):
        self.experiment_code, self.id, self.code, self.robots, self.requests, self.factors, self.persons = experiment_code, id, code, robots, requests, factors, persons
