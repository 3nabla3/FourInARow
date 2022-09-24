from pygame.color import THECOLORS
import pygame
from pygame.locals import *
from four_in_a_row import Game

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


def get_int_from_key(key):
	# takes a pygame key input and returns the int associated iif the key is a number
	print(key.to_bytes(10))


def draw_piece(screen, row, col, color):
	square_width = GRID_WIDTH / NUM_COL
	square_height = GRID_HEIGHT / NUM_ROW
	x = MARGIN_WIDTH + square_width * (col + 0.5)
	y = MARGIN_HEIGHT + square_height * (row + 0.5)

	pygame.draw.circle(screen, THECOLORS[color], (x, y), 20)


def draw_pieces(screen, board):
	for row_i, row in enumerate(board.state):
		for col_i, elem in enumerate(row):
			if elem in Game.PLAYERS:
				color = 'red' if elem == Game.PLAYERS[0] else 'blue'
				draw_piece(screen, row_i, col_i, color)


def main():
	screen = pygame.display.set_mode((W, H))
	pygame.display.set_caption('Unbeatable 4 in a row')

	game = Game()

	running = True
	while running:
		screen.fill(THECOLORS['black'])

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == MOUSEBUTTONDOWN:
				# TODO: accept mouse input as well
				pass
			elif event.type == KEYDOWN:
				# reset
				if event.key == K_r:
					game.__init__()
				# column input
				else:
					num = int(event.unicode)
					if num in range(NUM_COL) and not game.over:
						game.play(num)

		draw_pieces(screen, game.board)
		draw_grid(screen, NUM_ROW, NUM_COL)

		pygame.display.update()


if __name__ == '__main__':
	main()
