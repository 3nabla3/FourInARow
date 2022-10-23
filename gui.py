import pygame
from pygame.color import THECOLORS
from pygame.locals import *

from four_in_a_row import Game
from fiar_min_max import FIARMinMax

pygame.init()

W, H = 800, 600

NUM_ROW = 6
NUM_COL = 7

# leave a 5% margin on left and right
HORIZ_MARGIN = 0.05
MARGIN_WIDTH = W * HORIZ_MARGIN
GRID_WIDTH = W * (1 - HORIZ_MARGIN * 2)

# leave a 3% margin on top and bottom
VERT_MARGIN = 0.03
GRID_HEIGHT = H * (1 - VERT_MARGIN * 2)
MARGIN_HEIGHT = H * VERT_MARGIN

P0_COL = 'darkred'
P0_SPEC_COL = 'red'
P1_COL = 'darkblue'
P1_SPEC_COL = 'blue'


def draw_vert_line(screen, x, min_y, max_y):
	pygame.draw.line(screen, THECOLORS['turquoise'], (x, min_y), (x, max_y))


def draw_horiz_line(screen, y, min_x, max_x):
	pygame.draw.line(screen, THECOLORS['turquoise'], (min_x, y), (max_x, y))


def draw_grid(screen, n_rows, n_cols):
	for i in range(n_cols + 1):
		draw_vert_line(screen, MARGIN_WIDTH + (GRID_WIDTH / n_cols) * i, min_y=MARGIN_HEIGHT, max_y=H - MARGIN_HEIGHT)

	# the top of the board is open so the pieces can fall in
	for i in range(1, n_rows + 1):
		draw_horiz_line(screen, MARGIN_HEIGHT + (GRID_HEIGHT / n_rows) * i, min_x=MARGIN_WIDTH, max_x=W - MARGIN_WIDTH)


def draw_piece(screen, row, col, color):
	square_width = GRID_WIDTH / NUM_COL
	square_height = GRID_HEIGHT / NUM_ROW
	x = MARGIN_WIDTH + square_width * (col + 0.5)
	y = MARGIN_HEIGHT + square_height * (row + 0.5)

	pygame.draw.circle(screen, THECOLORS[color], (x, y), 20)


def top_of_col(board, coord, col) -> bool:
	"""Return true if the last piece played on the column is at coord."""
	p_row, p_col = coord
	if p_col != col:
		return False
	if p_row == 0:
		return True
	return board.state[p_row - 1][col] == board.EMPTY


def draw_pieces(screen, board, alignment, last_play_col):
	for row_i, row in enumerate(board.state):
		for col_i, elem in enumerate(row):
			if elem == board.EMPTY:
				continue
			coord = row_i, col_i
			special = coord in alignment or top_of_col(board, coord, last_play_col)

			if elem == Game.PLAYERS[0]:
				color = P0_SPEC_COL if special else P0_COL
			else:
				color = P1_SPEC_COL if special else P1_COL
			draw_piece(screen, row_i, col_i, color)


def get_column_from_coord(x: int) -> int | None:
	"""Translate x coordinate from mouse click to a column on the board.
	Returns None if the mouse was not on any column."""
	if not MARGIN_WIDTH <= x <= W - MARGIN_WIDTH:
		return None

	# get the ratio of how far is it along the board
	ratio = (x - MARGIN_WIDTH) / GRID_WIDTH

	# convert that ratio to a column
	col = int(ratio * NUM_COL)
	return col


def main():
	screen = pygame.display.set_mode((W, H))
	pygame.display.set_caption('Unbeatable 4 in a row')
	clock = pygame.time.Clock()

	initial = [
		list('.......'),
		list('.......'),
		list('.......'),
		list('.......'),
		list('..+#...'),
		list('..+#+#.'),
	]
	game = Game(verbose=True)
	fiar_mm = FIARMinMax(game, max_depth=5, plays=1, verbose=True, mt=False)

	running = True
	while running:
		screen.fill(THECOLORS['black'])

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				col = get_column_from_coord(x)
				if col is not None:
					game.play(col)
			elif event.type == KEYDOWN:
				# reset
				if event.key == K_r:
					game.__init__()
				# column input
				elif event.unicode in [str(i) for i in range(NUM_COL)]:
					col = int(event.unicode)
					game.play(col)

		draw_pieces(screen, game.board, game.alignment, game.last_play)
		draw_grid(screen, NUM_ROW, NUM_COL)
		pygame.display.update()

		algo_player_sym = Game.PLAYERS[fiar_mm.plays]
		if game.playing == algo_player_sym and not game.over:
			col = fiar_mm.get_best_play()
			game.play(col)

		clock.tick(30)


if __name__ == '__main__':
	main()
