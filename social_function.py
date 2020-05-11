import logging

class Theta:
    """
    Theta class provide some functionalities for easier mapping in a dict
    
    Attributes:
        theta: Ordered List of types of players
    Methods:
        encode
    """
    def __init__(self, theta):
        self.theta = theta

    def encode(self):
        """encoding of Ѳ for mapping purpose"""
        return ','.join(self.theta)

    def __repr__(self):
        return '{' + ' '.join(self.theta) + '}'

    def __str__(self):
        return self.__repr__()

class SocialChoiceFunc:
    """
    SocialChoiceFunc class provide some functionalities for easier pretty print
    and represents mapping of Ѳ to outcome

    Attributes:
        id: unique id of the social choice function
        theta_s: List of Theta class
        mappings_s: mapping of outcomes to given theta_s

    Methods:
        f: f reports the outcome for a given Ѳ
    """
    def __init__(self, id, theta_s, mapping_s):
        size = len(theta_s)
        for i in range(size):
            theta, mapping = theta_s[i], mapping_s[i]
            self.func[theta.encode()] = mapping

    def f(self, theta):
        try:
            return self.func[theta.encode()]
        except KeyError:
            logging.error(f'Invalid Ѳ, no mapping available for {theta}')

    def __repr__(self):
        repr = f'\nsocial choice function: #{self.id}\n'
        repr += '===================================='
        for theta in self.theta_s:
            repr += f'{theta} -> {self.func[theta.encode()]}\n'
        repr += '====================================\n'
        return repr

    def __str__(self):
        return self.__repr__()
