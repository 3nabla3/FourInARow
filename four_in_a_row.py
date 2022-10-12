from enum import Enum, auto

from colorama import Fore, Style


class Board:
	"""A board is a 7 * 6 board of red, black or empty pieces"""
	WIDTH = 7
	HEIGHT = 6
	EMPTY = '.'

	def __init__(self, initial_state=None):
		if initial_state:
			self.state = initial_state
		else:
			self.state = [[self.EMPTY for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

	def reset(self, *, initial_state=None):
		self.__init__(initial_state=initial_state)

	def get_valid_columns(self):
		"""Returns the indices of non-empty columns."""
		for i in range(Board.WIDTH):
			if self.state[0][i] == self.EMPTY:
				yield i

	def insert_piece(self, column, piece):
		if column not in range(self.WIDTH):
			raise ValueError("The column is invalid")

		# if there is no more room in that column
		if self.state[0][column] != self.EMPTY:
			raise ValueError("The column is full")

		# 'row' represents the row the piece is currently in as it is falling down
		for row in range(self.HEIGHT):
			# if we are on the last row, or there is another piece below
			if row == self.HEIGHT - 1 or self.state[row + 1][column] != self.EMPTY:
				# place the piece and move on
				self.state[row][column] = piece
				break

	def gen_row(self, row_i):
		"""Returns a generator for the given row."""
		return (self.state[row_i][i] for i in range(self.WIDTH))

	def gen_col(self, col_i):
		"""Returns a generator for the given column."""
		return (self.state[i][col_i] for i in range(self.HEIGHT))

	def gen_up_diag(self, diag_i):
		"""Returns a generator for the given up diag (SW to NE)."""
		# if the diag starts on the first column
		if diag_i < Board.HEIGHT:
			row_i = diag_i
			col_i = 0
		# if the diag starts on the bottom row
		else:
			row_i = Board.HEIGHT - 1
			col_i = diag_i - Board.HEIGHT + 1

		# keep going NE until off the grid
		while row_i >= 0 and col_i < self.WIDTH:
			yield self.state[row_i][col_i]
			row_i -= 1
			col_i += 1

	def gen_dn_diag(self, diag_i):
		"""Returns a generator for the given down diag (NW to SE)."""
		# if the diag starts on the first column
		if diag_i < Board.HEIGHT:
			row_i = Board.HEIGHT - diag_i - 1
			col_i = 0
		# if the diag starts on the top row
		else:
			row_i = 0
			col_i = diag_i - Board.HEIGHT + 1

		# keep going SE until off the grid
		while row_i < Board.HEIGHT and col_i < Board.WIDTH:
			yield self.state[row_i][col_i]
			row_i += 1
			col_i += 1

	def gen_all_lines(self):
		"""Simply utility that yields generators for all the lines."""

		for i in range(self.HEIGHT):
			yield self.gen_row(i)
		for i in range(self.WIDTH):
			yield self.gen_col(i)
		for i in range(self.HEIGHT + self.WIDTH - 1):
			yield self.gen_up_diag(i)
		for i in range(self.HEIGHT + self.WIDTH - 1):
			yield self.gen_dn_diag(i)

	def __iter__(self):
		for row in self.state:
			yield row

	def __copy__(self):
		copied_state = [row.copy() for row in self.state]
		return Board(copied_state)

	def __eq__(self, other):
		assert len(self.state) == len(other.state)
		for self_row, other_row in zip(self.state, other.state):
			if self_row != other_row:
				return False
		return True

	def __str__(self, alignment=None):
		alignment = alignment or []
		res = ""

		# put the column numbers
		res += '|'
		for c in range(self.WIDTH):
			res += f'\t{c}'
		res += '\t|\n'

		# put the actual board
		for y, row in enumerate(self.state):
			res += '|'
			for x, elem in enumerate(row):
				if (y, x) in alignment:
					res += f"\t{Fore.RED}{elem}{Style.RESET_ALL}"
				else:
					res += f"\t{elem}"
			res += f"\t|\n"

		return res


class Game:
	PLAYERS = ['#', '+']

	class GameState(Enum):
		IN_PROGRESS = auto()
		TIE = auto()
		P1_WON = auto()
		P2_WON = auto()

	def __init__(self, initial_board: Board | list[list[str]] = None, *, verbose=False):
		# index of the player whose turn it is
		if initial_board:
			p1_count = sum(row.count(Game.PLAYERS[0]) for row in initial_board)
			p2_count = sum(row.count(Game.PLAYERS[1]) for row in initial_board)
			self.p_i = 1 if p1_count > p2_count else 0
		else:
			self.p_i = 0

		# column that was last played
		# (used by the algo to figure out how to move around the tree)
		self.last_play: int | None = None

		# if the given board is a list, convert it to a board first
		if isinstance(initial_board, list):
			initial_board = Board(initial_board)

		# if an initial board was given, set it and update the board state
		self.board = initial_board or Board()
		if initial_board:
			self._update_board_state()
		else:
			self._state = self.GameState.IN_PROGRESS
		# the coordinate of the 4 pieces in a row (used for graphics)
		self.alignment = []
		self.verbose = verbose

	def debug_print(self, *args, **kwargs):
		if self.verbose:
			print(*args, **kwargs)

	@property
	def playing(self):
		return self.PLAYERS[self.p_i]

	@property
	def not_playing(self):
		return self.PLAYERS[(self.p_i + 1) % 2]

	def switch_player(self):
		self.p_i = (self.p_i + 1) % 2

	@property
	def over(self):
		return self.get_state() is not self.GameState.IN_PROGRESS

	def get_state(self):
		if not self._state:
			self._update_board_state()
		return self._state

	@staticmethod
	def get_state_static(board):
		temp = Game(initial_board=board)
		return temp.get_state()

	def _update_board_state(self):
		if alignment := self.get_4_in_row(0):
			self._state = self.GameState.P1_WON
		elif alignment := self.get_4_in_row(1):
			self._state = self.GameState.P2_WON
		elif not any(self.board.get_valid_columns()):
			self._state = self.GameState.TIE
		else:
			self._state = self.GameState.IN_PROGRESS

		self.alignment = alignment or []

	def play(self, column):
		if self.over:
			self.debug_print('Game is over!')
			return
		try:
			self.board.insert_piece(column, self.playing)
		except ValueError as e:
			self.debug_print("Error: ", e)
		else:
			self.switch_player()
		self._update_board_state()

		if self._state == self.GameState.P1_WON:
			self.debug_print('P1 won')
		elif self._state == self.GameState.P2_WON:
			self.debug_print('P2 won')
		elif self._state == self.GameState.TIE:
			self.debug_print('Tie')

		self.last_play = column

	def get_4_in_row(self, player: int) -> list[tuple]:
		"""
		Check if a player has won the game and get the coordinates of the alignment
		:param player: the player to analyze
		:return: a list of tuples representing the aligned pieces
		"""

		# we need to find the symbol 4 times in a row
		p_sym = self.PLAYERS[player]
		to_find = p_sym * 4

		# check rows
		for row_i in range(self.board.HEIGHT):
			row_s = ''.join(self.board.gen_row(row_i))
			if (col_i := row_s.find(to_find)) >= 0:
				return [(row_i, col_i + j) for j in range(4)]

		# check columns
		for col_i in range(self.board.WIDTH):
			col_s = ''.join(self.board.gen_col(col_i))
			if (row_i := col_s.find(to_find)) >= 0:
				return [(row_i + j, col_i) for j in range(4)]

		# check the positive slope diags
		for up_diag_i in range(Board.HEIGHT + Board.WIDTH - 1):
			up_diag_s = ''.join(self.board.gen_up_diag(up_diag_i))
			if (i := up_diag_s.find(to_find)) >= 0:
				# get the starting coordinates for the alignment
				if up_diag_i < Board.HEIGHT:
					y, x = up_diag_i - i, i
				else:
					y, x = Board.HEIGHT - i - 1, up_diag_i - Board.HEIGHT + i + 1
				return [(y - j, x + j) for j in range(4)]

		# check the negative slope diags
		for dn_diag_i in range(Board.HEIGHT + Board.WIDTH - 1):
			dn_diag_s = ''.join(self.board.gen_dn_diag(dn_diag_i))
			if (i := dn_diag_s.find(to_find)) >= 0:
				# get the starting coordinates for the alignment
				if dn_diag_i < Board.HEIGHT:
					y, x = Board.HEIGHT - dn_diag_i + i - 1, i
				else:
					y, x = i, dn_diag_i - Board.HEIGHT + i + 1
				return [(y + j, x + j) for j in range(4)]

		return []

	def __str__(self, *args, **kwargs):
		return self.board.__str__(*args, **kwargs)


if __name__ == '__main__':
	def main():
		g = Game()
		print(g)
		align = []
		while not align:
			c = int(input(f"Enter a column {list(g.board.get_valid_columns())}: "))
			g.play(c)
			align = g.get_4_in_row(player=0)
			print(g.__str__(align))


	main()
