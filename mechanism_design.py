import itertools
import logging
import util

class Environment:
    """
    Environment represents the environment settings in a mechanism design

    Attributes:
        n: number of players
        type_sets: represents type set of all the players
        types: represents the real types of the players
        outcomes: represents the outcome set of the environment

    Methods:
        dsic, export, dictatorial
    """

    def __init__(self, n, type_sets, types, outcomes):
        self.n, self.outcomes = n, outcomes
        self.type_sets, self.types = type_sets, types

    def dsic(self, func):
        """
        dsic reports whether the given function is DSIC or not

        func: SocialChoiceFunc
        """

        #TODO: implement method
        util.undefined()

    def expost(self, func):
        """
        expost reports whether the given function is expost efficient

        func: SocialChoiceFunc
        """

        #TODO: implement method
        util.undefined()

    def dictatorial(self, func):
        """
        dictatorial reports whether the given function is dictatorial

        func: SocialChoiceFunc
        """

        #TODO: implement method
        util.undefined()
