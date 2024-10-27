import sys

sys.path.append("..")
# make sure test in gomuku/tests directory
from board import Board
from game_controller import GameController
from computer import Computer

width = 900
height = 1000
margin = 100
line_space = 50
bottom_margin = 100

gc = GameController("p1", "p2", width, height, margin)
computer = Computer()
board = Board(width, height, margin, line_space, bottom_margin, gc, computer)

def test_constructor():
    
    assert board.gc is gc
    assert board.computer is computer
    assert board.empty_target is computer.empty_target
    assert board.player_target is computer.player_target
    assert board.computer_target is computer.computer_target


def test_add_chess_to_display():
    """test player / computer add a chess to display"""
    row = 3
    col = 5
    player_name = "Alice"
    board.add_chess_to_display(row, col, player_name)
    assert board.total_chesses == 1
    row = 8
    col = 10
    board.add_chess_to_display(row, col, computer.name)
    assert board.total_chesses == 2

def test_add_player_loc():
    assert board.players_matrix[3][5] is board.player_target


def test_is_board_full():
    assert board.is_board_full() is False
    player_name = "Alice"
    for row in range(15):
        for col in range(15):
            board.add_chess_to_display(row, col, player_name)
    
    assert board.is_board_full() is True

def test_who_wins():
    assert board.who_wins() is board.player_target

def test_check_game_board():
    assert gc.p1_wins
