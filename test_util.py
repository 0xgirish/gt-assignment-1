import itertools
from util import parse


def test_parse():
    testcase = 'testdir'
    n, s, u = parse(testcase)

    assert n == 2, f'{testcase} [n] got {n} expected 2'
    assert len(s) == 2, f'{testcase} [len(s)] got {len(s)} expected 2'

    res_s = [['0', '1'], ['0', '1']]
    assert s == res_s, f'{testcase} [strategy_profile] got {s}, expected {res_s}'

    strategy_vectors = [['0', '0'], ['0', '1'],
                        ['1', '0'], ['1', '1'], ['1', 'a']]
    results = [[-2, 2], [5, -5], [3, -3], [0, 0], None]

    for sv, res in zip(strategy_vectors, results):
        assert u(sv) == res, f'{testcase} [utility_function] failed'
