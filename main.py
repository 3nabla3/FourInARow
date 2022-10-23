import pygame
from pygame.color import THECOLORS
from pygame.locals import *

from fiar_min_max import FIARMinMax
from four_in_a_row import Game
from gui import get_column_from_coord, draw_grid, draw_pieces, W, H, NUM_ROW, NUM_COL

pygame.init()


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
					fiar_mm.__init__(
						game, max_depth=fiar_mm.max_depth,
						plays=fiar_mm.plays, verbose=fiar_mm.verbose, mt=fiar_mm.mt)

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


def bot_vs_bot():
	screen = pygame.display.set_mode((W, H))
	pygame.display.set_caption('Unbeatable 4 in a row')
	clock = pygame.time.Clock()

	game = Game(verbose=True)
	fiar_mm0 = FIARMinMax(game, max_depth=5, plays=0, verbose=True, mt=False)
	fiar_mm1 = FIARMinMax(game, max_depth=6, plays=1, verbose=True, mt=False)

	running = True
	while running:
		screen.fill(THECOLORS['black'])

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False

		draw_pieces(screen, game.board, game.alignment, game.last_play)
		draw_grid(screen, NUM_ROW, NUM_COL)
		pygame.display.update()

		fiar = fiar_mm0 if game.playing == Game.PLAYERS[fiar_mm0.plays] else fiar_mm1
		if not game.over:
			col = fiar.get_best_play()
			game.play(col)

		clock.tick(1)


if __name__ == '__main__':
	main()
