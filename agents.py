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


class CentipedePlayer(object):
    """
    Class which implements the agents in centipede game.
    """

    def __init__(self, player_id, color, game_length, revision_length, mode='random'):
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
        self.color = color
        self.mode = mode
        self.strategy = np.random.randint(1 + int(self.game_length / 2)) + 1
        self.revision_length = revision_length

    def set_strategy(self):
        strategy = self.strategy
        return strategy

    def update_strategy(self, revision_length, population_2):
        revision = []
        for i in range(revision_length):
            games = []
            for j in range(1, 7):
                self.strategy = j
                player_2 = population_2.get_player()
                # if self.color == 'yellow':
                games.append(self.play_centipede_game(player_2)[0])
            games = np.array(games)
            revision.append(np.where(games == np.max(games))[0][0] + 1)
        self.strategy = max(set(revision), key=revision.count)

    def update_strategy2(self, revision_length, population_1):
        revision = []
        for i in range(revision_length):
            games = []
            for j in range(1, 7):
                self.strategy = j
                player_1 = population_1.get_player()
                # if self.color == 'yellow':
                games.append(player_1.play_centipede_game(self)[1])
            games = np.array(games)
            revision.append(np.where(games == np.max(games))[0][0] + 1)
        self.strategy = max(set(revision), key=revision.count)

    def play_centipede_game(self, player_2_instance):
        player_1 = self.strategy
        player_2 = player_2_instance.strategy
        if player_1 == 6 & player_2 == 6:
            return self.game_length, self.game_length
        elif player_1 <= player_2:
            return [player_1 * 2 - 2, player_1 * 2 - 2]
        else:
            return [player_2 * 2 - 3, player_2 * 2 + 1]


class CentipedePopulation(object):
    """
    Class which implements the populations of players.
    """

    def __init__(self, game_length, population_size, color, revision_length, mode='random'):
        """
        Parameters
        ----------
        game_length : int
            lattice side size
        population_size : int
            Size of the populations
        color : string
            Color of players
        revision_length : int
            Number of times the player will test his strategy
        mode : string
            Specifies how to looking for holes, randomly or nearby.
        """
        # Set internal parameters
        self.revision_length = revision_length
        self.game_length = game_length
        self.population_size = population_size
        self.color = color
        self.mode = mode
        self.initial_strategy = np.random.randint(self.game_length)
        self.population = self.populate_group()

    def populate_group(self):
        population = []
        for i in range(self.population_size):
            player = CentipedePlayer(i, self.color, self.game_length, self.revision_length, mode='random')
            population.append(player)
        return population

    def get_player(self):
        return np.random.choice(self.population)

    def get_strategy_distribution(self):
        strategies = [player.strategy for player in self.population]
        distribution = np.histogram(strategies, bins=[1, 2, 3, 4, 5, 6, 7])[0]
        plt.show()
        return distribution

    def review_strategy(self, population_other):
        if self.color == 'yellow':
            for player in self.population:
                player.update_strategy(self.revision_length, population_other)
        else:
            for player in self.population:
                player.update_strategy2(self.revision_length, population_other)


class CentipedeGame(object):
    """
    Class which implements the game.
    """

    def __init__(self, game_rounds, game_length, population_size, review_frequency, revision_length, mode='random'):
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
        self.game_rounds = game_rounds
        self.revision_length = revision_length
        self.game_length = game_length
        self.population_size = population_size
        self.review_frequency = review_frequency
        self.mode = mode
        # (self, game_length, population_size, color, revision_length, mode='random')
        self.population_yellow = CentipedePopulation(self.game_length,
                                                     self.population_size,
                                                     'yellow',
                                                     self.revision_length)
        self.population_blue = CentipedePopulation(self.game_length,
                                                   self.population_size,
                                                   'blue',
                                                   self.revision_length)

    def simulate_centipede_game(self):
        dist_payoffs = []
        # strategies_blue = []
        # strategies_yellow = []
        for g in range(1, self.game_rounds):
            index_1 = np.random.permutation(range(self.population_size))
            index_2 = np.random.permutation(range(self.population_size))
            if g % self.review_frequency == 0:
                # TODO: Review strategy needs to be modified alternating one player from each population.
                self.population_yellow.review_strategy(self.population_blue)
                self.population_blue.review_strategy(self.population_yellow)
                # strategies_yellow.append(self.population_yellow.get_strategy_distribution())
                # strategies_blue.append(self.population_blue.get_strategy_distribution())
            for p1, p2 in zip(index_1, index_2):
                payoffs = []
                payoff = self.population_yellow.population[p1].play_centipede_game(self.population_blue.population[p2])
                payoffs.append(np.mean(payoff))
            dist_payoffs.append(np.mean(payoffs))
        return dist_payoffs


def main():
    game_rounds = 100
    game_length = 10
    population_size = 1000
    review_frequency = 1
    revision_length = 1

    g = CentipedeGame(game_rounds, game_length, population_size, review_frequency, revision_length)
    g.simulate_centipede_game()


if __name__ == '__main__':
    main()
