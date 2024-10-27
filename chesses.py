from chess import Chess


class Chesses:
    """all chesses object"""

    def __init__(self, WIDTH, HEIGHT, MARGIN, SPACING, game_controller):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.MARGIN = MARGIN
        self.spacing = SPACING
        self.start = MARGIN

        self.gc = game_controller

        # stores all chesses' playable locations in 15 * 15 matrix
        self.coords_matrix = []

        # stores all chess's coordinates in tuple
        # to determine which (x, y) is empty
        self.coord_set = set()

        # matrix size
        self.N = int((self.WIDTH - 2 * self.MARGIN) / self.spacing + 1)

        # now have a 15 * 15 matrix stores all chesses object for display purpose
        self.chesses_display_matrix = [
            [None for col in range(self.N)] for row in range(self.N)
        ]

        for i in range(self.start, self.WIDTH - self.MARGIN + 1, self.spacing):
            row = []
            for j in range(self.start, self.WIDTH - self.MARGIN + 1, self.spacing):
                # print(j, i)
                row.append([j, i])
            self.coords_matrix.append(row)

        # print(self.coords_matrix[0])

        # for ------------ testing
        self.all = []
        for coord in self.coords_matrix:
            self.all.append(Chess(coord[0], coord[1], "p1"))

    def add_chess(self, row, col, player):
        """Given row and col indices on the players location matrix
        add one chess to the all chesses display matrix"""
        # print(self.all_chesses)

        # convert row col indices to coordinates
        x = self.coords_matrix[row][col][0]
        y = self.coords_matrix[row][col][1]

        # avoid duplicates
        if self.is_empty(x, y):
            # create a new chess base on player
            a_chess = Chess(x, y, player)
            # add the chess instance to all chesses matrix
            self.chesses_display_matrix[row][col] = a_chess

            # add such coordinates to coordinates set
            self.coord_set.add((x, y))
            # print(player, "add chess to:", x, y)

    def display(self):
        """display all chesses"""
        for row in self.chesses_display_matrix:
            for chess in row:
                if chess is not None:
                    chess.display()

    def is_empty(self, x, y):
        """given a x, y coordinates, check where is empty or occupied
        """
        if (x, y) not in self.coord_set:
            return True
        else:
            return False