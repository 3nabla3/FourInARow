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
	score: int | None = None  # the minmax score associated with the board


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

	@staticmethod
	def _analyze_line(line: list, player) -> int:
		"""Returns 4 - (the minimum number of pieces the player has to add to the line
		in order to get a 4 in a row on that line). If there is not enough space to get a 4
		in a row, return 0"""

		# if making a 4 in a row is impossible, return immediately
		if len(line) < 4 or line.count('.') + line.count(Game.PLAYERS[player]) < 4:
			return 0

		# split the line on every opponent piece and treat each segment independently
		other_player = Game.PLAYERS[(player + 1) % 2]
		if line.count(other_player):
			segments = [list(seg) for seg in "".join(line).split(other_player)]
			# print(f"split {line} in {segments}")
			results = [MinMaxTree._analyze_line(seg, player) for seg in segments]
			return max(results)

		pre = 0
		chain = 0
		inner = []  # the number of inner empty spaces between two chains
		post = 0
		for elem in line:
			# deal with the empty spots first
			if elem == Board.EMPTY:
				# if we are still before the chain
				if chain == 0:
					pre += 1
				# if we are after the chain
				else:
					post += 1
				continue

			# if we are still following the chain
			if post == 0:
				chain += 1
			# if we are hitting another chain
			else:
				chain += 1
				inner.append(post)
				post = 0

		# if the chain is split in two
		if inner:
			# if we don't need to extend to the sides
			if chain + sum(inner) >= 4:
				return 4 - sum(inner)
			# if we do
			if pre + chain + sum(inner) + post >= 4:
				return chain
		else:
			# if the chain is in one piece, and we can extend it to 4
			if pre + chain + post >= 4:
				return chain
		return 0

	def _score(self, player: int) -> int:
		"""Calculates the score (how good their situation is) of a given player.
		Used in the static evaluation of the board"""

		longest_chain = 0
		# find the longest chain in every line
		for line in (list(gen) for gen in self._node.board.gen_all_lines()):
			chain_len = self._analyze_line(line, player)
			if chain_len > longest_chain:
				longest_chain = chain_len

		return longest_chain


if __name__ == '__main__':
	def main():
		# initial = [
		# 	['.'] * 7,
		# 	*[[Game.PLAYERS[(j // 2 + i) % 2] for j in range(7)] for i in range(6)]
		# ]
		# initial = [
		# 	list('.' * 7),
		# 	list('.' * 7),
		# 	list('....+..'),
		# 	list('...++#.'),
		# 	list('.#.##+.'),
		# 	list('+#+##+.')
		# ]
		# game = Game(initial_board=initial)
		# print(game)
		# fiar_mm = MinMaxTree(game.board, 0)
		# fiar_mm.generate_tree(0)
		# print(fiar_mm._score2(0))
		# print(fiar_mm._score(0), fiar_mm._score(1))
		score = MinMaxTree._analyze_line(list('.#.#.+.'), 0)
		print(f"{score = }")


	main()
