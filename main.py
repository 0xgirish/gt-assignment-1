import argparse
import util

from game import Game
from two import TwoPlayer, TwoPlayerZeroSum
from social_function import SocialChoiceFunc, EncodedList
from mechanism_design import Environment

def q1(testcase):
    # TODO: implement function
    util.undefined()

def q2(testcase):
    # TODO: implement function
    util.undefined()

def q3(testcase):
    # TODO: implement function
    util.undefined()

def q4(testcase):
    # TODO: implement function
    util.undefined()

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
        solve(testcase)

# vim: set path=./:
