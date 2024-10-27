class Chess:
    """chess object"""

    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.id = player
        if self.id != "Computer":
            # black chess
            self.color = [0, 0, 0, 255]
        else:
            # white chess
            self.color = [255, 255, 255, 255]
        # radius of a chess
        self.radius = 30

    @property
    def get_chess_radius(self):
        """get chess's radius"""
        return self.radius

    @property
    def get_chess_value(self):
        """For testing purpose
        get chesses value representing the player"""
        if self.id == "Computer":
            return 2
        else:
            return 1

    def display(self):
        """display a chess"""
        fill(self.color[0], self.color[1], self.color[2], self.color[3])
        circle(self.x, self.y, self.radius)
