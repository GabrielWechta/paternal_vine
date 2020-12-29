from collections import deque
import interface


def print_map(map):
    for line in map:
        print(line)


def listToString(s):
    str1 = ""
    return (str1.join(s))


def balls_number(map):
    counter = 0
    for line in map:
        for char in line:
            if char != " ":
                counter += 1
    return counter


def get_color_dictionary(map):
    color_dictionary = {'G': 0, 'Y': 0, 'B': 0, 'R': 0}
    for line in map:
        for char in line:
            if char == ' ':
                continue
            color_dictionary[char] += 1

    return color_dictionary


def get_most_common_ball(map):
    color_dictionary = get_color_dictionary(map)
    ordered_colors = list(sorted(color_dictionary.items(), key=lambda item: item[1], reverse=True))
    for next_color in ordered_colors:
        yield next_color[0]


# >>>>> nowy kod dotyczący sygnałów tu sie zaczyna <<<<<

def create_the_signal_map(map):
    signal_map = [[0 for _ in range(7)] for _ in range(7)]
    # fill entire temporal_field with 1s
    temporal_field = [[1 for _ in range(9)] for _ in range(9)]

    # set 0 for every free cell in the table (i.e. no ball present)
    for y in range(7):
        for x in range(7):
            if map[y][x] == ' ':
                temporal_field[y + 1][x + 1] = 0

    # set cell in signal table so that the more surrounded ball is - the stronger is the signal to move it
    for y in range(1, 8):
        for x in range(1, 8):
            if temporal_field[y][x] >= 0:
                signal_map[y - 1][x - 1] = temporal_field[y][x + 1] + \
                                           temporal_field[y][x - 1] + \
                                           temporal_field[y - 1][x] + \
                                           temporal_field[y + 1][x]
            # for empty fields we also need to set a signal but it will be negative
            # else: signal_map[y - 1][x - 1] = -1 * (temporal_field[y][x + 1] + \
            #                                temporal_field[y][x - 1] + \
            #                                temporal_field[y - 1][x] + \
            #                                temporal_field[y + 1][x])
    return signal_map

    # ??? set 0 or decrease by 1 if the ball fits the pattern and is part of the 5 ball line ???
    # ??? which means do not take from here ???


# ??? set signal to 10 if the different color ball is part of the recongised 5 ball's line ???
# ??? which means do not take from here ???

# >>>>> nowy kod się konczy tu <<<<<

# >>>>> nowy kod dotyczący diagonali <<<<<

def create_diag_up(map):
    diag_up_map = [[] for _ in range(5)]

    # diag with 7 balls - copy ball colors from diag into the the horizon-vertical structure
    for x in range(7):
        diag_up_map[2].append(map[6 - x][x])

    # 2 x diag with 6 balls
    for x in range(6):
        diag_up_map[1].append(map[5 - x][x])
        diag_up_map[3].append(map[6 - x][x + 1])

    # 2 x diag with 5 balls
    for x in range(5):
        diag_up_map[0].append(map[4 - x][x])
        diag_up_map[4].append(map[6 - x][x + 2])

    print(diag_up_map)
    return diag_up_map


def create_diag_down(map):
    diag_down_map = [[] for _ in range(5)]

    # diag with 7 balls - copy ball colors from diag into the the horizon-vertical structure
    for x in range(7):
        diag_down_map[2].append(map[x][x])

    # 2 x diag with 6 balls
    for x in range(6):
        diag_down_map[1].append(map[x + 1][x])
        diag_down_map[3].append(map[x][x + 1])

    # 2 x diag with 5 balls
    for x in range(5):
        diag_down_map[0].append(map[x + 2][x])
        diag_down_map[4].append(map[x][x + 2])

    print(diag_down_map)
    return diag_down_map


def create_diag_down_map_orig_coordinates():
    diag_down_map_orig_coordinates = [[[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]],
                                      [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]],
                                      [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]],
                                      [[1, 0], [2, 1], [3, 2], [4, 3], [5, 4], [6, 5]],
                                      [[2, 0], [3, 1], [4, 2], [5, 3], [6, 4]]]
    return diag_down_map_orig_coordinates


def create_diag_down_reverse_map_orig_coordinates():
    diag_down_map_orig_coordinates = [[[4, 6], [3, 5], [2, 4], [1, 3], [0, 2]],
                                      [[5, 6], [4, 5], [3, 4], [2, 3], [1, 2], [0, 1]],
                                      [[6, 6], [5, 5], [4, 4], [3, 3], [2, 2], [1, 1], [0, 0]],
                                      [[6, 5], [5, 4], [4, 3], [3, 2], [2, 1], [1, 0]],
                                      [[6, 4], [5, 3], [4, 2], [3, 1], [2, 0]]]
    return diag_down_map_orig_coordinates


def create_diag_up_map_orig_coordinates():
    diag_up_map_orig_coordinates = [[[0, 4], [1, 3], [2, 2], [3, 1], [4, 0]],
                                    [[0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0]],
                                    [[0, 6], [1, 5], [2, 4], [3, 3], [4, 2], [5, 1], [6, 0]],
                                    [[1, 6], [2, 5], [3, 4], [4, 3], [5, 2], [6, 1]],
                                    [[2, 6], [3, 5], [4, 4], [5, 3], [6, 2]]]
    return diag_up_map_orig_coordinates


def create_diag_up_reverse_map_orig_coordinates():
    diag_up_map_orig_coordinates = [[[4, 0], [3, 1], [2, 2], [1, 3], [0, 4]],
                                    [[5, 0], [4, 1], [3, 2], [2, 3], [1, 4], [0, 5]],
                                    [[6, 0], [5, 1], [4, 2], [3, 3], [2, 4], [1, 5], [0, 6]],
                                    [[6, 1], [5, 2], [4, 3], [3, 4], [2, 5], [1, 6], ],
                                    [[6, 2], [5, 3], [4, 4], [3, 5], [2, 6], ]]
    return diag_up_map_orig_coordinates


#     # # diag with 7 balls - copy ball colors from diag into the the horizon-vertical structure
#     for x in range(6):
#         diag_up_map(x, 0) = map(x, x)
#
#     # 2 x diag with 6 balls
#     for x in range(5):
#         diag_up_map(x, 1) = map(x , x+1)
#         diag_up_map(x, 2) = map(x + 1, x)
#
#     # 2 x diag with 5 balls
#     for x in range(4):
#         diag_up_map(x, 3) = map(x, x+2)
#         diag_up_map(x, 4) = map(x + 2, x)


# >>>>> tu się konczy new code <<<<<

def replace_sames(pattern, color):
    local_pattern = list(pattern)

    for j, element in enumerate(pattern):
        if element == "SAME":
            local_pattern[j] = color
        else:
            local_pattern[j] = " "
    return local_pattern


# find balls of the same color as in the longest line but not from the line itself

def find_not_considered_ball(local_map, color):
    movable_balls = []
    for y, line in enumerate(local_map):
        for x, char in enumerate(line):
            if char == color:
                movable_balls.append([x, y, 0])
    print(movable_balls)
    return movable_balls


class queueNode:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def is_valid(row: int, col: int):
    return (row >= 0) and (row < 7) and (col >= 0) and (col < 7)


def bfs(mat, src_x: int, src_y: int, dest_x: int, dest_y: int) -> bool:
    src = queueNode(src_x, src_y)
    dest = queueNode(dest_x, dest_y)
    rowNum = [-1, 0, 0, 1]
    colNum = [0, -1, 1, 0]

    if mat[src.y][src.x] == " " or mat[dest.y][dest.x] != " ":
        print("Incorrect input to bfs.")
        return False

    visited = [[False for _ in range(7)] for _ in range(7)]
    visited[src.y][src.x] = True
    q = deque()
    q.append(src)
    while q:
        curr = q.popleft()
        if curr.x == dest.x and curr.y == dest.y:
            return True
        for i in range(4):
            row = curr.y + rowNum[i]
            col = curr.x + colNum[i]
            if is_valid(row, col) and mat[row][col] == " " and not visited[row][col]:
                visited[row][col] = True
                adjacent_cell = queueNode(col, row)
                q.append(adjacent_cell)
    return False


def try_to_move_ball(maze, balls_to_consider, x_target, y_target):
    for ball in balls_to_consider:
        if bfs(maze, ball[0], ball[1], x_target, y_target):
            return ball
    return None


def will_ball_reach_it(maze, x_src, y_src, x_tar, y_tar):
    if bfs(maze, x_src, y_src, x_tar, y_tar):
        return True
    else:
        return False


def rotate_matrix(mat):
    N = len(mat[0])
    # Consider all squares one by one
    for x in range(0, int(N / 2)):

        # Consider elements in group
        # of 4 in current square
        for y in range(x, N - x - 1):
            # store current cell in temp variable
            temp = mat[x][y]

            # move values from right to top
            mat[x][y] = mat[y][N - 1 - x]

            # move values from bottom to right
            mat[y][N - 1 - x] = mat[N - 1 - x][N - 1 - y]

            # move values from left to bottom
            mat[N - 1 - x][N - 1 - y] = mat[N - 1 - y][x]

            # assign temp to left
            mat[N - 1 - y][x] = temp


def mark_xes(local_map, pattern, index_x, index_y):
    for i, pattern_element in enumerate(pattern):
        if pattern_element != " ":
            local_map[index_y][index_x + i] = "X"


def mark_diag_down_xes(local_map, pattern, index_x, index_y):
    ddmoc = create_diag_down_map_orig_coordinates()
    line = ddmoc[index_y]
    for i, pattern_element in enumerate(pattern):
        if pattern_element != " ":
            x, y = line[i + index_x]
            local_map[y][x] = "X"


def mark_diag_up_xes(local_map, pattern, index_x, index_y):
    dumoc = create_diag_up_map_orig_coordinates()
    line = dumoc[index_y]
    for i, pattern_element in enumerate(pattern):
        if pattern_element != " ":
            x, y = line[i + index_x]
            local_map[y][x] = "X"


def add_signal(balls_to_consider, signal_map):
    for ball in balls_to_consider:
        ball[2] = signal_map[ball[1]][ball[0]]
    return balls_to_consider


def sort_balls_to_consider(balls_to_consider):
    print("wybrane kulki przed posortowaniem po sygnale")
    print_map(balls_to_consider)

    # balls_to_consider=sorted(balls_to_consider, key=[2],reverse=True) # tu się wywala

    balls_to_consider.sort(key=lambda row: row[2], reverse=True)

    print("wybrane kulki PO posortowaniu po sygnale")
    print_map(balls_to_consider)

    # input("chwila do namysłu"+'\n')

    return balls_to_consider


def replace_sames_and_diffs(pattern, same, diff):
    for i in range(len(pattern)):
        if pattern[i] == "SAME":
            pattern[i] = same
        if pattern[i] == "DIFF":
            pattern[i] = diff
    return pattern


def different_finder_and_signal_update(map, signal_map):
    pattern_tab = [
        ["SAME", "SAME", "SAME", "SAME", "DIFF"],
        ["SAME", "SAME", "SAME", "DIFF", "SAME"],
        ["SAME", "SAME", "DIFF", "SAME", "SAME"],
        ["SAME", "DIFF", "SAME", "SAME", "SAME"],
        ["DIFF", "SAME", "SAME", "SAME", "SAME"],
    ]

    rotated_map = [row[:] for row in map]
    rotate_matrix(rotated_map)

    for same in ["R", "G", "Y", "B"]:
        for diff in ["R", "G", "Y", "B"]:
            if same == diff:
                continue
            for pattern_template in pattern_tab:
                pattern = replace_sames_and_diffs(pattern_template.copy(), same, diff)
                pattern_str = listToString(pattern)

                # for local_map in [map, rotated(map)]:
                for y, line in enumerate(map):
                    line_str = listToString(line)
                    index = line_str.find(pattern_str)
                    if index != -1:
                        x = line_str.find(diff)
                        signal_map[y][x] += 10

                for y, line in enumerate(rotated_map):
                    line_str = listToString(line)
                    index = line_str.find(pattern_str)
                    if index != -1:
                        true_x = 6 - y
                        true_y = line_str.find(diff)
                        signal_map[true_y][true_x] += 10
    print_map(signal_map)
