import random
import math
from computer_module import *


class Computer:
    """a computer class"""

    def __init__(self):
        self.name = "Computer"

        # represent different chesses on players location matrix
        self.empty_target = 0
        self.player_target = 1
        self.computer_target = 2

        # default matrix size
        self.N = 0
        # players matrix
        self.players_matrix = []
        # indices of empty spaces of indices within players matrix
        self.empty_spaces = set()
        # how many chesses computer has put on the matrix
        self.computer_chesses = 0

    @property
    def get_name(self):
        """get computer name"""
        return self.name

    def update(self, players_matrix, computer_chesses):
        """update local player_matrix
        matrix size
        and empty spaces left
        """

        self.players_matrix = players_matrix
        if self.N == 0:
            self.N = len(players_matrix)

        # remove non-empty spaces from set empty spaces
        if self.empty_spaces is not None:
            for tup in self.empty_spaces:
                if self.players_matrix[tup[0]][tup[1]] != self.empty_target:
                    self.empty_spaces.remove(tup)

        # add empty spaces left to set empty spaces
        for row in range(self.N):
            for col in range(self.N):
                curr = players_matrix[row][col]
                # only want empty spaces
                if curr == self.empty_target:
                    self.empty_spaces.add(tuple([row, col]))
        self.computer_chesses = computer_chesses
        # print(self.empty_spaces)

    def rand_select_empty(self):
        """randomly place a computer chess to a empty space
        that is not on the edge
        return a tuple of indices row, col of the player matrix
        """

        # separate empty spaces at edge or not at edge
        edge_empty_spaces = []
        inner_empty_spaces = []
        for pair in list(self.empty_spaces):
            if 0 in pair or self.N - 1 in pair:
                edge_empty_spaces.append(pair)
            else:
                inner_empty_spaces.append(pair)

        # if there are empty spaces not at edge
        # avoid choosing random select space at edge
        if len(inner_empty_spaces) > 0:
            choice = random.choice(inner_empty_spaces)
        else:
            choice = random.choice(edge_empty_spaces)
        return choice

    def add_chess(self):
        """add a chess to player matrix
        return a tuple of indices row, col of the player matrix
        """
        # 1. check if theres any computer chesses
        # print("computer chesses ", self.computer_chesses)
        if self.computer_chesses == 0:
            # if theres non ->random select an empty indices
            return self.rand_select_empty()

        # 2. stop players with 3 or more
        # 2.1 get players longest paths
        paths = longest_path(self.players_matrix, self.player_target)
        # print(paths)
        # tuple[0]: max length of current path
        # tuple[1]: direction in horizontal, vertical, diagonal or anti-diagonal of current path
        # tuple[2]: a list of matrix[r][c] indices of the longest path
        for path in paths:
            if path[0] >= 3:
                res = check_path(
                    matrix=self.players_matrix,
                    direction=path[1],
                    path=path[2],
                    empty_spaces=self.empty_spaces,
                )
                # ignore invalid path
                if res is False or res is None:
                    continue

                return res

        # 3. get all computer paths
        paths = longest_path(self.players_matrix, self.computer_target)
        for path in paths:
            if path[0] >= 1:
                res = check_path(
                    matrix=self.players_matrix,
                    direction=path[1],
                    path=path[2],
                    empty_spaces=self.empty_spaces,
                )
                if res is False or res is None:
                    continue

                return res

        # no other choices
        return self.rand_select_empty()
