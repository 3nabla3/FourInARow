# tests how long it takes to generate the tree
from multiprocessing import Process

import pytest

from four_in_a_row import Board
from min_max_tree import MinMaxTree


# this should not be a test because it depends how many background tasks are running
# and on the power of the computer, it is only for my own information because it
# is still a nonfunctional requirement. It would be very bland to play with an
# unbearably slow algorithm
@pytest.mark.parametrize(
	('depth', 'max_time'), (
			(4, 1),
			(5, 5),
			(6, 15)
	))
def _test_gen_tree(depth, max_time):  # max time in seconds
	thread = Process(target=generate_tree, args=(depth,))
	thread.start()
	thread.join(timeout=max_time)
	assert not thread.is_alive()
	thread.kill()


def generate_tree(depth):
	tree = MinMaxTree(Board(), 0)
	tree.generate_tree(depth)
