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

        self.U1 = np.array(utility_matrix1)
        self.U2 = np.array(utility_matrix2)

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

        # TODO: implement linear programming for zero sum game
        # Compute: Zp := max z
        # Subject to: sum { x(si)u(si, sii) ∀ sii ∈ SII } ≥ z
        #             sum { x(si) } = 1; x(si) ≥ 0 ∀ si ∈ SI
        pass
