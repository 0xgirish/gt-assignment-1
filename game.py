# game class for basic funcationalties like, dominant strategies, iterative elimination
class Game:
    # a n-player game is represented by the tupple <N, S, U>
    # where N is number of players
    # S is strategies set for all the players, e.g. S[i] = strategies set for player i
    # U is utility function Ui: <Si, S-i> -> R, U(strategies vector) gives a list
    # utility of player i with strategy vector, ~s = Ui(~s) = U(~s)[i]
    def __init__(self, n, s, u):
        self.n, self.s, self.u = n, s, u

    # return strongly_dominated_strategies for ith player
    def sds(self, i):
        """
        i: ith player
        return: strongly_dominated_strategies for ith player
        """
        # TODO: implement method
        pass

    # return weakly_dominated_strategies for ith player
    def wds(self, i):
        """
        i: ith player
        return: weakly_dominated_strategies for ith player:
        """
        # TODO: implement method
        pass

    # return all weakly_dominated_strategies and strongly_dominated_strategies for ith player
    def ds(self, i):
        sds, wds = self.sds(i), self.wds(i)
        return sds.extend(wds)

    # return maxmin value of ith player
    def maxmin(self, i):
        # TODO: implement method
        pass

    # return minmax value of ith player
    def minmax(self, i):
        # TODO: implement method
        pass

    # return subgame after elimination of strongly or weakly dominant staregies
    def iterative_elimination(self):
        # TODO: implement method
        pass
