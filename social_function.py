import logging
import copy
import itertools


class EncodedList(list):
    """ EncodedList class provide encode method for mapping in dictonary """

    def encode(self):
        return ','.join(self.theta)


class SocialChoiceFunc:
    """
    SocialChoiceFunc class provide some functionalities for easier pretty print
    and represents mapping of Ѳ to outcome

    Attributes:
        id: unique id of the social choice function
        theta_s: List of EncodedList class
        mappings_s: mapping of outcomes to given theta_s

    Methods:
        f: f reports the outcome for a given Ѳ
    """
    def __init__(self, id, theta_s, mapping_s):
        size, self.func  = len(theta_s), dict()
        for i in range(size):
            theta, mapping = theta_s[i], mapping_s[i]
            self.func[theta.encode()] = mapping

    def f(self, theta):
        try:
            return self.func[theta.encode()]
        except KeyError:
            logging.error(f'Invalid Ѳ, no mapping available for {theta}')

    def __repr__(self):
        """ pretty print for SocialChoiceFunc  """

        repr = f'\nsocial choice function: #{self.id}\n'
        repr += '===================================='
        for theta in self.theta_s:
            repr += f'{theta} -> {self.func[theta.encode()]}\n'
        repr += '====================================\n'
        return repr

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def all(type_sets, outcomes):
        """
        all generates all possible social choice functions

        type_sets: type sets of all the players
        outcomes: outcome set for the environment
        """

        theta_s = list()  # all combinations of types of players
        for _theta in itertools.product(*type_sets):
            theta_s.append(EncodedList(list(_theta)))

		# all possbile outcome mappings for theta_s
        _comb_outcomes, id = [copy.deepcopy(outcomes) for _ in range(len(theta_s))], 0
        for mapping in itertools.product(*_comb_outcomes):
            id += 1
            yield SocialChoiceFunc(id, theta_s, mapping)

# vim: set path=./:
