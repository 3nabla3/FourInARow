from four_in_a_row import Board
from min_max_tree import MinMaxTree


def test_analyse_line():
	assert MinMaxTree._analyze_line(list('.......'), 0) == 0
	assert MinMaxTree._analyze_line(list('....#..'), 0) == 1
	assert MinMaxTree._analyze_line(list('..##...'), 0) == 2
	assert MinMaxTree._analyze_line(list('..#+...'), 0) == 0
	assert MinMaxTree._analyze_line(list('.##.#..'), 0) == 3
	assert MinMaxTree._analyze_line(list('.##..#.'), 0) == 2
	assert MinMaxTree._analyze_line(list('.#.#.+.'), 0) == 2
	assert MinMaxTree._analyze_line(list('.#.#.#+'), 0) == 2


def test_score():
	state = [
		['.'] * 7,
		['.'] * 7,
		list("....+.."),
		list("...++#."),
		list("..###+."),
		list("+#+##+."),
	]
	mmt = MinMaxTree(Board(initial_state=state), 0)
	assert mmt._score(0) == 3
	assert mmt._score(1) == 2

	state = [
		['.'] * 7,
		['.'] * 7,
		list("....+.."),
		list("...++#."),
		list(".#.##+."),
		list("+#+##+."),
	]
	mmt = MinMaxTree(Board(initial_state=state), 0)
	assert mmt._score(0) == 3
	assert mmt._score(1) == 2

	state = [
		['.'] * 7,
		['.'] * 7,
		list("....+.."),
		list("...++#."),
		list(".#.#++."),
		list("+#+##+#"),
	]
	mmt = MinMaxTree(Board(initial_state=state), 0)
	assert mmt._score(0) == 2
	assert mmt._score(1) == 3
