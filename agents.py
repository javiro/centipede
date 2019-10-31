import numpy as np
import matplotlib.pyplot as plt


def plot_states(sli, sl):
    axes_initial = plt.subplot(211)
    plt.imshow(sli)
    axes_end = plt.subplot(212)
    plt.imshow(sl)
    axes_initial.set_ylabel('Initial')
    axes_end.set_ylabel('End')
    plt.show()


class CentipedePlayers(object):
    """
    Class which implements the agents in centipede game.
    """

    def __init__(self, player_id, color, game_length, mode='random'):
        """
        Parameters
        ----------
        player_id : int
            player id
        color : string
            Player's color
        game_length : int
            lattice side size
        mode : string
            Specifies how to looking for holes, randomly or nearby.
        """
        # Set internal parameters
        self.player_id = player_id
        self.game_length = game_length
        self.mode = mode
        self.strategy = np.random.randint(self.game_length)

    def compute_payoff(self, i, j, sl, value):
        """
        Returns the utility value.
        :param i: int, file index
        :param j: int, column index
        :param L: int, length of lattice side
        :param sl: matrix_like, Schelling lattice
        :param value: float, values 1 or -1
        :return: int, 1 or 0
        """
        sl_pad = np.pad(sl, (1, 1), 'wrap')
        moore_nb = sl_pad[i:i + 3, j:j + 3]
        masc = np.ones((3, 3))
        masc[1, 1] = 0.0
        moore_nb = np.multiply(moore_nb, masc)
        s = np.abs(np.sum(moore_nb[np.where(moore_nb == value)])) / np.sum(np.abs(moore_nb)) - self.T
        return np.heaviside(s, 1)

    def set_strategy(self):
        strategy = self.strategy
        return strategy

    def update_strategy(self, revision_length, population_2):
        revision = []
        for i in range(revision_length):
            games = []
            for j in range(1, 7):
                player_2 = population_2.get_player()
                games.append(self.play_centipede_game(player_2))
            games = np.array(games)
            revision.append(np.where(games == np.max(games))[0][0] + 1)
        return max(set(revision), key=revision.count)

    def play_centipede_game(self, player_2):
        player_1 = self.strategy
        if player_1 == 6 & player_2 == 6:
            return self.game_length, self.game_length
        elif player_1 <= player_2:
            return player_1 * 2 - 2, player_1 * 2 - 2
        else:
            return player_2 * 2 - 3, player_2 * 2 + 1


class CentipedeGame(object):
    """
    Class which implements the game.
    """

    def __init__(self, game_length, population_size, mode='random'):
        """
        Parameters
        ----------
        game_length : int
            lattice side size
        population_size : int
            Size of the populations
        mode : string
            Specifies how to looking for holes, randomly or nearby.
        """
        # Set internal parameters
        self.game_length = game_length
        self.population_size = population_size
        self.mode = mode
        self.initial_strategy = np.random.randint(self.game_length)

    def simulate_centipede_game(self, player_1, player_2):
        if player_1 == 6 & player_2 == 6:
            return self.game_length, self.game_length
        elif player_1 <= player_2:
            return player_1 * 2 - 2, player_1 * 2 - 2
        else:
            return player_2 * 2 - 3, player_2 * 2 + 1
