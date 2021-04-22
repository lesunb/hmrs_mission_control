
from ensembles.engine import Engine


class ScheduledEffect:

    def __init__(self, events):
        self.


class ScheduledEffectPlugin:

    def __init__(self, events):
        # todo sort by due_time
        self.events = events


    def run(self, engine: Engine):
        triggerd_effects_count = 0
        for event in self.events:
            if event.due_time < self.engine.time:
                triggerd_effects_count  += 1
                event.effect(engine)
            else:
                break
        # todo splice the already triggered efects from  arr