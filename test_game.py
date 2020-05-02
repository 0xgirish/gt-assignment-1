import logging

from game import Game
import util


def test_strong_dominant():
    """test strong dominant strategy and equilibrium"""
    
    # create game from testcase
    testcase = 'testdir/test.game/test.1'
    n, s, u = util.parse(testcase)
    game = Game(n, s, u)

    real_strong_strategies = ['a', 'p']
    strong_strategies = list()

    for i in range(1, n+1):
        strong_strategies.append(game.strongly_dominant_strategy(i))

    assert real_strong_strategies == strong_strategies, 'strongly dominant strategy failed'

    real_sdse = ['a', 'p']
    sdse = game.sdse()

    assert real_sdse == sdse, 'sdse failed'

def test_weak_dominant():
    """test weak dominant strategy and equilibrium"""
    
    testcase = 'testdir/test.game/test.2'
    n, s, u = util.parse(testcase)
    game = Game(n, s, u)

    real_weak_strategies = ['a', 'p']
    weak_strategies = list()

    for i in range(1, n+1):
        weak_strategies.append(game.weakly_dominant_strategy(i))

    assert real_weak_strategies == weak_strategies, 'weakly dominant strategy failed'

    real_wdse = ['a', 'p']
    wdse = game.wdse()

    assert real_wdse == wdse, 'wdse failed'

def test_psne():
    """test psne calculation"""

    testcases = ['testdir/test.game/test.1',
                 'testdir/test.game/test.2',
                 'testdir/test.game/test.3']

    real_psnes = [set([('a', 'p')]),
                  set([('a', 'p')]),
                  set([('a', 'p'), ('b', 'q'), ('c', 'r')])]

    for testcase, real_psne in zip(testcases, real_psnes):
        n, s, u = util.parse(testcase)
        game = Game(n, s, u)

        psne = game.psne()

        logging.info(f'psne = {psne}')
        assert real_psne == psne, 'psne failed'

def test_maxmin():
    """test maxmin value of a game"""
    
    testcase = 'testdir/test.game/test.2'
    n, s, u = util.parse(testcase)
    game = Game(n, s, u)

    maxmin_value = [2, 2]
    maxmin_strategy = [set(['a', 'b']), set(['p'])]

    for i in range(1, n+1):
        value, strategy = game.maxmin(i)
        
        assert maxmin_value[i-1] == value, 'maxmin value failed'
        assert maxmin_strategy[i-1] == strategy, 'maxmin strategy failed'


def test_minmax():
    """test minmax value of a game"""
    
    testcase = 'testdir/test.game/test.1'
    n, s, u = util.parse(testcase)
    game = Game(n, s, u)

    minmax_value = [1, 2]
    minmax_strategy = [set(['c']), set(['q', 'r'])]

    for i in range(1, n+1):
        value, strategy = game.minmax(i)
        
        assert minmax_value[i-1] == value, 'minmax value failed'
        assert minmax_strategy[i-1] == strategy, 'minmax strategy failed'

# vim: set path=./:
