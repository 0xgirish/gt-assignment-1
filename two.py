import itertools
import logging
import numpy as np
from scipy.optimize import linprog
from game import Game
import util

zero_p = 0.0000000000000001
one_m = 1

class TwoPlayer(Game):
    """
    TwoPlayer game class extend Game class for two player game

    attribute:
        self.n == 2, represents 2 player game
        self.s: strategy profile set of both players
        self.u: utility function
        self.U: utility matrix for both players

    methods:
        msne: find mixed straegy nash equilibrium for (n x m) game
    """

    def __init__(self, n, s, u):
        assert len(s) == 2, f'TwoPlayer game only accepts 2 player game, got {len(s)}'

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

    def iterative_elimination(self):
        game = self._iterative_elimination()
        return TwoPlayer(game.n, game.s, game.u)

    def msne(self):
        """find Mix Strategy Nash Equilibrium for 2 player game"""

        # linear programming for every support in the self
        for support1 in util.power_supports(self.s[0]):
            for support2 in util.power_supports(self.s[1]):
                # logging.info(f'MSNE calculation for supports: {support1}\n{support2}')
                result2 = self._lp_msne(support1, support2, 1)
                result1 = self._lp_msne(support2, support1, 2)
                if result1.success and result2.success:
                    mixed_strategy_1 = util.create_mixed_strategy(self.s[0], self.s[0], result1.x[1:])
                    mixed_strategy_2 = util.create_mixed_strategy(self.s[1], self.s[1], result2.x[1:])
                    return result1.x[1:], result2.x[1:]
                    return mixed_strategy_1, mixed_strategy_2

        logging.warning('not able to find msne for the self')

    def _lp_msne(self, self_support, opponent_support, player=1):
        """Find msne for self_support and opponent_support for player 1 and 2"""

        # logging.info(f'_lp_msne for player {player}')
        ns, U = len(self.s[player % 2]), self.U[player-1]
        if player != 1:
            U = U.T

        f, support_u = np.array([0.0 for _ in range(ns+1)]), U[np.where(self_support == 1)]

        a_temp = np.array([[0.] if i == 0 else [-1.] for i in range(support_u.shape[0]+1)])
        Aeq = np.concatenate([a_temp, np.concatenate([np.ones((1, support_u.shape[1])), support_u], axis=0)], axis=1)
        Beq = np.array([[1.] if i == 0 else [0.] for i in range(Aeq.shape[0])])
        # logging.info(f'Aeq: {Aeq}, {Aeq.shape}')
        # logging.info(f'Beq: {Beq}, {Beq.shape}')

        si_0 = np.where(self_support == 1)[0][0]
        not_support = U[np.where(self_support == 0)]
        # logging.info(f'not_support: {not_support}, {not_support.shape}')

        Aub = not_support - U[[si_0], :]
        Aub = np.concatenate([np.zeros((Aub.shape[0], 1)), Aub], axis=1)
        Bub = np.zeros((Aub.shape[0], 1))
        # logging.info(f'Aub: {Aub}, {Aub.shape}')
        # logging.info(f'Bub: {Bub}, {Bub.shape}')

        if not_support.shape[0] == 0 or not_support.shape[1] == 0:
            Aub, Bub = None, None

        p_bounds = np.array([(zero_p, one_m) for _ in range(ns)])
        p_bounds[np.where(opponent_support == 0)] = (0, 0)

        return linprog(f, A_ub=Aub, b_ub=Bub, A_eq=Aeq, b_eq=Beq, bounds=[(None, None), *p_bounds], method='simplex')


class TwoPlayerZeroSum(TwoPlayer):
    """
    TwoPlayerZeroSum game class extend TwoPlayer class for zero sum games

    attribute:
        self.n == 2, represents 2 player game
        self.s: strategy profile set of both players
        self.u: utility function
        self.U: utility matrix for both players

    methods:
        saddle_point: find the saddle point of the game if exist
        msne: find mixed strategy nash equilibrium for (n x m) game
    """

    def __init__(self, n, s, u):
        super().__init__(n, s, u)

        # check if utilities are according to zero sum game
        assert np.all(self.U[0] == -self.U[1]), 'provided game is not a zero sum game'

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

    def iterative_elimination(self):
        game = self._iterative_elimination()
        return TwoPlayerZeroSum(game.n, game.s, game.u)

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


    def _lp_msne(self, player):
        S, U = self.s[player-1], self.U[player-1]
        if player == 2:
            U = U.T

        # solve for player i
        f = np.array([1.0 if i == 0 else 0.0 for i in range(len(S)+1)])
        a_ub = np.concatenate([np.ones((len(S), 1)), -U], axis=1)
        b_ub = np.zeros(len(S))

        a_eq = np.array([[0 if i == 0 else 1.0 for i in range(len(S)+1)]])
        b_eq = np.array([[1.0]])

        r_bounds = (None, None)
        p_bounds = [(0, 1.0) for _ in S]

        return linprog(f, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=[r_bounds, *p_bounds])
