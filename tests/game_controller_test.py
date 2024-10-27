import sys, os

sys.path.append("..")
# make sure test in gomuku/tests directory
from game_controller import GameController


WIDTH = 900
HEIGHT = 1000
MARGIN = 100
LINE_SPACE = 50
BOTTOM_MARGIN = 100


def test_constructor():
    """test player names"""
    gc = GameController("1", "p2", WIDTH, HEIGHT, MARGIN)
    assert gc.p1 == "1"
    assert gc.p2 == "p2"

def test_game_over():
    """test game over or not"""
    gc1 = GameController("1", "p2", WIDTH, HEIGHT, MARGIN)
    assert gc1.game_over is False
    assert gc1.winner() is False
    gc1.p1_wins = True
    assert gc1.winner() is True
    assert gc1.game_over() is True

def test_game_flag():
    """test game winning/tie flags"""
    gc2 = GameController("1", "p2", WIDTH, HEIGHT, MARGIN)
    assert gc2.winner() is False
    assert gc2.game_over() is False
    gc2.p1_wins = True
    assert gc2.winner() is True
    assert gc2.game_over() is True


def test_record_result():
    """test file log winner name"""
    gc3 = GameController("1", "p2", WIDTH, HEIGHT, MARGIN)
    path = "../txt/scores.txt"
    # remove score.txt if exists
    if os.path.exists(path):
        os.remove(path)
    winner_name = "Winner"
    winnings = 2
    gc3.record_result(winner_name, "../")
    gc3.record_result(winner_name, "../")

    with open(path, "r", encoding="utf-8") as file:
        line = file.readline()
        line = line.strip()
        assert line.split(" ")[0] == winner_name
        assert line.split(" ")[1] == str(winnings)


def test_check_name():
    """test for checking a valid player name"""
    gc4 = GameController("1", "p2", WIDTH, HEIGHT, MARGIN)
    name = "123"
    assert gc4.check_name(name)[0] is False
    name = "al4ice"
    assert gc4.check_name(name)[0] is True
    assert gc4.check_name(name)[1] == "Alice"
