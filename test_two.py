import logging
import util
import numpy as np
from two import TwoPlayer, TwoPlayerZeroSum

def equal(src, target):
    return abs(src - target) < 0.000001

def test_non_zero_sum():
    testcase = 'testdir/test.msne/test.1'
    n, s, u = util.parse(testcase)
    game = TwoPlayer(n, s, u)
    game = game.iterative_elimination()
    result = game.msne()

    # if linear program is not able to find the MSNE then fail
    assert result is not None, 'Non zero sum game MSNE failed'

    result_1, result_2 = result
    logging.info(f'[iterative elimination] S1 = {game.s[0]},  S2 = {game.s[1]}')
    logging.info(f'Results P1: {result_1} P2: {result_2}')

    condition = equal(result_1[0], 3/5) and equal(result_1[1], 0) and equal(result_1[2], 2/5)
    condition = condition and equal(result_2[0], 5/8) and equal(result_2[1], 3/8)
    condition = condition and equal(result_2[2], 0)
    assert condition, 'Non zero sum game MSNE failed'

def test_zero_sum():
    testcase = 'testdir/test.msne/test.0'
    n, s, u = util.parse(testcase)
    game = TwoPlayerZeroSum(n, s, u)
    game = game.iterative_elimination()
    result = game.msne()

    # if linear program is not able to find the MSNE then fail
    assert result is not None, 'Non zero sum game MSNE failed'

    result_1, result_2 = result
    logging.info(f'[iterative elimination] S1 = {game.s[0]},  S2 = {game.s[1]}')
    logging.info(f'Results P1: {result_1} P2: {result_2}')

    condition = equal(result_1[0], result_1[1]) and equal(result_1[1], result_1[2])
    condition = condition and equal(result_2[0], result_2[1]) and equal(result_2[1], result_2[2])
    assert condition, 'Non zero sum game MSNE failed'
