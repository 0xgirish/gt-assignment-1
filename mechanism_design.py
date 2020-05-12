import itertools
import copy
import logging
import util
import numpy as np
from social_function import EncodedList

class Environment:
    """
    Environment represents the environment settings in a mechanism design

    Attributes:
        n: number of players
        type_sets: represents type set of all the players
        types: represents the real types of the players
        outcomes: represents the outcome set of the environment
        utility_func: u(x, theta) -> is ordered list of all the utilities of the players

    Methods:
        dsic, export, dictatorial
    """

    def __init__(self, n, type_sets, outcomes, utility_func):
        self.outcomes, self.u = outcomes, utility_func
        self.n, self.type_sets = n, type_sets

        self.thetas = list()
        for _theta in itertools.product(*type_sets):
            self.thetas.append(list(_theta))

    def _is_dsic(self, player, func):
        """
        _is_dsic reports whether player will report its true type
        for given social choice function, func

        player: player to check
        func: SocialChoiceFunc
        """

        for theta_hat in self.thetas:
            for type in self.type_sets[player]:
                true_theta = copy.deepcopy(theta_hat)
                true_theta[player] = type

                fhat = func(EncodedList(theta_hat))
                ftrue = func(EncodedList(true_theta))

                ui_fhat = func(EncodedList([fhat, *true_theta]))[player]
                ui_ftrue = func(EncodedList([ftrue, *true_theta]))[player]

                if ui_fhat > ui_ftrue:
                    return False

        return True

    def dsic(self, func):
        """
        dsic reports whether the given function is DSIC or not

        func: SocialChoiceFunc
        """

        for player in range(0, self.n):
            if not self._is_dsic(player, func):
                return False

        return True

    def expost(self, func):
        """
        expost reports whether the given function is expost efficient

        func: SocialChoiceFunc
        """

        for theta in self.thetas:
            ftheta = func(EncodedList(theta))
            sum_ftheta = sum(self.u(EncodedList([ftheta, *theta])))
            for x in self.outcomes:
                sum_xtheta = sum(self.u(EncodedList([x, *theta])))
                if sum_xtheta > sum_ftheta:
                    return False

        return True

    def dictatorial(self, func):
        """
        dictatorial reports whether the given function is dictatorial

        func: SocialChoiceFunc
        """

        for theta in self.thetas:
            ftheta = func(EncodedList(theta))
            u_ftheta = np.array(self.u(EncodedList([ftheta, *theta])))
            compare = np.array([True for _ in range(self.n)])
            for x in self.outcomes:
                u_xtheta = np.array(self.u(EncodedList([x, *theta])))
                compare = compare & (u_ftheta >= u_xtheta)

            if np.any(compare):
                return True

        return False

# vim: set path=./:
