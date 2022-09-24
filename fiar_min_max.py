from four_in_a_row import Game


class FIARMinMax:
	def __init__(self, game, *, plays=None):
		self.game = game
		self.plays = plays or Game.PLAYERS[1]

	def get_best_play(self):
		return next(self.game.get_valid_columns())
