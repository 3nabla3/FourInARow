from dataclasses import dataclass
from typing import Union

from four_in_a_row import Board, Game


@dataclass
class Node:
	"""A node is a block of data used in trees"""
	board: Board
	game_state: Game.GameState
	delta: int  # the move that resulted in the current board
	playing: int = 0  # who's turn is it to play
	maximizing: bool = (playing == 0)  # the convention is that P1 maximizes while P2 minimizes
	score: Union[int, None] = None  # the minmax score associated with the board


class MinMaxTree:
	"""A tree is recursively defined as being a block of data (a node) along with
	a list of trees (subtrees)."""

	def __init__(self, board, playing, *, delta=None):
		game_state = Game.get_state_static(board)
		self._node = Node(board, game_state, delta, playing)

		# the children will be generated later
        # TODO: should it actually??
        self.children = []

	def generate_tree(self, depth):
		# exit condition of the recursion
		if depth <= 0:
			return

		for col in self._node.board.get_valid_columns():
			new_board = self._node.board.__copy__()
			new_board.insert_piece(col, Game.PLAYERS[self._node.playing])
			new_player = (self._node.playing + 1) % 2
			child = MinMaxTree(new_board, new_player, delta=col)
			self.children.append(child)

		for child in self.children:
			child.genrate_tree(depth - 1)

	def get_score(self):
		# if the score hasn't been calculated yet
		if not self._node.score:
			self._calculate_score()
		return self._node.score

	def _calculate_score(self):
		# if the node is a leaf, perform a static evaluation
		if not self.children:
			self._static_eval()

	def _static_eval(self):
		"""Let _score(p) be the length of the longest chain of player p that can still be expanded to 4.
		The static score of a board is defined as _score(P1) - _score(P2)"""
		self._node.score = self._score(0) - self._score(1)

	def _score(self, player: int) -> int:
		"""Calculates the score (how good their situation is) of a given player.
		Used in the static evaluation of the board"""

		# TODO: Refactor this shit

		longest_chain = 0

		# loop over all rows (top to bottom)
		for row_i in range(2, Board.HEIGHT):
			num_prev_empty = 0  # number of empty spots before the chain
			num_post_empty = 0  # number of empty spots after the chain
			chain_length = 0

			row = list(self._node.board.row_gen(row_i))
			for elem in row:
				if elem == Board.EMPTY:
					if chain_length == 0:
						num_prev_empty += 1
					elif chain_length > 0:
						num_post_empty += 1
					continue

				# this point will only happen on a player piece

				# if we haven't ended the chain
				if num_post_empty == 0:
					# if we are still getting the player's piece keep counting them
					if elem == Game.PLAYERS[player]:
						chain_length += 1
					# if it is blocked by the opponent's piece, the chain is finished and reset it
					else:
						if longest_chain < chain_length and num_prev_empty + chain_length + num_post_empty >= 4:
							longest_chain = chain_length
						num_prev_empty = 0
						chain_length = 0

				# if we hit the end of post empty pieces
				elif num_post_empty > 0:
					# record the chain we just found
					if longest_chain < chain_length and num_prev_empty + chain_length + num_post_empty >= 4:
						longest_chain = chain_length

					# if another chain starts, transfer the count of empty pieces
					if elem == Game.PLAYERS[player]:
						num_prev_empty = num_post_empty
					# if not, reset both counters
					else:
						num_prev_empty = 0
					num_post_empty = 0

			if longest_chain < chain_length and num_prev_empty + chain_length + num_post_empty >= 4:
				longest_chain = chain_length

		return longest_chain


if __name__ == '__main__':
	# initial = [
	# 	['.'] * 7,
	# 	*[[Game.PLAYERS[(j // 2 + i) % 2] for j in range(7)] for i in range(6)]
	# ]
	initial = [
		list('.' * 7),
		list('.' * 7),
		list('....+..'),
		list('...++#.'),
		list('.#.##+.'),
		list('+#+##+.')
	]
	game = Game(initial_board=initial)
	print(game)
	fiar_mm = MinMaxTree(game.board, 0)
	fiar_mm.generate_tree(0)
	print(fiar_mm._score(0), fiar_mm._score(1))
	pass
