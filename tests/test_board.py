from pytest import raises


def test_column_valid(board):
	for i in range(board.WIDTH):
		board.insert_piece(i, '#')


def test_column_invalid(board):
	with raises(ValueError):
		board.insert_piece(-1, '#')
	with raises(ValueError):
		board.insert_piece(0.5, '#')
	with raises(ValueError):
		board.insert_piece(board.WIDTH, '#')
	with raises(ValueError):
		board.insert_piece(board.WIDTH + 1, '#')
