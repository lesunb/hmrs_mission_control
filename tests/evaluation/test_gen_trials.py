
from mission_control.core import POI

from evaluation.framework.trial import draw_without_repetition, total_combinations

from random import Random

def test_total_combinations():
    robot_factors =  {
        'battery_level': range(0, 100, 50),
        'battery_rate': [0.05, 0.10],
        'initial_position': [ POI('a'), POI('b')],
        'skills': ['a']
    }

    trials = total_combinations(robot_factors)
    assert len(trials) == 8


def test_gen_trials_with_nest():
    robot_factors =  {
        'robots.[1]': {
            'battery_level': range(0, 100, 50),
            'battery_rate': [0.05, 0.10],
            'initial_position': [ POI('a'), POI('b')],
            'skills': [1, 2]
        },
        'robots.[2]': {
            'battery_level': range(0, 100, 50),
            'battery_rate': [0.05, 0.10],
            'initial_position': [ POI('a'), POI('b')],
            'skills': [1, 2]
        }

    }

    trials = total_combinations(robot_factors)
    assert len(trials) == 256

def test_draw_without_repetition():
    random = Random(1)
    all = ['a', 'b', 'c']
    result = draw_without_repetition(all, 3, random)
    assert not set(all) - set(result)