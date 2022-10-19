from four_in_a_row import Game
from fiar_min_max import FIARMinMax


def test_win_when_possible():
	# make sure algo wins when it has the opportunity to
	initial = [
		list('.......'),
		list('.......'),
		list('.......'),
		list('.......'),
		list('....#..'),
		list('###++.+'),
	]
	game = Game(initial_board=initial)
	fiar_mm = FIARMinMax(game, max_depth=5, plays=1)
	assert fiar_mm.get_best_play() == 5
	assert fiar_mm.last_play_options == [5]

	initial = [
		list('.......'),
		list('.......'),
		list('.......'),
		list('...+++.'),
		list('..#+#+.'),
		list('..#+###'),
	]
	game = Game(initial_board=initial)
	fiar_mm = FIARMinMax(game, max_depth=5, plays=1)
	assert fiar_mm.get_best_play() in (2, 3)
	assert fiar_mm.last_play_options == [2, 3]


def test_block_when_possible():
	# make sure algo blocks when player is going to win
	initial = [
		list('.......'),
		list('.......'),
		list('.......'),
		list('....+..'),
		list('....+..'),
		list('.###+#.'),
	]
	game = Game(initial_board=initial)
	fiar_mm = FIARMinMax(game, max_depth=5, plays=1)
	assert fiar_mm.get_best_play() == 4
	assert fiar_mm.last_play_options == [4]

	initial = [
		list('.......'),
		list('.......'),
		list('..+#...'),
		list('..++...'),
		list('..#+...'),
		list('.#+##+#'),
	]
	game = Game(initial_board=initial)
	fiar_mm = FIARMinMax(game, max_depth=5, plays=0)
	assert fiar_mm.get_best_play() == 4
	assert fiar_mm.last_play_options == [4]


def test_play_smart():
	# make sure algo plays in a spot where win is assured
	initial = [
		list('.......'),
		list('.......'),
		list('.......'),
		list('....++.'),
		list('..#+#+.'),
		list('..#+###'),
	]
	game = Game(initial_board=initial)
	fiar_mm = FIARMinMax(game, max_depth=5, plays=1)
	assert fiar_mm.get_best_play() == 3
	assert fiar_mm.last_play_options == [3]
