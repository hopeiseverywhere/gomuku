from chesses import Chesses
from computer_module import check_x_or_more


class Board:
    """a board class"""

    def __init__(
        self,
        WIDTH,
        HEIGHT,
        MARGIN,
        LINE_SPACE,
        BOTTOM_MARGIN,
        game_controller,
        computer,
    ):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.MARGIN = MARGIN
        self.LINE_SPACE = LINE_SPACE
        self.BOTTOM_MARGIN = BOTTOM_MARGIN
        # chess radius
        self.radius = 30

        self.gc = game_controller
        self.computer = computer

        self.empty_target = computer.empty_target
        self.player_target = computer.player_target
        self.computer_target = computer.computer_target

        # a instance of all chesses
        self.chesses = Chesses(
            self.WIDTH, self.HEIGHT, self.MARGIN, self.LINE_SPACE, self.gc
        )

        # stores all chesses' playable locations in matrix
        self.coords_matrix = self.chesses.coords_matrix

        # distance to determine how close a mouse click can be
        self.DIST = 10

        # how big the matrix is
        self.N = self.chesses.N

        # stores all player locations in a matrix
        # 0: empty space
        # 1: player location
        # 2: computer location
        self.players_matrix = [[0 for col in range(self.N)] for row in range(self.N)]

        # number of consecutive chess to win
        self.COUNT = 5

        # number of total chesses
        self.total_chesses = 0
        # number of computer chesses
        self.computer_chesses = 0

        # stores horizontal and vertical lines' coordinates into sets
        self.hor_indices_set = set()
        self.ver_indices_set = set()

        # for displaying board coordinates
        self.text_size = 14

    def display_lines(self):
        """display board line"""
        strokeWeight(2)
        # draw lines
        # Horizontal line
        hor_start = self.MARGIN
        # line(self.MARGIN, hor_start, self.WIDTH - self.MARGIN, hor_start)
        while hor_start <= self.WIDTH - self.MARGIN and hor_start <= self.WIDTH:
            line(
                self.MARGIN,
                hor_start,
                self.HEIGHT - self.MARGIN - self.BOTTOM_MARGIN,
                hor_start,
            )
            self.hor_indices_set.add(hor_start)
            hor_start += self.LINE_SPACE

        # vertical line
        ver_start = self.MARGIN

        while ver_start <= self.WIDTH - self.MARGIN:
            line(ver_start, self.MARGIN, ver_start, self.WIDTH - self.MARGIN)
            self.ver_indices_set.add(ver_start)
            ver_start += self.LINE_SPACE

        self.display_indices()

    def display_indices(self):
        """display board indices"""
        fill(0, 0, 0, 255)
        textAlign(LEFT)
        textSize(self.text_size)
        LETTERS = "ABCDEFGHIJKLMNOPQRST"

        hor_indices = sort(list(self.hor_indices_set))
        # print(self.WIDTH + self.MARGIN)
        for i, hor in enumerate(hor_indices):
            text(LETTERS[i], hor - 4, self.WIDTH - self.MARGIN + self.radius)

        ver_indices = sort(list(self.hor_indices_set))
        i = self.N
        for ver in ver_indices:
            text(i, self.MARGIN - self.radius * 1.2, ver + 2)
            i -= 1

    def display(self):
        """display chesses"""
        self.chesses.display()

    def display_mouse_effect(self):
        """when mouse moved to an unoccupied slot
        display a black circle"""
        for row in self.coords_matrix:
            for coord in row:
                x = coord[0]
                y = coord[1]

                if (
                    abs(mouseX - x) <= self.DIST
                    and abs(mouseY - y) <= self.DIST
                    and self.chesses.is_empty(x, y)
                ):
                    fill(225, 142, 76, 255)
                    circle(x, y, self.radius)

    def add_chess_to_display(self, row, col, player_name):
        """given row and col indices on player locations matrix
        add a corresponding chess to display"""

        # add new chess instance
        self.chesses.add_chess(row=row, col=col, player=player_name)
        # add player location to player matrix
        self.add_player_loc(row, col, player_name)

        # increment chesses on board
        self.total_chesses += 1

        # testing purpose, print player locations matrix
        # self.print_players_matrix()
        # check winner and spaces left
        self.check_game_board()

    def player_add_chess(self, player):
        """when theres a mouse click
        near a unoccupied space, return that location's
        row col indices on player location matrix
        return True if player finished add a chess
        return False is player didn't click close enough"""
        # print(mouseX, mouseY)

        for r in range(self.N):
            for c in range(self.N):
                coord = self.coords_matrix[r][c]
                x = coord[0]
                y = coord[1]

                if (
                    abs(mouseX - x) <= self.DIST
                    and abs(mouseY - y) <= self.DIST
                    and self.chesses.is_empty(x, y)
                ):
                    self.add_chess_to_display(r, c, player)
                    return True
        return False

    def com_add_chess(self):
        """computer add a chess to the board"""
        # update info to computer
        self.computer.update(self.players_matrix, self.computer_chesses)
        # get chess indices pair
        pair = self.computer.add_chess()
        name = self.computer.get_name

        self.add_chess_to_display(pair[0], pair[1], name)
        self.computer_chesses += 1
        # update
        self.computer.update(self.players_matrix, self.computer_chesses)
        # check board for winner
        self.check_game_board()

    def print_players_matrix(self):
        """print player location
        for testing purpose"""
        for row in self.players_matrix:
            print(row)
        print()

    def add_player_loc(self, row, col, player_name):
        """add player loc to player locations matrix"""

        # add to player location
        if player_name == self.computer.get_name:
            self.players_matrix[row][col] = self.computer_target
        else:
            self.players_matrix[row][col] = self.player_target

    def check_game_board(self):
        """call game controller to check winner or tie"""
        if self.is_board_full():
            # if board is full
            # we have a tie
            self.gc.ties = True

        res = self.who_wins()
        if res == self.player_target:
            # self.print_players_matrix()
            self.gc.p1_wins = True
        if res == self.computer_target:
            # self.print_players_matrix()
            self.gc.p2_wins = True

    def is_board_full(self):
        """check if theres any space left"""
        # print("total chess: ",self.total_chesses)
        # if total chesses < row * row
        # board is not full
        if self.total_chesses < self.N * self.N:
            return False
        return True

    def who_wins(self):
        """check who wins based on player location
        and returns integer:
        1 -> player
        2 -> computer
        """
        # check if anyone has 5 or more
        winner = check_x_or_more(
            matrix=self.players_matrix, count=self.COUNT, empty_target=0
        )
        # print("winner: ", winner)
        return winner
