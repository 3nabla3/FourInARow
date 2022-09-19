from pygame.color import THECOLORS
import pygame
from pygame.locals import *
from four_in_a_row import Game

pygame.init()

W, H = 800, 600


def draw_vert_line(screen, x, min_y, max_y):
	pygame.draw.line(screen, THECOLORS['turquoise'], (x, min_y), (x, max_y))


def draw_horiz_line(screen, y, min_x, max_x):
	pygame.draw.line(screen, THECOLORS['turquoise'], (min_x, y), (max_x, y))


def draw_grid(screen, n_cols, n_rows):
	# leave a 5% margin on left and right
	horiz_margin = 0.05
	grid_width = W * (1 - horiz_margin * 2)
	margin_width = W * horiz_margin

	# leave a 3% margin on top and bottom
	vert_margin = 0.03
	grid_height = H * (1 - vert_margin * 2)
	margin_height = H * vert_margin

	for i in range(n_cols + 1):
		draw_vert_line(screen, margin_width + (grid_width / n_cols) * i, min_y=margin_height, max_y=H - margin_height)

	# the top of the board is open so the pieces can fall in
	for i in range(1, n_rows + 1):
		draw_horiz_line(screen, margin_height + (grid_height / n_rows) * i, min_x=margin_width, max_x=W - margin_width)


def get_int_from_key(key):
	# takes a pygame key input and returns the int associated iif the key is a number
	print(key.to_bytes(10))


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
			if event.type == MOUSEBUTTONDOWN:
				# TODO: accept mouse input as well
				pass
			if event.type == KEYDOWN:
				num = int(event.unicode)
				if num in range(7):
					print(f'playing {num=}')
					game.play(num)

		draw_grid(screen, 7, 6)

		pygame.display.update()


if __name__ == '__main__':
	main()
