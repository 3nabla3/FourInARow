import pytest
from four_in_a_row import Board


@pytest.fixture
def board():
	return Board()
