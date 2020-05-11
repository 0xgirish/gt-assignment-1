import logging
import numpy as np
import itertools
import inspect

def parse(testcase):
    """
    parse testcase folder for strategy profiles of the player and utility
    function

    testcase: testcase is path to the folder containing testcase metedata and utility.csv file
    return: (number_of_players, strategy_profile, utility_function)
    """

    with open(f'{testcase}/meta.txt', 'r') as metafile:
        while True:
            line = metafile.readline()
            if line[0] == '#':
                # its a comment continue
                continue
            # first non comment line of meta file contains number_of_players (n)
            number_of_players = int(line)
            break

        strategy_profile = list()
        # next n line contains strategy profile of ith player
        for line in metafile.readlines():
            if len(strategy_profile) == number_of_players:
                break
            # strategies of ith player are comma separeted strings
            if line[0] == '#':
                # lines starting with a # are comments
                continue
            strategies = (line[:-1]).replace(' ', '').split(',')
            if len(strategies) != 0:
                strategy_profile.append(strategies)

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
        utility profile for strategy vector sv is OneIndexed e.g. index starts
        from 1 not 0

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

    return number_of_players, strategy_profile, utility_function

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
    assert False, f'{inspect.stack()[2][3]} is not defined'

# vim: set path=./:
