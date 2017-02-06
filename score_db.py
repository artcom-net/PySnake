"""ScoreDb class for PySnake game.

This class describes the various operations with a local database
that contains the results of the games.

"""


from operator import itemgetter
from shelve import DbfilenameShelf


__author__ = 'Artem Kustov'
__email__ = 'artem.kustov@artcom-net.ru'
__version__ = '1.0'


class ScoreDb(DbfilenameShelf):
    """Used Game class to store results of the players."""

    def __init__(self, db_path):
        """Initialize an instance.

        Argument db_path is an absolute path.
        The object of this class is controlled instance of the Game.

        """
        super().__init__(db_path)

    def add_score(self, player, score):
        """Adds the result to the db."""

        if player in self:
            current_score = self[player]
            self[player] = score if score > current_score else current_score
        else:
            self[player] = score

    def get_scores(self):
        """Returns a sorted list of tuples."""

        return self._sort_scores()

    def _sort_scores(self, count=10):
        """Sorts a list of tuples of two values:
        the player's name and number of score.

        """
        return sorted(
            sorted(self.items(), key=itemgetter(0), reverse=True),
            key=itemgetter(1))[::-1][:count]

    def get_top_score(self):
        """Returns the max score in the database."""

        return max(self.values()) if self.values() else 0

    def clear_db(self):
        """Clear the db."""

        for player in self:
            del self[player]
