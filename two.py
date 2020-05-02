import itertools
import numpy as np
from scipy.optimize import linprog
from game import Game


class TwoPlayerZeroSum(Game):
    """
    TwoPlayerZeroSum game class extend Game class for zero sum games

    attribute:
        self.n == 2, represents 2 player game
        self.s: strategy profile set of both players
        self.u: utility function

    methods:
        saddle_point: find the saddle point of the game if exist
        msne: find mixed strategy nash equilibrium for (n x m) game
    """

    def __init__(self, n, s, u):
        assert n == 2, f'TwoPlayerZeroSum only accepts 2 player game, got {n}'

        self.n, self.s, self.u = n, s, u

        # create utility matrix (#s1 x #s2) for player 1 & 2
        utility_matrix1, utility_matrix2 = list(), list()
        for si in self.s[0]:
            comb = [[si], self.s[1]]
            utility1, utility2 = list(), list()

            for sv in itertools.product(*comb):
                utility = self.u(sv)
                utility1.append(utility[0])
                utility2.append(utility[1])

            utility_matrix1.append(utility1)
            utility_matrix2.append(utility2)

        self.U = [np.array(utility_matrix1), np.array(utility_matrix2)]

    def saddle_point(self):
        """
        Find saddle point of two player zero sum game if exist

        return: saddle point if exist else None
        """
        maxmin_of_player1 = self.maxmin(0)
        minmax_of_player2 = self.minmax(1)

        if maxmin_of_player1 == minmax_of_player2:
            return maxmin_of_player1
        return None

    def msne(self):
        """
        msne calculates Mixed Strategy Nash equilibrium for a (n x m)
        two player zero sum game.
        msne method uses linear programming to find the MSNE

        return: Mixed Strategy which is Nash Equilibrium
        """

        # for player 1
        res1 = self._lp_msne(1)
        res2 = self._lp_msne(2)

        p_res1, p_res2 = res1.x[1:], res2.x[1:]
        return p_res1, p_res2


    def _lp_msne(self, i):
        # solve for player i
        f = np.array([1.0 if i == 0 else 0.0 for i in range(len(self.s[i-1])+1)])
        a_ub = np.concatenate([np.ones((len(self.s[i-1]), 1)), -self.U[i-1]], axis=1)
        b_ub = np.zeros(len(self.s[i-1]))

        a_eq = np.array([0 if i == 0 else 1.0 for i in range(len(self.s[i-1])+1)])
        b_eq = np.array([1.0])

        r_bounds = (None, None)
        p_bounds = [(0, 1.0) for _ in self.s[i-1]]

        return linprog(f, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=[r_bounds, *p_bounds])
