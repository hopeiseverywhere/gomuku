from board import Board
from game_controller import GameController
from computer import Computer

WIDTH = 900
HEIGHT = 1000
MARGIN = 100
LINE_SPACE = 50
BOTTOM_MARGIN = 100

is_player_turn = True

player_name = ""
is_name_valid = None

computer = Computer()
game_controller = GameController(player_name, computer.get_name, WIDTH, HEIGHT, MARGIN, LINE_SPACE)
board = Board(WIDTH, HEIGHT, MARGIN, LINE_SPACE, BOTTOM_MARGIN, 
game_controller, computer)

game_start_state = True
log_winner_state = True
mouse_effect_state = 0

game_over = False
winner = False

count = 0
wait = 0
is_logged = False

def setup():
    size(WIDTH, HEIGHT)
    

def draw():
    global game_start_state, log_winner_state
    global winner, game_over, is_logged
    global count, wait
    global is_player_turn, player_name, is_name_valid

    background(225,142,76,255)
    board.display_lines()
    board.display()    

    # when game starts
    if game_start_state:
        # display welcoming message
        game_controller.display_game_start()
        game_controller.display_button()
        
    
    if (not game_over and not game_start_state):
        if mouse_effect_state == 1:
            board.display_mouse_effect()
        
        if wait == 0:
            count = count + 1 
        else:
            wait -= 1

        if not is_player_turn and wait == 0:
            board.com_add_chess()
            board.display()
            is_player_turn = True

        # if game is over, end the game
        game_over = game_controller.game_over()

    if game_over:
        # check winner
        winner = game_controller.winner()

        # when game ends and player wins
        # ask user to enter player name
        if log_winner_state and game_controller.p1_wins:
            game_controller.display_log_winner()
            if is_name_valid is None:
                game_controller.display_msg(player_name)
            if is_name_valid is False:
                game_controller.display_msg("Please enter a VALID name")

        if not log_winner_state:
            if winner:
                game_controller.update_winner()
            else:
                # check ties
                game_controller.update_ties()

            # log winner, use a flag to make sure it only logs once
            if not is_logged:
                game_controller.record_result(player_name)
                is_logged = True

def mouseMoved():
    global mouse_effect_state
    mouse_effect_state = 1
    
def mousePressed(): 
    global game_start_state
    global is_player_turn, wait, player_name

    # if game start let the user to click start button
    if game_start_state:
        game_start_state = game_controller.button_clicked()

    if is_player_turn:
        # using a flag to prevent user clicked somewhere outside of the board
        flag = board.player_add_chess(player_name)
        if flag:
            wait = 80
            is_player_turn = False
    
def keyPressed():
    global log_winner_state
    global player_name, is_name_valid
    is_name_valid = None

    # let user enter name
    if key == 65535:
        # ignore CAPS
        pass
    elif key == '\x08':
        # delete keys
        player_name = player_name[:-1]
    else:
        player_name += str(key)
    
    if key == ENTER :
        # check if name is valid
        result = game_controller.check_name(player_name)
        is_name_valid, player_name = result[0], result[1]
        
        if is_name_valid is False:
            player_name = ""
        if is_name_valid is True:
            # user entered a valid name, so update it to controller class
            game_controller.update_player_name(player_name)
            log_winner_state = False    
