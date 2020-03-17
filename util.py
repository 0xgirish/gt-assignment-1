import pandas as pd
import numpy as np

def parse(testcase):
    """
    testcase: testcase is path to the folder containing testcase metedata and utility.csv file
    return: (number_of_players, strategy_profile, utility_function)
    """

    with open(f'{testcase}/meta.txt', 'r') as metafile:
        # first line of meta file contains number of players
        number_of_players = int(metafile.readline())
        strategy_profile = list()
        # next n line contains strategy profile of ith player
        for line in metafile.readlines():
            # strategies of ith player are comma separeted strings
            strategies = (line[:-1]).replace(' ', '').split(',')
            if len(strategies) != 0:
                strategy_profile.append(strategies)

    utilities = pd.read_csv(f'{testcase/utility.csv}')

    def utility_function(sv):
        """
        sv: strategy vector
        return: utilities of all the players, e.g. list of utilities
        """

        # TODO: extract utlities from csv file and create utlity function
        pass

    return number_of_players, strategy_profile, utility_functio
