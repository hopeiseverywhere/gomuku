def check_x_or_more(matrix, count, empty_target=0):
    """check if anyone has count chesses or more in a row or col
    or in diagonal
    Args:
        matrix (int matrix): a N by N matrix where 0 == empty space, 1 == player, 2 == computer
        count (int): the value in a row we want to check
        empty_target (int): default value 0

    Returns integer:
        0: there are count * 0s (empty space) in a row/col/diagonal
        1: there are count * 1s (player) in a row/col/diagonal
        2: there are count * 2s (computer) in a row/col/diagonal
    """

    N = len(matrix)

    # check row
    for row in matrix:
        for i in range(0, N - count + 1):
            match_found = True
            curr_element = row[i]
            for j in range(1, count):
                if row[i + j] != curr_element or curr_element == empty_target:
                    match_found = False
                    break
            if match_found:
                # print("row")
                return curr_element

    # check col
    # matrix[i][j] == matrix[i+1][j] == matrix[i+2][j]
    for col in range(N):
        for row in range(0, N - count + 1):
            match_found = True
            current_element = matrix[row][col]
            for i in range(1, count):
                if (
                    matrix[row + i][col] != current_element
                    or current_element == empty_target
                ):
                    match_found = False
                    break
            if match_found:
                # print("col")
                return current_element

    # check main diagonal: top left to bottom right
    # matrix[i][j] == matrix[i+1][j+1] == matrix[i+2][j+2]
    for row in range(0, N - count + 1):
        for col in range(0, N - count + 1):
            match_found = True
            current_element = matrix[row][col]
            for i in range(1, count):
                if (
                    matrix[row + i][col + i] != current_element
                    or current_element == empty_target
                ):
                    match_found = False
                    break
            if match_found:
                # print("main diag")
                return current_element

    # check anti diagonal: lower left to upper right
    # matrix[row][col]==matrix[row+1][col-1]==matrix[row+2][col-2]
    for row in range(0, N - count + 1):
        for col in range(N - 1, count - 2, -1):
            match_found = True
            current_element = matrix[row][col]
            for i in range(1, count):
                if (
                    matrix[row + i][col - i] != current_element
                    or current_element == empty_target
                ):
                    match_found = False
                    break
            if match_found:
                # print("anti")
                return current_element
    # default return 0
    return 0


def dfs(row, col, direction, path, matrix, target):
    """a helper function for dfs on a players matrix

    Args:
        row (int): matrix[row][col]
        col (int): matrix[row][col]
        direction (string): in "horizontal", "vertical", "main-diagonal" or "anti-diagonal"
        path (list of tuples): a list stores (row, col)
        matrix (int matrix): a N by N matrix where 0 == empty space, 1 == player, 2 == computer
        target (int): the target (0, 1 or 2) we want to check

    Returns: void
    """
    N = len(matrix)
    # make sure the current call is within matrix range
    if row < 0 or row >= N or col < 0 or col >= N or matrix[row][col] != target:
        return None

    matrix[row][col] = -1
    path.append((row, col))

    if direction == "horizontal":
        dfs(row, col + 1, direction, path, matrix, target)
    elif direction == "vertical":
        dfs(row + 1, col, direction, path, matrix, target)
    elif direction == "main-diagonal":
        dfs(row + 1, col + 1, direction, path, matrix, target)
    elif direction == "anti-diagonal":
        dfs(row - 1, col + 1, direction, path, matrix, target)


def longest_path(matrix, target):
    """given a player locations matrix
    return a descending list of longest paths of target (0, 1 or 2) using dfs

    Args:
        matrix (int matrix): a N by N matrix where 0 == empty space, 1 == player, 2 == computer
        target (int): the target (0, 1 or 2) we want to check

    Returns a list of tuple:
        tuple[0]: max length of current path
        tuple[1]: direction in horizontal, vertical, diagonal or anti-diagonal of current path
        tuple[2]: a list of matrix[r][c] indices of the longest path
    """
    N = len(matrix)
    # make 4 deep copies for 4 different directions
    hor_matrix_copy = [row[:] for row in matrix]
    ver_matrix_copy = [row[:] for row in matrix]

    diag_matrix_copy = [row[:] for row in matrix]
    anti_diag_matrix_copy = [row[:] for row in matrix]

    # ignore only 1 chess
    length = 1
    max_length = 2
    max_path = []
    max_direction = ""
    # stores a list of tuple that contains direction and paths
    paths = []

    # note the loop from left to right, top to bottom
    # only works for the
    # top left corner to the bottom right corner: main diagonal
    for r in range(N):
        for c in range(N):
            if matrix[r][c] == target:
                # three different curr path list for three different directions
                hor_path = []
                ver_path = []
                diag_path = []

                dfs(r, c, "horizontal", hor_path, hor_matrix_copy, target)
                # if len of curr path > max_length, update
                if len(hor_path) >= length:
                    max_length = len(hor_path)
                    max_path = hor_path
                    max_direction = "horizontal"
                    paths.append(tuple([max_length, max_direction, max_path]))

                dfs(r, c, "vertical", ver_path, ver_matrix_copy, target)
                if len(ver_path) >= length:
                    max_length = len(ver_path)
                    max_path = ver_path
                    max_direction = "vertical"
                    paths.append(tuple([max_length, max_direction, max_path]))

                dfs(r, c, "main-diagonal", diag_path, diag_matrix_copy, target)
                if len(diag_path) >= length:
                    max_length = len(diag_path)
                    max_path = diag_path
                    max_direction = "main-diagonal"
                    paths.append(tuple([max_length, max_direction, max_path]))
    # check the top right to the bottom left corner diagonal
    # from bottom to up, left to right
    for r in range(N - 1, -1, -1):
        for c in range(N):
            if matrix[r][c] == target:
                anti_diag_path = []
                dfs(
                    r, c, "anti-diagonal", anti_diag_path, anti_diag_matrix_copy, target
                )
                if len(anti_diag_path) >= length:
                    max_length = len(anti_diag_path)
                    max_path = anti_diag_path
                    max_direction = "anti-diagonal"
                    paths.append(tuple([max_length, max_direction, max_path]))

    # sort the returning list is descending order base on max_length
    # print(max_path)
    paths = sorted(paths, key=lambda x: x[0], reverse=True)
    return paths


def check_path(matrix, direction, path, empty_spaces):
    """for a given path of chesses
    1. check if both ends' next one is empty
    2. check if one end's next one is empty but the other end's next one is not
    3. if both ends' next one are empty, choose the end is further to the edge
    Args:
        matrix (int matrix): a N by N matrix where 0 == empty space, 1 == player, 2 == computer
        direction (string): in "horizontal", "vertical", "main-diagonal" or "anti-diagonal"
        path (list of tuples): a list stores (row, col)
        empty_spaces (set of tuples): a set of empty (row, col)

    Return:
        False: both ends' next one of this path is occupied or invalid
    """
    N = len(matrix)
    bound = N - 1
    if direction == "horizontal":
        # get the min col and max col of the path
        row = path[0][0]
        min_c = path[0][1]
        max_c = path[-1][1]

        # if both ends' next one is occupied -> invalid path
        if not is_indices_empty(
            (row, min_c - 1), empty_spaces
        ) and not is_indices_empty((row, max_c + 1), empty_spaces):
            return False

        # if left of head is not empty but right to tail is empty
        if not is_indices_empty((row, min_c - 1), empty_spaces) and is_indices_empty(
            (row, max_c + 1), empty_spaces
        ):
            return row, max_c + 1
        # if left of head is empty but right to tail is not empty
        elif is_indices_empty((row, min_c - 1), empty_spaces) and not is_indices_empty(
            (row, max_c + 1), empty_spaces
        ):
            return row, min_c - 1

        # if both ends are in bound, check witch end is further to bound
        # i.e see if min c is closer to 0 or max c is closer to 14
        if min_c - 0 >= bound - max_c and is_indices_empty(
            (row, min_c - 1), empty_spaces
        ):
            return row, min_c - 1
        elif min_c - 0 < bound - max_c and is_indices_empty(
            (row, max_c + 1), empty_spaces
        ):
            return row, max_c + 1

    elif direction == "vertical":
        min_r = path[0][0]
        max_r = path[-1][0]
        col = path[0][1]
        # if both ends' next one is occupied -> invalid path
        if not is_indices_empty(
            (min_r - 1, col), empty_spaces
        ) and not is_indices_empty((max_r + 1, col), empty_spaces):
            return False

        # if top of the head is not empty and bottom of the tail is empty
        if not is_indices_empty((min_r - 1, col), empty_spaces) and is_indices_empty(
            (max_r + 1, col), empty_spaces
        ):
            return max_r + 1, col

        # if top of the head is empty and bottom of the tail is not empty
        elif is_indices_empty((min_r - 1, col), empty_spaces) and not is_indices_empty(
            (max_r + 1, col), empty_spaces
        ):
            return min_r - 1, col

        # if both ends are in bound, check witch end is further to bound
        # i.e. see if min r is closer to 0 or max r is closer to 14
        if min_r - 0 >= bound - max_r and is_indices_empty(
            (min_r - 1, col), empty_spaces
        ):
            return min_r - 1, col
        elif min_r - 0 < bound - max_r and is_indices_empty(
            (max_r + 1, col), empty_spaces
        ):
            return max_r + 1, col

    # check for 2 diagonals
    head_r = path[0][0]
    head_c = path[0][1]
    tail_r = path[-1][0]
    tail_c = path[-1][1]

    # check which end is further away from edge of the matrix
    # if head: return -1
    # if tail: return 1
    res = diag_distance_to_edge(path[0], path[-1], direction, N)

    if direction == "main-diagonal":
        # if both ends' next slot is not empty -> invalid path
        if not is_indices_empty(
            (head_r - 1, head_c - 1), empty_spaces
        ) and not is_indices_empty((tail_r + 1, tail_c + 1), empty_spaces):
            return False

        # if top left of the head is not empty, but lower right of tail is empty
        if not is_indices_empty(
            (head_r - 1, head_c - 1), empty_spaces
        ) and is_indices_empty((tail_r + 1, tail_c + 1), empty_spaces):
            return tail_r + 1, tail_c + 1
        # if top left of the head is empty, but lower right of tail is not empty
        if is_indices_empty(
            (head_r - 1, head_c - 1), empty_spaces
        ) and not is_indices_empty((tail_r + 1, tail_c + 1), empty_spaces):
            return head_r - 1, head_c - 1

        # check which end is further away from edge of the matrix
        # head is further, and upper left of the head is empty
        if res == -1 and is_indices_empty((head_r - 1, head_c - 1), empty_spaces):
            return head_r - 1, head_c - 1
        # tail is further, and lower right of the tail is empty
        if res == 1 and is_indices_empty((tail_r + 1, tail_c + 1), empty_spaces):
            return tail_r + 1, tail_c + 1

    elif direction == "anti-diagonal":
        # (note the head is lower left in this case)
        # if both ends' next slot is not empty -> invalid path
        # head_r + 1, head_c - 1
        # tail_r - 1, tail_c + 1
        if not is_indices_empty(
            (head_r + 1, head_c - 1), empty_spaces
        ) and not is_indices_empty((tail_r - 1, tail_c + 1), empty_spaces):
            return False

        # if lower left of head is not empty and upper right of the tail is empty
        if not is_indices_empty(
            (head_r + 1, head_c - 1), empty_spaces
        ) and is_indices_empty((tail_r - 1, tail_c + 1), empty_spaces):
            return tail_r - 1, tail_c + 1
        # if lower left of head is empty and upper right of the tail is not empty
        if is_indices_empty(
            (head_r + 1, head_c - 1), empty_spaces
        ) and not is_indices_empty((tail_r - 1, tail_c + 1), empty_spaces):
            return head_r + 1, head_c - 1

        # check which end is further away from edge of the matrix
        # head is further, and lower left of the head is empty
        if res == -1 and is_indices_empty((head_r + 1, head_c - 1), empty_spaces):
            return head_r + 1, head_c - 1
        # tail is further, and upper right of the tail is empty
        if res == 1 and is_indices_empty((tail_r - 1, tail_c + 1), empty_spaces):
            return tail_r - 1, tail_c + 1


def is_indices_empty(pair, empty_spaces):
    """check if a pair of indices (row, col) are at empty space or not
    Args:
        pair (tuple): (row, col)

        empty_spaces (set of tuples): a set of empty (row, col)

    Returns:
        True: a pair of indices is at empty spaces
        False: pair of indices is not at empty spaces
    """
    if pair in empty_spaces:
        return True
    return False


def diag_distance_to_edge(head, tail, direction, N):
    """given a path on a main (top left to bottom right) diagonal
    or a path on a anti (lower left to top right) diagonal
    (note the head is lower left in this case)

    check whether the head or the tail of the path is further from the edge

    Args:
        head (tuple): tuple (row, col)
        tail (tuple): tuple (row, col)
        direction (string): "main-diagonal" or "anti-diagonal"
        N (int): size of the matrix

    Returns:
        integer:    if head: return -1
                    if tail: return 1
    """
    head_to_edge = -1
    tail_to_edge = -1
    head_lis = list(head)
    tail_lis = list(tail)

    if direction == "main-diagonal":
        while head_lis[0] >= 0 and head_lis[1] >= 0:
            head_lis[0] -= 1
            head_lis[1] -= 1
            head_to_edge += 1

        while tail_lis[0] < N and tail_lis[1] < N:
            tail_lis[0] += 1
            tail_lis[1] += 1
            tail_to_edge += 1
    if direction == "anti-diagonal":
        # head_r + 1, head_c -1
        # tail_r - 1, tail_c + 1
        while head_lis[0] < N and head_lis[1] > 0:
            head_lis[0] += 1
            head_lis[1] -= 1
            head_to_edge += 1

        while tail_lis[0] > 0 and tail_lis[1] < N:
            tail_lis[0] -= 1
            tail_lis[1] += 1
            tail_to_edge += 1
    # print(head_to_edge, tail_to_edge)
    if head_to_edge > tail_to_edge:
        return -1

    return 1
