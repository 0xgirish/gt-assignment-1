import logging
import itertools
import numpy as np
import math

# game class for basic funcationalties like, dominant strategies, iterative elimination
class Game:
    # a n-player game is represented by the tupple <N, S, U>
    # where N is number of players
    # S is strategies set for all the players, e.g. S[i] = strategies set for player i
    # U is utility function Ui: <Si, S-i> -> R, U(strategies vector) gives a list
    # utility of player i with strategy vector, ~s = Ui(~s) = U(~s)[i]
    def __init__(self, n, s, u):
        self.n, self.s, self.u = n, s, u

    # _dominant_strategy reports dominant strategy based on compare function, (dominates)
    # big-O runtime O(π#Si) => O(#s1 * #s2 * #s3 ... #sn), where #si = number of strategies of ith player
    def _dominant_strategy(self, i, dominates):
        """
        i: ith player
        dominates: comparision function, e.g np.all(si > sj) for strongly dominant strategy
        return: _dominant_strategy for ith player
        """
        Si = self.s[i] # strategy set of ith player

        sds, sds_util, exist = Si[1], self._utility_tensor(Si[1], i), true
        for k in range(2, len(Si)+1):
            si_util = self._utility_tensor(Si[k], i)
            if dominates(sds_util, si_util):
                continue
            elif dominates(si_util, sds_util):
                # strategy Si[k] is dominating strategy sds
                sds, sds_util, exist = Si[k], si_util, true
            else:
                sds_util, exist = np.maximum(sds_util, si_util), false

        return sds if exist else None

    # _dominant_strategy_equilibrium reports dominant strategy equilibrium based on func_dominant_strategy
    # big-O runtime O(nπ#si) = O(n * #s1 * #s2 * #s3 ... #sn), where #si = number of strategies of ith player
    def _dominant_strategy_equilibrium(func_dominant_strategy):
        _dse_profile = list()
        for i in range(1 , self.n+1):
            _ds_for_ith_player = func_dominant_strategy(i)

            # if dominant strategy does not exist for ith player then
            # _dse does not exist
            if _ds_for_ith_player is None:
                logging.info(f'{equilibira_type} equilibrium does not exist')
                return None
            _dse_profile.append(_ds_for_ith_player)

        return _dse_profile

    # find strongly dominant strategy for ith player
    def strongly_dominant_strategy(self, i):
        """
        i: ith player
        return: strongly_dominant_strategy for ith player
        """
        return self._dominant_strategy(i, lambda si, sj: np.all(si > sj))

    # find weakly dominant strategy for ith player
    def weakly_dominant_strategy(self, i):
        """
        i: ith player
        return: weakly_dominant_strategy for ith player
        """
        return self._dominant_strategy(i, lambda si, sj: np.all(si >= sj) and np.any(si > sj))


    # find strongly dominant strategy equilibrium if exist
    def sdse(self):
        return self._dominant_strategy_equilibrium(self.strongly_dominant_strategy)

    # find weakly dominant strategy equilibrium if exist
    def wdse(self):
        return self._dominant_strategy_equilibrium(self.weakly_dominant_strategy)


    # find strategy vector for which ith players get maximum utility if he/she plays si strategy
    def _max_util_strategy_vector(self, si, i):
        """
        si: strategy played by ith player
        i: ith player
        return: strategy vector(s) (si, s-i) for which ith player gets maximum utility
        """
        sv_set = set() # strategy vector set which gives maximum utility for ith player
        comb = [[si] if j == i else self.s[j] for j in range(1, self.n+1)]

        max_utility = -math.inf
        for sv in itertools.product(*comb):
            ith_sv_utility = self.u(sv)[i]
            if max_utility < ith_sv_utility:
                sv_set.clear()
                sv_set.add(sv)
            elif max_utility == ith_sv_utility:
                sv_set.add(sv)

        return sv_set

    # find Pure Strategy Nash Equilibrium if it exist
    def psne(self):
        nash_eqilibrium = self._all_strategy_vectors() # nash equilibrium strate vectors set
        for i in range(1, self.n+1):
            ith_set = set()
            for si in self.s[i]:
                ith_set.union(self._max_util_strategy_vector(si, i))

            nash_eqilibrium.intersection(ith_set)

        if len(a):
            log.info('Pure Strategy Nash Equilibrium does not exist')
            return None

        return nash_eqilibrium

    # find maxmin value and maxmin strategies of ith player
    def maxmin(self, i):
        maxmin_strategy_set, maxmin_utility = set(), -math.inf
        for si in self.s[i]:
            utility_vector = self._utility_tensor(si, i)
            min_utility = min(utility_vector)
            if maxmin_utility < min_utility:
                maxmin_utility = min_utility
                maxmin_strategy_set.clear()
                maxmin_strategy_set.add(si)
            elif maxmin_utility == min_utility:
                maxmin_strategy_set.add(si)

        return maxmin_utility, maxmin_strategy_set

    # find minmax value and minmax strategies ith player
    def minmax(self, i):
        minmax_strategy_set, minmax_utility = set(), math.inf
        for si in self.s[i]:
            utility_vector = self._utility_tensor(si, i)
            max_utility = max(utility_vector)
            if minmax_utility > max_utility:
                minmax_utility = max_utility
                minmax_strategy_set.clear()
                minmax_strategy_set.add(si)
            elif minmax_utility == max_utility:
                minmax_strategy_set.add(si)

        return minmax_utility, minmax_strategy_set

    # find all strategy vectors
    def _all_strategy_vectors(self):
        s = set()
        for sv in itertools.product(*self.s):
            s.add(sv)
        return s

    # find all the utilities ith player can get if he/she plays si strategy
    def _utility_tensor(si, i):
        comb = [[si] if j == i else self.s[j] for j in range(1, self.n+1)]

        utility_si = list()
        # (si, s-i) ∀ s-i ∈ S-i
        for sv in itertools.product(*comb):
            utility_si.append(self.u(sv)[i])

        return np.array(utility_si)
