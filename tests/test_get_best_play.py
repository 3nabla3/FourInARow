from four_in_a_row import Game
from fiar_min_max import FIARMinMax


def test_get_best_play():
	initial = [
		list('.......'),
		list('.......'),
		list('.......'),
		list('.......'),
		list('....#..'),
		list('.##++.+'),
	]
	game = Game(initial_board=initial)
	fiar_mm = FIARMinMax(game, max_depth=5, plays=0)
	assert fiar_mm.get_best_play() == 5
