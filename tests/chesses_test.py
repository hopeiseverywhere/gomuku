import sys, os

sys.path.append("..")
# make sure test in gomuku/tests directory
from game_controller import GameController
from chesses import Chesses

width = 900
height = 1000
margin = 100
line_space = 50

gc = GameController("p1", "p2", width, height, margin)


def test_constructor():
    """test constructor"""
    all_chesses = Chesses(width, height, margin, line_space, gc)
    assert all_chesses.gc is gc
    # test matrix size
    assert all_chesses.N == int((width - 2 * margin) / line_space + 1)

    width1 = 900
    height1 = 1000
    margin1 = 100
    line_space1 = 20

    all_chesses2 = Chesses(width1, height1, margin1, line_space1, gc)
    assert all_chesses2.N == int((width1 - 2 * margin1) / line_space1 + 1)


def test_add_chess():
    """give row, col indices and player name, testing whether
    a corresponding chess is added to display matrix"""
    all_chesses = Chesses(width, height, margin, line_space, gc)
    row = 1
    col = 1
    assert all_chesses.chesses_display_matrix[row][col] is None
    all_chesses.add_chess(row, col, "player")
    assert all_chesses.chesses_display_matrix[row][col] is not None
    assert all_chesses.chesses_display_matrix[row][col].get_chess_value == 1

    row = 4
    col = 11
    all_chesses.add_chess(row, col, "Computer")
    assert all_chesses.chesses_display_matrix[row][col] is not None
    assert all_chesses.chesses_display_matrix[row][col].get_chess_value == 2

    # test you can't add chess to a occupied location
    all_chesses.add_chess(row, col, "player")
    assert all_chesses.chesses_display_matrix[row][col].get_chess_value == 2


def test_is_empty():
    """test a display coordinate is empty or not"""
    all_chesses = Chesses(width, height, margin, line_space, gc)
    assert all_chesses.is_empty(100, 200) is True
    all_chesses.coord_set.add((100, 200))
    assert all_chesses.is_empty(100, 200) is False