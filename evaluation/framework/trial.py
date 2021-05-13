import random
from copy import copy
from typing import List
from collections.abc import MutableMapping

from mission_control.core import Request

class Trial:
    def __init__(self, id, robots, requests: List[Request]):
        self.id, self.robots, self.requests = id, robots, requests
        

class Factor:
    def __init__(self, property, levels):
        self.property, self.levels = property, levels

def flatten(d, parent_key='', sep='_'):
    ''' 
    Transform a nested dictionary into a flat one
    '''
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def total_combinations(factors):
    factors = flatten(factors)
    all_combinations = [{}]
    for factor, levels in factors.items():
        last_combination = all_combinations
        all_combinations = []
        for trial in last_combination:
            for level in levels:
                new_trial = copy(trial)
                new_trial[factor]= level
                all_combinations.append(new_trial)
    return all_combinations
        

def draw_without_repetition(source: List, number_of_draw:int, rand):
    drawn = [rand.choice(source)]
    if number_of_draw > 1:
        return drawn + draw_without_repetition(list(set(source) - set(drawn)), number_of_draw - 1, rand)
    else:
        return drawn

def draw_with_repetition(source: List, number_of_draw:int, rand):
    drawn = [rand.choice(source)]
    if number_of_draw > 1:
        return drawn + draw_with_repetition(source, number_of_draw - 1, rand)
    else:
        return drawn