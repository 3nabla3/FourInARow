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

	def __init__(self, board, playing, *, delta=None, children: 'MinMaxTree' = None):
		game_state = Game.get_state_static(board)
		self.node = Node(board, game_state, delta, playing)

		self.children = children or []
