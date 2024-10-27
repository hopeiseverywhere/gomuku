import os


class GameController:
    """game controller"""

    def __init__(self, p1, p2, WIDTH, HEIGHT, MARGIN, LINE_SPACE):
        # player name p1 vs computer name p2
        self.p1 = p1
        self.p2 = p2
        self.p1_wins = False
        self.p2_wins = False
        self.ties = False
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.MARGIN = MARGIN
        self.LINE_SPACE = LINE_SPACE

        self.text_size = 100
        self.text_size_small = 20
        # black
        self.text_color = [0, 0, 0, 255]

        self.DIST = 20

    def game_over(self):
        """check if there's end the of the game"""
        if self.winner() or self.ties:
            return True
        else:
            return False

    def record_result(self, winner_name, cwd=os.getcwd()):
        """record winner's name to a txt file"""
        # make sure to get the current directory
        f_path = cwd + "/txt/scores.txt"
        try:
            with open(f_path, "r") as file:
                lines = file.readlines()
                found = False

                for i, line in enumerate(lines):
                    # make sure we are not dealing empty file
                    if len(line) >= 1:
                        name, score = line.strip().split()

                        if name == winner_name:
                            lines[i] = "{} {}\n".format(winner_name, int(score) + 1)
                            found = True
                            break
                if not found:
                    lines.append("{} {}\n".format(winner_name, 1))
                # sort descending by wins
                lines = sorted(
                    lines,
                    key=lambda item: int(item.split()[1])
                    if len(item.split()) > 1
                    else 0,
                    reverse=True,
                )
            with open(f_path, "w") as file:
                file.writelines(lines)
        except IOError:
            # if the file does not exist, create a new one with the winner's entry
            with open(f_path, "w") as file:
                file.write("{} {}\n".format(winner_name, 1))

    def winner(self):
        """check if there is a winner"""
        if not self.p1_wins and not self.p2_wins:
            return False
        if self.p1_wins or self.p2_wins:
            return True

    def update_winner(self):
        """if there is a winner update the game"""
        textAlign(CENTER)
        fill(
            self.text_color[0],
            self.text_color[1],
            self.text_color[2],
            self.text_color[3],
        )

        if self.winner():
            if self.p1_wins is True:
                # txt = self.p1 + " wins"
                txt = self.p1 + " Wins!"
                msg = "Winner name logged to record"
                self.display_msg(msg)

            else:
                txt = self.p2 + " wins"
            textSize(self.text_size)
            text(txt, self.WIDTH / 2, self.WIDTH + self.MARGIN / 3)

    def update_ties(self):
        """if there is no space in the board"""
        textSize(self.text_size)
        textAlign(CENTER)
        fill(
            self.text_color[0],
            self.text_color[1],
            self.text_color[2],
            self.text_color[3],
        )

        if self.ties:
            txt = "NO SPACE!"
            text(txt, self.WIDTH / 2, self.WIDTH + self.MARGIN / 2)

    def update_player_name(self, name):
        """update player name"""
        self.p1 = name

    def display_game_start(self):
        """display instructions and welcome messages"""
        fill(
            self.text_color[0],
            self.text_color[1],
            self.text_color[2],
            self.text_color[3],
        )
        textSize(self.text_size_small)
        textAlign(CENTER)

        msg = "Welcome to Gomuku \n Player (Black) V.S. Computer (White) \n Click Black Bar To START"
        text(msg, self.WIDTH / 2, self.WIDTH - self.MARGIN / 3)

    def display_button(self):
        """display start button"""
        rect(
            self.WIDTH / 2 - self.LINE_SPACE,
            self.WIDTH + self.MARGIN / 2,
            self.LINE_SPACE * 2,
            20,
        )

    def button_clicked(self):
        """check if user click the button, if clicked return False"""
        x = self.WIDTH / 2 - self.LINE_SPACE
        y = self.WIDTH + self.MARGIN / 2
        if abs(mouseX - x) <= self.DIST and abs(mouseY - y) <= self.DIST:
            return False

    def display_log_winner(self):
        """ask user to enter a name when player wins"""
        # print(msg1)
        textSize(self.text_size_small)
        textAlign(CENTER)
        msg = "Player Wins! \n Please enter player name (End by ENTER)"
        text(msg, self.WIDTH / 2, self.WIDTH - self.MARGIN / 3)
        text("-----", self.WIDTH / 2, self.WIDTH + self.MARGIN * 0.8)

    def check_name(self, name):
        """check where user's name input is valid
        Args:
            name (string)
        Returns tuple:
            tuple[0] (boolean): True or False
            tuple[1] (string): Capitalized name
        """
        # print(list(name))

        # ignore any non-ASCII part
        res = ""
        for el in list(name):
            if len(el) == 1 and el.isalpha():
                res += el

        if res.isalpha() and len(res) >= 2:
            name = res.lower()
            name = res.capitalize()

            return True, name

        return False, name

    def display_msg(self, msg):
        """display a msg at the bottom of the window"""
        textSize(self.text_size_small)
        textAlign(CENTER)
        text(msg, self.WIDTH / 2, self.WIDTH + self.MARGIN / 1.5)

    # def display_player_name(self):
    #     """display player name at the top left of the window"""
    #     textSize(self.text_size_small)
    #     textAlign(LEFT)
    #     fill(
    #         self.text_color[0],
    #         self.text_color[1],
    #         self.text_color[2],
    #         self.text_color[3],
    #     )
    #     msg = "Player: "
    #     text(msg + self.p1, self.MARGIN / 10, self.MARGIN / 4)
