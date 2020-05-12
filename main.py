import argparse
import util

from game import Game
from two import TwoPlayer, TwoPlayerZeroSum
from social_function import SocialChoiceFunc, EncodedList
from mechanism_design import Environment

def q1(testcase):
    n, s, u = util.parse(testcase)
    game = Game(n, s, u)

    print('\n---------------- strong dominant strategies ----------------')
    for i in range(1, n+1):
        sds_i = game.strongly_dominant_strategy(i)
        print(f'player {i}: sds = {sds_i}')

    print('\n----------------- weak dominant strategies -----------------')
    for i in range(1, n+1):
        wds_i = game.weakly_dominant_strategy(i)
        print(f'player {i}: wds = {wds_i}')


    print('\n----------- strong dominant strategy equilibrium -----------')
    print(f'sdse: {game.sdse()}')


    print('\n------------ weak dominant strategy equilibrium ------------')
    print(f'wdse: {game.wdse()}')


    print('\n-------------- pure strategy nash equilibrium --------------')
    psne = game.psne()
    if psne is None:
        psne = 'does not exist'
    print(f'psne: {psne}')


    print('\n-------------------------- maxmin --------------------------')
    for i in range(1, n+1):
        value, strategy_set = game.maxmin(i)
        print(f'player {i}: value = {value}, strategies = {strategy_set}')


    print('\n-------------------------- minmax --------------------------')
    for i in range(1, n+1):
        value, strategy_set = game.minmax(i)
        print(f'player {i}: value = {value}, strategies = {strategy_set}')


    
def q2(testcase):
    n, s, u = util.parse(testcase)
    game = TwoPlayer(n, s, u)
    msne = game.msne()

    if msne is None:
        msne = 'not able to find'

    print(f'\nmsne: (P1, P2) = {msne}\n')
    
def q3(testcase):
    n, s, u = util.parse(testcase)
    game = TwoPlayerZeroSum(n, s, u)
    saddle_point = game.saddle_point()
    msne = game.msne()

    if saddle_point is None:
        saddle_point = 'does not exist'

    if msne is None:
        msne = 'not able to find'

    print(f'\nsaddle point: {saddle_point}')
    print(f'msne: (P1, P2) =  {msne}\n')

def q4(testcase):
    n, type_sets, outcomes, u = util.parse_md(testcase)
    env = Environment(n, type_sets, outcomes, u)

    # for all possible social choice functions check dsic, export and non-dictatorial
    for func in SocialChoiceFunc.all(type_sets, outcomes):
        valid = env.dsic(func) and env.expost(func) and (not env.dictatorial(func))
        if valid:
            print(func)
    
if __name__ == '__main__':
    description = """
        game theory assignment solve questions for corresponding testcases
        ----------------------------------------------------------------------------
        e.g. pyhton main.py --q 1 2 --testcase input/test.a input/test.b
        ----------------------------------------------------------------------------
        in the above example solver will solve question 1 for testcase input/test.a
        and question 2 for testcase input/test.b """

    # parse arguments from command line
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--q', type=int, nargs='+', help='question to solve e.g. --q 1 2 3 4')
    parser.add_argument('--testcase', type=str, nargs='+', help='directories for the testcases')

    args = parser.parse_args()

	# check if all questions has corresponding testcase, e.g. len(args.q) == len(args.testcase)
    assert len(args.q) == len(args.testcase), 'number of testcases should be same as number of questions'

    solver = {1: q1, 2: q2, 3: q3, 4: q4}
    for i in range(len(args.q)):
        question, testcase = args.q[i], args.testcase[i]
        solve = solver.get(question, lambda _: parser.print_help())

    	# solve question for testcase
        print(f'\n\033[1m\033[1;32m=================== solving question {question} =====================')
        print(f'\033[1;31mtestcase: {testcase}\033[0m')
        solve(testcase)

# vim: set path=./:
