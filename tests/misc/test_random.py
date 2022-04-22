from random import Random


def test_rand_consistency():
    random = Random()
    random.seed(42)

    x, y, z = random.choice(['a', 'b', 'c']), random.choice(['a', 'b', 'c']), random.choice(['a', 'b', 'c'])
    assert x == 'c'
    assert y == 'a'
    assert z == 'a'