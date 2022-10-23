from dataclasses import dataclass

from four_in_a_row import Board, Game


@dataclass
class Node:
	"""A node is a block of data used in trees"""
	board: Board
	game_state: Game.GameState
	delta: int  # the move that resulted in the current board
	playing: int  # who's turn is it to play
	score: int | None = None  # the minmax score associated with the board
	alpha = beta = None  # these will get initiated when calculating the score

	@property
	def maximizing(self):
		# the convention is that P1 maximizes while P2 minimizes
		return self.playing == 0


class MinMaxTree:
	"""A tree is recursively defined as being a block of data (a node) along with
	a list of trees (subtrees)."""

	def __init__(self, board, playing: int, *, delta=None):
		game_state = Game.get_state_static(board)
		self.node = Node(board, game_state, delta, playing)

		# used to make more distant results less valuable than closer ones.
		# this forces the algo to win in the fastest way possible and lose in the longest way
		self.damping_factor = 0.9

		# the children will be generated later
		# TODO: should it actually??
		self.children: list[MinMaxTree] = []

	def child_already_exists(self, col):
		return any(filter(lambda child: child.node.delta == col, self.children))

	def generate_tree(self, depth):
		"""Makes sure the tree is the right depth,
		needs to be called every time the tree is moved to one of its children."""

		# if the tree is already deep enough or the node is a leaf
		if depth <= 0 or self.node.game_state is not Game.GameState.IN_PROGRESS:
			return

		# reset the score so it gets recalculated
		self.node.score = None

		# make sure every direct child exists
		for col in self.node.board.get_valid_columns():
			if self.child_already_exists(col):
				continue
			new_board = self.node.board.__copy__()
			new_board.insert_piece(col, Game.PLAYERS[self.node.playing])
			new_player = (self.node.playing + 1) % 2
			child = MinMaxTree(new_board, new_player, delta=col)
			self.children.append(child)

		# call the method recursively for every child
		for child in self.children:
			child.generate_tree(depth - 1)

	def get_score(self):
		# if the score hasn't been calculated yet
		if self.node.score is None:
			self.node.score = self.minimax(alpha=-float('inf'), beta=float('inf'))
		return self.node.score

	def minimax(self, alpha, beta) -> float:
		"""https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/."""

		# if the node is a leaf, perform a static evaluation
		if not self.children:
			return self._static_eval()

		# TODO: find a way to arrange children by order of likeliness to be good

		# if not perform a dynamic evaluation
		best, worse = (max, min) if self.node.maximizing else (min, max)

		best_val = worse(-float('inf'), float('inf'))
		for child in self.children:
			value = child.minimax(alpha, beta)
			child.node.score = value

			best_val = best(best_val, value)
			# if maximizing, update alpha
			if self.node.maximizing:
				alpha = best(alpha, best_val)
			# if not, update the beta
			else:
				beta = best(beta, best_val)
			# check if we can prune the branch
			if beta <= alpha:
				break

		return best_val * self.damping_factor

	def _static_eval(self) -> int:
		"""Let _score(p) be the length of the longest chain of player p that can still be expanded to 4.
		The static score of a board is defined as _score(P1) - _score(P2)."""
		# if the state is decisive, the score is obvious
		if self.node.game_state is Game.GameState.P1_WON:
			return 5
		elif self.node.game_state is Game.GameState.P2_WON:
			return -5
		elif self.node.game_state is Game.GameState.TIE:
			return 0
		# otherwise calculate the score with the proposed algo
		return self._score(player=0) - self._score(player=1)

	@staticmethod
	def _analyze_line(line: list, player) -> int:
		"""Return 4 - (the minimum number of pieces the player has to add to the line
		in order to get a 4 in a row on that line). If there is not enough space to get a 4
		in a row, return 0"""

		# if making a 4 in a row is impossible, return immediately
		if len(line) < 4 or line.count(Board.EMPTY) + line.count(Game.PLAYERS[player]) < 4:
			return 0

		# split the line on every opponent piece and treat each segment independently
		other_player = Game.PLAYERS[(player + 1) % 2]
		if line.count(other_player):  # if the line can be split
			segments = [list(seg) for seg in "".join(line).split(other_player)]
			results = (MinMaxTree._analyze_line(seg, player) for seg in segments)
			return max(results)

		# at this point, the line only contains empty or player pieces, and it is possible to get a line of 4
		counts = []

		left = 4  # how many slots left before it is not possible to make a 4 in a row
		count = 0  # how long the chain is
		started: None | int = None  # index of where the chain starts, None if it didn't start yet

		# loop over every piece of the line
		i = 0
		while i < len(line):
			sym = line[i]
			if started is None:
				# start the chain
				if sym == Game.PLAYERS[player]:
					started = i
			if started:
				if sym == Game.PLAYERS[player]:
					# add one piece to the chain
					left -= 1
					count += 1
				else:  # if empty
					# add one to the length of the potential chain
					left -= 1
				if left == 0 or i == len(line) - 1:
					# if we finished a chain, reset
					counts.append(count)
					i = started + 1
					count = 0
					left = 4
					started = None

			i += 1

		# return the longest chain in the line
		return max(counts) if counts else 0

	def _score(self, player: int) -> int:
		"""Calculate the score (how good their situation is) of a given player.
		Used in the static evaluation of the board.
		Return the length of the longest chain in the board for the given player.
		"""

		chain_lengths = (self._analyze_line(list(line), player) for line in self.node.board.gen_all_lines())
		return max(chain_lengths)

	def __repr__(self):
		if self.node.score is not None:
			return f"{'max' if self.node.maximizing else 'min'} score: {self.node.score}"
		return "Branch pruned out"


if __name__ == '__main__':
	def main():
		initial = [
			list(' ' * 7),
			list(' ' * 7),
			list('    +  '),
			list('   ++# '),
			list(' # ##+ '),
			list('+#+##+ ')
		]
		game = Game(initial_board=initial)
		print(game)
		fiar_mm = MinMaxTree(game.board, 0)
		fiar_mm.generate_tree(0)
		score = fiar_mm.get_score()
		print(f"{score = }")


	main()
