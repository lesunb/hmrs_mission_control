
from mission_control.data_model.core import POI

from evaluation.experiment_gen_base.trial_design import draw_without_repetition, total_combinations

from random import Random

def test_total_combinations():
    random = Random()
    random.seed(1)
    number_of_robots = 1
    draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots, random),
    robot_factors =  [
        ('battery_charge', [
            draw_without_repetition([x for x in range(10, 90)], number_of_robots, random),
            draw_without_repetition([x for x in range(10, 90)], number_of_robots, random)]),
        ('battery_rate', [
            draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots, random),
            draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots, random)]),
        ('initial_position', [[ POI('a')], [POI('b')]]),
        ('skills', [['a'], ['b']])
    ]

    trials, code_map = total_combinations(robot_factors)
    assert len(trials) == 16
    assert code_map[0]['factor'] == 'battery_charge'
    assert code_map[0]['a']
    assert code_map[0]['b']


def test_draw_without_repetition():
    random = Random(1)
    all = ['a', 'b', 'c']
    result = draw_without_repetition(all, 3, random)
    assert not set(all) - set(result)