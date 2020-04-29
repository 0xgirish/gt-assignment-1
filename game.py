import math
import copy
import itertools
import numpy as np
import logging

# domination types
dominant = np.maximum
dominated = np.minimum


class Game:
    """
    game class for basic funcationalties like, dominant strategies, iterative elimination
    A n-player game is represented by the tupple <N, S, U> where N is number of players
    S is strategies set for all the players, e.g. S[i] = strategies set for player i
    U is utility function Ui: <Si, S-i> -> R, U(strategies vector) gives a list
    utility of player i with strategy vector, ~s = Ui(~s) = U(~s)[i]
    """

    def __init__(self, n, s, u):
        self.n, self.s, self.u = n, s, u

    def _domination_strategy(self, i, dominates, domination_type):
        """
        _domination_strategy reports dominant strategy based on compare function, (dominates)
        big-O runtime O(π#Si) => O(#s1 * #s2 * #s3 ... #sn), where #si = number of strategies of ith player

        i: ith player
        dominates: comparision function, e.g np.all(si > sj) for strongly dominant strategy
        return: _domination_strategy for ith player
        """

        Si = self.s[i-1]  # strategy set of ith player

        _ds, _ds_util, exist = Si[0], self._utility_tensor(Si[0], i), True
        for k in range(1, len(Si)):
            si_util = self._utility_tensor(Si[k], i)
            if dominates(_ds_util, si_util):
                continue
            elif dominates(si_util, _ds_util):
                # strategy Si[k] is dominating strategy
                _ds, _ds_util, exist = Si[k], si_util, True
            else:
                _ds_util, exist = domination_type(_ds_util, si_util), False

        return _ds if exist else None

    def _dominant_strategy_equilibrium(self, func_dominant_strategy):
        """
        _dominant_strategy_equilibrium reports dominant strategy equilibrium based on func_dominant_strategy
        big-O runtime O(nπ#si) = O(n * #s1 * #s2 * #s3 ... #sn), where #si = number of strategies of ith player
        """

        _dse_profile = list()
        for i in range(1, self.n+1):
            _ds_for_ith_player = func_dominant_strategy(i)

            # if dominant strategy does not exist for ith player then
            # _dse does not exist
            if _ds_for_ith_player is None:
                return None
            _dse_profile.append(_ds_for_ith_player)

        return _dse_profile

    def strongly_dominant_strategy(self, i):
        """
        find strongly dominant strategy for ith player

        i: ith player
        return: strongly_dominant_strategy for ith player
        """

        sdse_profile = self._domination_strategy(i, lambda si, sj: np.all(si > sj), domination_type=dominant)
        if sdse_profile is None:
            logging.info('SDSE equilibria dose not exist')
        return sdse_profile

    def weakly_dominant_strategy(self, i):
        """
        find weakly dominant strategy for ith player

        i: ith player
        return: weakly_dominant_strategy for ith player
        """

        wdse_profile = self._domination_strategy(i, lambda si, sj: np.all(si >= sj) and np.any(si > sj),
                                                 domination_type=dominant)
        if wdse_profile is None:
            logging.info('WDSE equilibria dose not exist')
        return wdse_profile

    def sdse(self):
        """find strongly dominant strategy equilibrium if exist"""

        return self._dominant_strategy_equilibrium(self.strongly_dominant_strategy)

    def wdse(self):
        """find weakly dominant strategy equilibrium if exist"""

        return self._dominant_strategy_equilibrium(self.weakly_dominant_strategy)

    def _max_util_strategy_vector(self, i):
        """
        find strategy vector for which ith players get maximum utility if he/she plays si strategy

        i: ith player
        return: strategy vector(s) (si, s-i) for which ith player gets maximum utility, with fixed s-i
        """

        sv_set = set()  # strategy vector set which gives maximum utility for ith player
        comb = self.s[:i-1] + self.s[i:]
        for _sv in itertools.product(*comb):
            Si = self.s[i-1]
            max_utility = -math.inf
            _sv_set = set()
            for si in Si:
                sv = _sv[:i-1] + tuple(si) + _sv[i-1:]
                sith_utility = self.u(sv)[i-1]
                if max_utility < sith_utility:
                    _sv_set.clear()
                    _sv_set.add(sv)
                    max_utility = sith_utility
                elif max_utility == sith_utility:
                    _sv_set.add(sv)

            sv_set = sv_set.union(_sv_set)

        return sv_set

    def psne(self):
        """find Pure Strategy Nash Equilibrium if it exist"""

        nash_eqilibrium = self._all_strategy_vectors()  # nash equilibrium strategy vectors set
        for i in range(1, self.n+1):
            ith_set = self._max_util_strategy_vector(i)

            nash_eqilibrium = nash_eqilibrium.intersection(ith_set)
            logging.info(f'for {i} player {ith_set}')

        if len(nash_eqilibrium) == 0:
            logging.info('Pure Strategy Nash Equilibrium does not exist')
            return None

        return nash_eqilibrium

    def msne(self):
        """find Mix Strategy Nash Equilibrium for 2 player game"""

        if self.n > 2:
            logging.info(f'Calculating MSNE for {self.n} player game is out of question scope')
            return

        # TODO: find two player MSNE using linear programming

    def maxmin(self, i):
        """find maxmin value and maxmin strategies of ith player"""

        maxmin_strategy_set, maxmin_utility = set(), -math.inf
        for si in self.s[i-1]:
            utility_vector = self._utility_tensor(si, i)
            min_utility = min(utility_vector)
            if maxmin_utility < min_utility:
                maxmin_utility = min_utility
                maxmin_strategy_set.clear()
                maxmin_strategy_set.add(si)
            elif maxmin_utility == min_utility:
                maxmin_strategy_set.add(si)

        return maxmin_utility, maxmin_strategy_set

    def minmax(self, i):
        """find minmax value and minmax strategies ith player"""

        minmax_strategy_set, minmax_utility = set(), math.inf
        for si in self.s[i-1]:
            utility_vector = self._utility_tensor(si, i)
            max_utility = max(utility_vector)
            if minmax_utility > max_utility:
                minmax_utility = max_utility
                minmax_strategy_set.clear()
                minmax_strategy_set.add(si)
            elif minmax_utility == max_utility:
                minmax_strategy_set.add(si)

        return minmax_utility, minmax_strategy_set

    def iterative_elimination(self):
        """iterative elimination of a game gives a new subgame with weakly dominated strategies removed"""

        # FIXME: clean the utility function of new game
        # by removing all the strategy vectors mappings containing removed strategy (wds)
        for i in range(1, self.n+1):
            if len(self.s[i-1]) == 1:
                continue
            wds = self._domination_strategy(i, lambda x, y: np.all(x <= y) and np.any(x < y), domination_type=dominated)
            if wds is not None:
                s = copy.deepcopy(self.s)
                s[i].remove(wds)
                return Game(self, self.n, s, self.u).iterative_elimination()

        # no wds found for any player, return original game
        return Game(self, self.n, self.s, self.u)

    def _all_strategy_vectors(self):
        """find all strategy vectors"""

        s = set()
        for sv in itertools.product(*self.s):
            s.add(sv)
        return s

    def _utility_tensor(self, si, i):
        """find all the utilities ith player can get if he/she plays si strategy"""

        comb = [[si] if j == i else self.s[j-1] for j in range(1, self.n+1)]

        utility_si = list()
        # (si, s-i) ∀ s-i ∈ S-i
        for sv in itertools.product(*comb):
            utility_si.append(self.u(sv)[i-1])

        return np.array(utility_si)

# vim: set path=./:
