class Engine:
    pass

class LocalEngine(Engine):
    """ Local Engine """

    def __init__(self, plugins = None, components = [], end_time = float("inf"), frequency=60):
        self.ensembles = []
        self.plugins = plugins
        self.components = components
        self.time = 0
        self.frequency = frequency


    def run(self):
        while self.time < self.end_time:
            self.exec(time)
            # todo wait(1/self.frequency)


    def exec(self, time):
        self.time = time
        self.exec_plugins()
        self.check_membership()
        self.exec_mappings()
        self.trigger_periodic_processes(time)

    def get_time():
        pass

    def init(self):
        pass

    def exec_plugins():
        # add, remove components
        for plugin in self.plugins:
            plugin.run(self)
        pass

    def exec_mappings(self):
        pass

    def check_membership(self):
        pass

    def trigger_periodic_processes(self, time):
        # mappings
        pass

    def shutdown(self):
        pass

class Manager:
    def 


    def exec(self, time):


class MembershipManager(Manager):
    def 


class ExternalClockDecoratorEngine(Engine):\

    """ Decorate a Engine with an external clock. 
        So we can sync the execution with and external clock.
        The clock in a generation function """

    def __init__(self, engine, clock):
        self.engine = engine
        self.clock = clock
        if engine.end_time != None:
            # todo alert not supported end_time
            pass


     def run(self):
        for time in clock():
            exec(time)