import logging
import itertools
import inspect
import numpy as np
from social_function import EncodedList

def parse(testcase):
    """
    parse testcase folder for strategy profiles of the player and utility
    function

    testcase: testcase is path to the folder containing testcase metedata and utility.csv file
    return: (number_of_players, strategy_profiles, utility_function)
    """

    number_of_players, strategy_profiles = None, list()
    with open(f'{testcase}/meta.txt', 'r') as metafile:
        # all the lines starting with # are comments
        # first uncommented line contains number of players
        # next n uncommented lines contain strategy profiles
        while True:
            line = metafile.readline()
            if len(line) != 0 and line[0] == '#':
                # its a comment ignore
                continue

            if number_of_players is None:
                number_of_players = int(line)
                continue

            if len(strategy_profiles) < number_of_players:
                strategies = (line[:-1]).replace(' ', '').split(',')
                if len(strategies) != 0:
                    strategy_profiles.append(strategies)
                continue

            break

    utility_sv_mapping = dict()
    with open(f'{testcase}/utility.csv', 'r') as utilityfile:
        # first line contains index for strategy and utility, e.g. s1, s2, s3,
        # u1, u2, u3
        _ = utilityfile.readline()  # ignore this line

        # for all other lines form utility_strategy_vector_mapping
        for line in utilityfile.readlines():
            su_vector = (line[:-1]).replace(' ', '').split(',')
            # first n entries in su_vector forms a strategy_vector (sv)
            # next n entries forms utility vector for all n players
            sv, uv = su_vector[:number_of_players], su_vector[number_of_players:]

            sv_encoding = ','.join(sv)
            utility_sv_mapping[sv_encoding] = [float(u) for u in uv]

    def utility_function(sv):
        """
        utility lookup for strategy vector is O(1)

        sv: strategy vector
        return: utilities of all the players, e.g. list of utilities
        """

        assert len(sv) == number_of_players, f'strategy vector should have length equal to {number_of_players}'

        sv_encoding = ','.join(sv)
        try:
            return utility_sv_mapping[sv_encoding]
        except KeyError:
            logging.warning(f'KeyError: unexpected strategy vector, {sv} [encoding = {sv_encoding}]')

        return None

    return number_of_players, strategy_profiles, utility_function

def parse_md(testcase):
    """
    parse_md parse testcase for mechanism design environment

    testcase: path to testcase folder for Q4
    returns:
        number_of_players (n)
        type_sets (type set of each player)
        outcomes (outcome set)
        utility_func (theta to utility mapping)
    """

    number_of_players, type_sets, outcomes = None, list(), None
    with open(f'{testcase}/meta.txt') as metafile:
        # all the lines starting with # are comments in meta.txt file
        # first uncommented line contains number of players (n)
        # next n lines contain type set of all the players
        # last uncommented line contains outcome set
        while True:
            line = metafile.readline()
            if line[0] == '#':
                continue

            if number_of_players is None:
                number_of_players = int(line)
                continue

            if len(type_sets) < number_of_players:
                type_i = (line[:-1]).replace(' ', '').split(',')
                if len(type) != 0:
                    type_sets.append(type)
                continue

            if outcomes is None:
                _outcomes = (line[:-1]).replace(' ', '').split(',')
                if len(_outcomes) != 0:
                    outcomes = _outcomes

            break

    utility_mapping = dict()
    with open(f'{testcase}/utility.csv') as utilityfile:
        # first line contains the indexes of the csv file ignore it
        # next lines contains outcome, <theta>, <utility>
        _ = utilityfile.readline()

        for line in utilityfile.readlines():
            u_xtheta = (line[:-1]).replace(' ', '').split(',')
            xtheta, utility = u_xtheta[:number_of_players+1], u_xtheta[number_of_players+1:]
            utility, xtheta = [float(u) for u in utility], EncodedList(xtheta)
            utility_mapping[xtheta.encode()] = utility

    def utility_func(theta):
        """utility_func reports utility of the players for the types"""

        try:
            return utility_mapping[theta.encode()]
        except KeyError:
            logging.error(f'Invalid Ѳ, no mapping available for {theta}')

    return number_of_players, type_sets, outcomes, utility_func

def power_supports(strategy_profile):
    """
    power_supports return all possible supports for strategy_profile

    strategy_profile: index array which have been selected for support
    """

    n = len(strategy_profile)

    # it is more likely that support will have size near to strategy_profile size
    comb = np.array([[1, 0] for _ in range(n)])
    for support in itertools.product(*comb):
        np_support = np.array(support)
        if np.all(np_support == 0):
            continue
        yield np_support

def undefined():
    """assert that function is not defined"""
    logging.error(f'\tfunction {inspect.stack()[1][3]} is not defined')

# vim: set path=./:
