from copy import deepcopy
from typing import List
from collections.abc import MutableMapping

class TrialDesign(dict):
    ''''
    Dict of factor:level with two fields
    id: a code of levels selected
    factors_map: a map with the levels selected
    '''
    def __init__(self):
        self.__id = None
        self.factors_map = {}

    def add_factor(self, factor, level, level_code):
        self[factor] = level
        self.factors_map[factor] = level_code
    
    def get_id(self):
        if self.__id == None:
            code = ''
            for _, level_code in self.factors_map:
                code += level_code
            self.__id = code
        return self.__id

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
    # starting with a empty 'seed_trial' that is further 'forked'
    # with possible levels of factors
    factors = flatten(factors)
    seed_trial = TrialDesign()

    all_combinations = [seed_trial]
    
    for factor, levels in factors.items():
        # for each factor, recombine the combinations up to now
        # with each level of the here selected factor
        last_combination = all_combinations
        all_combinations = []
        for trial in last_combination:
            level_code = 'A'
            for level in levels:
                
                new_trial = deepcopy(trial)
                new_trial.add_factor(factor, level, level_code)
                all_combinations.append(new_trial)
                level_code = chr(ord(level_code) + 1) # increment code
                
    return all_combinations
        

def draw_without_repetition(source: List, number_of_draw:int, rand):
    drawn = rand.choice(source)
    if number_of_draw > 1:
        new_source = [ element for element in  source if element is not drawn ]
        return [drawn] + draw_without_repetition(new_source, number_of_draw - 1, rand)
    else:
        return [drawn]

def draw_with_repetition(source: List, number_of_draw:int, rand):
    drawn = rand.choice(source)
    if number_of_draw > 1:
        return [drawn] + draw_with_repetition(source, number_of_draw - 1, rand)
    else:
        return [drawn]