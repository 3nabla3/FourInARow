class Board:
	"""A board is a 7 * 6 board of red, black or empty pieces"""
	WIDTH = 7
	HEIGHT = 6
	EMPTY = '.'

	def __init__(self, *, initial_state=None):
		if initial_state:
			self.state = initial_state
		else:
			self.state = [[self.EMPTY for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

	def reset(self, *, initial_state=None):
		self.__init__(initial_state=initial_state)

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

	# returns a generator for the given row
	def row_gen(self, row_i):
		return (self.state[row_i][i] for i in range(self.WIDTH))

	# returns a generator for the given col
	def col_gen(self, col_i):
		return (self.state[i][col_i] for i in range(self.HEIGHT))

	# returns a generator for the given up diag (SW to NE)
	def up_diag_gen(self, diag_i):
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

	# returns a generator for the given down diag (NW to SE)
	def dn_diag_gen(self, diag_i):
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

	def __str__(self, adf=False):
		res = ""

		# put the column numbers
		res += '|'
		for c in range(self.WIDTH):
			res += f'\t{c}'
		res += '\t|\n'

		# put the actual board
		for row in self.state:
			res += '|'
			for elem in row:
				res += f"\t{elem}"
			res += f"\t|\n"

		return res


class Game:
	PLAYERS = ['#', '+']

	def __init__(self, initial_board: Board = None):
		# index of the player whose turn it is
		self.p_i = 0
		self.board = initial_board or Board()

	@property
	def playing(self):
		return self.PLAYERS[self.p_i]

	@property
	def not_playing(self):
		return self.PLAYERS[(self.p_i + 1) % 2]

	def switch_player(self):
		self.p_i = (self.p_i + 1) % 2

	def play(self, column):
		try:
			self.board.insert_piece(column, self.playing)
		except ValueError as e:
			print("Error: ", e)
		else:
			self.switch_player()

	def check_win(self, player: int) -> tuple[str, tuple[int, int]]:
		"""
		Check if a player has won the game

		the type of win (string)
			* none (no win)
			* row (win in a row)
			* col (win in a column)
			* ud (win in a positive slope diag)
			* dd (win in a negative slope diag)
		the coordinate (tuple) of the leftmost (if tied, upmost), element in the alignment
			* (-1, -1) if no win

		:param player: the player to analyze
		:return: the tuple representing the state
		"""

		# we need to find the symbol 4 times in a row
		p_sym = self.PLAYERS[player]
		to_find = p_sym * 4

		# check rows
		for row_i in range(self.board.HEIGHT):
			row_s = ''.join(self.board.row_gen(row_i))
			if (col_i := row_s.find(to_find)) >= 0:
				return 'row', (row_i, col_i)

		# check columns
		for col_i in range(self.board.WIDTH):
			col_s = ''.join(self.board.col_gen(col_i))
			if (row_i := col_s.find(to_find)) >= 0:
				return 'col', (row_i, col_i)

		# check the positive slope diags
		for up_diag_i in range(Board.HEIGHT + Board.WIDTH - 1):
			up_diag_s = ''.join(self.board.up_diag_gen(up_diag_i))
			if (i := up_diag_s.find(to_find)) >= 0:
				if up_diag_i < Board.HEIGHT:
					return 'ud', (up_diag_i - i, i)
				else:
					return 'ud', (Board.HEIGHT - i - 1, up_diag_i - Board.HEIGHT + i + 1)

		# check the negative slope diags
		for dn_diag_i in range(Board.HEIGHT + Board.WIDTH - 1):
			dn_diag_s = ''.join(self.board.dn_diag_gen(dn_diag_i))
			if (i := dn_diag_s.find(to_find)) >= 0:
				if dn_diag_i < Board.HEIGHT:
					return 'dd', (Board.HEIGHT - dn_diag_i + i - 1, i)
				else:
					return 'dd', (i, dn_diag_i - Board.HEIGHT + i + 1)

		return 'none', (-1, -1)

	# returns the non-empty columns
	def get_valid_columns(self):
		for i in range(Board.WIDTH):
			if self.board.state[0][i] == self.board.EMPTY:
				yield i

	def __str__(self):
		return str(self.board)


if __name__ == '__main__':
	def main():
		g = Game()
		print(g)
		while True:
			c = int(input(f"Enter a column {list(g.get_valid_columns())}: "))
			g.play(c)
			print(g.check_win(0))
			print(g)

	main()
