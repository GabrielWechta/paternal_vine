from functions import *

class SolutionsHolder:
    def __init__(self):
        self.red = [None]
        self.green = [None]
        self.blue = [None]
        self.yellow = [None]

    def save_solution(self, color: str, is_ending: bool, pattern_length: int, ball_x: int, ball_y: int, hole_x: int,
                      hole_y: int):
        if color == "R" and len(self.red) == 0:
            self.red = [is_ending, pattern_length, ball_x, ball_y, hole_x, hole_y]
        if color == "G" and len(self.green) == 0:
            self.green = [is_ending, pattern_length, ball_x, ball_y, hole_x, hole_y]
        if color == "B" and len(self.blue) == 0:
            self.blue = [is_ending, pattern_length, ball_x, ball_y, hole_x, hole_y]
        if color == "Y" and len(self.yellow) == 0:
            self.yellow = [is_ending, pattern_length, ball_x, ball_y, hole_x, hole_y]

    def show_best_solutions(self):
        for solution in self.__dict__:
            print(solution)

    def decide(self, map, signal_map):
        sorted_solutions = sorted(self.__dict__, key=lambda l: l[1], reverse=True)
        ending_solutions = [solution if solution[0] is True and not None else None for solution in sorted_solutions]
        for ending in ending_solutions:
            if ending is not None:
                return ending[2], ending[3], ending[4], ending[5]

        """ Signal map part """
        balls_by_signal = []
        for y, _ in enumerate(signal_map):
            for x, _ in enumerate(signal_map):
                balls_by_signal.append([signal_map[y][x], x, y])
        sorted_balls_by_signal = sorted(balls_by_signal, key=lambda l: l[0], reverse=True)

        for ball in sorted_balls_by_signal:
            ball_x, ball_y, ball_color = ball[1], ball[2], map[ball[2]][ball[1]]
            if ball_color == "R":
                hole_x, hole_y = self.red[4], self.red[5]
                if bfs(map, ball_x, ball_y, hole_x, hole_y):
                    return ball_x, ball_y, hole_x, hole_y
            if ball_color == "G":
                hole_x, hole_y = self.green[4], self.green[5]
                if bfs(map, ball_x, ball_y, hole_x, hole_y):
                    return ball_x, ball_y, hole_x, hole_y
            if ball_color == "B":
                hole_x, hole_y = self.blue[4], self.blue[5]
                if bfs(map, ball_x, ball_y, hole_x, hole_y):
                    return ball_x, ball_y, hole_x, hole_y
            if ball_color == "Y":
                hole_x, hole_y = self.yellow[4], self.yellow[5]
                if bfs(map, ball_x, ball_y, hole_x, hole_y):
                    return ball_x, ball_y, hole_x, hole_y
        print("SOMETHING WENT WRONG in solutionHolder.decide")


def find_pattern(map):
    pattern_tab = [["SAME", "SAME", "SAME", "SAME", "EMPTY", "SAME", "SAME"],  # 6 in a row, 5 SAME
                   ["SAME", "SAME", "SAME", "EMPTY", "SAME", "SAME", "SAME"],
                   ["SAME", "SAME", "EMPTY", "SAME", "SAME", "SAME", "SAME"],

                   ["SAME", "SAME", "SAME", "SAME", "EMPTY", "SAME"],  # 6 in a row 5 SAME
                   ["SAME", "SAME", "SAME", "EMPTY", "SAME", "SAME"],
                   ["SAME", "SAME", "EMPTY", "SAME", "SAME", "SAME"],
                   ["SAME", "EMPTY", "SAME", "SAME", "SAME", "SAME"],
                   ["EMPTY", "SAME", "SAME", "SAME", "SAME", "SAME"],

                   ["SAME", "SAME", "SAME", "SAME", "EMPTY"],  # 5 in a row 4 SAME
                   ["SAME", "SAME", "SAME", "EMPTY", "SAME"],
                   ["SAME", "SAME", "EMPTY", "SAME", "SAME"],
                   ["SAME", "EMPTY", "SAME", "SAME", "SAME"],
                   ["EMPTY", "SAME", "SAME", "SAME", "SAME"],

                   ["SAME", "SAME", "SAME", "EMPTY", "EMPTY"],  # 5 in a row 3 SAME
                   ["SAME", "SAME", "EMPTY", "SAME", "EMPTY"],
                   ["SAME", "EMPTY", "SAME", "SAME", "EMPTY"],
                   ["SAME", "EMPTY", "SAME", "EMPTY", "SAME"],
                   ["SAME", "SAME", "EMPTY", "EMPTY", "SAME"],
                   ["EMPTY", "SAME", "SAME", "SAME", "EMPTY"],  # risky

                   ["SAME", "SAME", "EMPTY", "EMPTY", "EMPTY"],  # 2 SAME
                   ["SAME", "EMPTY", "SAME", "EMPTY", "EMPTY"],
                   ["SAME", "EMPTY", "EMPTY", "SAME", "EMPTY"],
                   ["SAME", "EMPTY", "EMPTY", "EMPTY", "SAME"],
                   ["EMPTY", "SAME", "EMPTY", "SAME", "EMPTY"],
                   ["EMPTY", "EMPTY", "SAME", "SAME", "EMPTY"],
                   ["EMPTY", "EMPTY", "EMPTY", "SAME", "SAME"],

                   ["SAME", "SAME", "SAME", "EMPTY"],  # 3 SAME
                   ["SAME", "SAME", "EMPTY", "SAME"],

                   ["SAME", "SAME", "EMPTY", "EMPTY"],  # 2 SAME
                   ["SAME", "EMPTY", "EMPTY", "SAME"],
                   ["SAME", "EMPTY", "SAME", "EMPTY"],

                   ["SAME", "SAME", "EMPTY"],
                   ["SAME", "EMPTY", "SAME"],
                   ["SAME", "EMPTY"],
                   ["EMPTY"]
                   ]

    # create the signal map every time when new map is received from the mobile screen

    signal_map = create_the_signal_map(map)
    different_finder_and_signal_update(map, signal_map)

    solutions_holder = SolutionsHolder()

    for pattern in pattern_tab:
        """The original pattern_tab is replaced by new one. No need to worry, every time when find_pattern is called it 
        is initialized. """
        for color in get_most_common_ball(map):

            changed_pattern = replace_sames(pattern, color)

            rotated_map = [row[:] for row in map]
            print("Considering pattern: ", changed_pattern)
            pattern_str = listToString(changed_pattern)

            # JW diag down handling
            # trzeba jeszcze raz obr diag down

            print("Teraz diag down': mapa nie powinna byc rotowana")
            print_map(rotated_map)

            diag_down_map = create_diag_down(rotated_map)
            diag_down_map_orig_coordinates = create_diag_down_map_orig_coordinates()

            for y, line in enumerate(diag_down_map):
                line_str = listToString(line)
                index = line_str.find(pattern_str)
                if index != -1:
                    local_map = [row[:] for row in rotated_map]  # really makes COPY
                    add_to_x = pattern_str.find(" ")
                    print(index + add_to_x, y, sep=":")

                    mark_diag_down_xes(local_map, changed_pattern, index, y)

                    balls_to_consider = find_not_considered_ball(local_map, color)

                    # JW wsp x and y m

                    new_x = diag_down_map_orig_coordinates[y][index + add_to_x][0]
                    new_y = diag_down_map_orig_coordinates[y][index + add_to_x][1]

                    print(diag_down_map_orig_coordinates)
                    print(balls_to_consider)

                    # tutaj posortowac balls to consider po signal
                    balls_to_consider = add_signal(balls_to_consider, signal_map)
                    balls_to_consider = sort_balls_to_consider(balls_to_consider)

                    ball_found = try_to_move_ball(map, balls_to_consider, new_x, new_y)
                    if ball_found:
                        print("Ball found.")
                        print("Adding to solutions: ", pattern)
                        solutions_holder.save_solution(color, True if pattern.count("SAME") >= 4 else False,
                                                       len(pattern),
                                                       ball_found[0], ball_found[1], new_x,
                                                       new_y)
                    else:
                        print("Ball not found.")

            print("nie znalazłem pattern w diag_down")

            # JW diag up handling
            # trzeba jeszcze raz obr diag up

            print("Teraz diag up': mapa powinna byc nierotowana ")
            print_map(rotated_map)

            diag_up_map = create_diag_up(rotated_map)
            diag_up_map_orig_coordinates = create_diag_up_map_orig_coordinates()

            for y, line in enumerate(diag_up_map):
                line_str = listToString(line)
                index = line_str.find(pattern_str)
                if index != -1:
                    local_map = [row[:] for row in rotated_map]  # really makes COPY
                    add_to_x = pattern_str.find(" ")
                    print(index + add_to_x, y, sep=":")

                    mark_diag_up_xes(local_map, changed_pattern, index, y)

                    balls_to_consider = find_not_considered_ball(local_map, color)

                    # JW wsp x and y m

                    new_x = diag_up_map_orig_coordinates[y][index + add_to_x][0]
                    new_y = diag_up_map_orig_coordinates[y][index + add_to_x][1]

                    print(diag_up_map_orig_coordinates)
                    print(balls_to_consider)

                    # tutaj posortowac balls to consider po signal
                    balls_to_consider = add_signal(balls_to_consider, signal_map)
                    balls_to_consider = sort_balls_to_consider(balls_to_consider)

                    ball_found = try_to_move_ball(map, balls_to_consider, new_x, new_y)
                    if ball_found:
                        print("Ball found.")
                        print("Adding to solutions: ", pattern)
                        solutions_holder.save_solution(color, True if pattern.count("SAME") >= 4 else False,
                                                       len(pattern),
                                                       ball_found[0], ball_found[1], new_x,
                                                       new_y)
                    else:
                        print("Ball not found.")

            print("nie znalazłem pattern w diag_up")

            rotated_map = [row[:] for row in map]
            print("Considering pattern: ", changed_pattern)
            pattern_str = listToString(changed_pattern)
            # normal map part
            print("Normal map:")
            print_map(map)
            for y, line in enumerate(map):
                line_str = listToString(line)
                index = line_str.find(pattern_str)
                if index != -1:
                    local_map = [row[:] for row in map]  # really makes COPY
                    add_to_x = pattern_str.find(" ")
                    print(index + add_to_x, y, sep=":")
                    mark_xes(local_map, changed_pattern, index, y)
                    balls_to_consider = find_not_considered_ball(local_map, color)
                    new_x = index + add_to_x
                    new_y = y

                    # tutaj posortowac balls to consider po signal
                    balls_to_consider = add_signal(balls_to_consider, signal_map)
                    balls_to_consider = sort_balls_to_consider(balls_to_consider)

                    ball_found = try_to_move_ball(map, balls_to_consider, new_x, new_y)
                    if ball_found:
                        print("Ball found.")
                        print("Adding to solutions: ", pattern)
                        solutions_holder.save_solution(color, True if pattern.count("SAME") >= 4 else False,
                                                       len(pattern),
                                                       ball_found[0], ball_found[1], new_x,
                                                       new_y)
                    else:
                        print("Ball not found.")

            print("nie znalazłem w normalnej")

            # JW rotated map part 90' antyclockwise
            # trzeba pomieszać z indeksami
            rotate_matrix(rotated_map)
            print("Rotated by 90': ")
            print_map(rotated_map)
            for y, line in enumerate(rotated_map):
                line_str = listToString(line)
                index = line_str.find(pattern_str)
                if index != -1:
                    local_map = [row[:] for row in rotated_map]  # really makes COPY
                    add_to_x = pattern_str.find(" ")
                    print(index + add_to_x, y, sep=":")
                    mark_xes(local_map, changed_pattern, index, y)
                    balls_to_consider = find_not_considered_ball(local_map, color)

                    # sort the balls depending on the signal strength of each ball

                    for point in balls_to_consider:
                        tmp_x = point[0]
                        tmp_y = point[1]
                        point[0] = 6 - tmp_y
                        point[1] = tmp_x
                        # JW
                    new_x = 6 - y
                    new_y = index + add_to_x

                    # tutaj posortowac balls to consider po signal
                    balls_to_consider = add_signal(balls_to_consider, signal_map)
                    balls_to_consider = sort_balls_to_consider(balls_to_consider)

                    ball_found = try_to_move_ball(map, balls_to_consider, new_x, new_y)
                    if ball_found:
                        print("Ball found.")
                        print("Adding to solutions: ", pattern)
                        solutions_holder.save_solution(color, True if pattern.count("SAME") >= 4 else False,
                                                       len(pattern),
                                                       ball_found[0], ball_found[1], new_x,
                                                       new_y)
                    else:
                        print("Ball not found.")

            print("nie znalazłem pattern w -90'")

            # JW rotated map part 180' antyclockwise
            # trzeba pomieszać z indeksami
            rotate_matrix(rotated_map)
            print("Rotated by 180': ")
            print_map(rotated_map)
            for y, line in enumerate(rotated_map):
                line_str = listToString(line)
                index = line_str.find(pattern_str)
                if index != -1:
                    local_map = [row[:] for row in rotated_map]  # really makes COPY
                    add_to_x = pattern_str.find(" ")
                    print(index + add_to_x, y, sep=":")
                    mark_xes(local_map, changed_pattern, index, y)
                    balls_to_consider = find_not_considered_ball(local_map, color)
                    for point in balls_to_consider:
                        tmp_x = point[0]
                        tmp_y = point[1]
                        point[0] = 6 - tmp_x
                        point[1] = 6 - tmp_y
                        # JW
                    new_x = 6 - (index + add_to_x)
                    new_y = 6 - y

                    # tutaj posortowac balls to consider po signal
                    balls_to_consider = add_signal(balls_to_consider, signal_map)
                    balls_to_consider = sort_balls_to_consider(balls_to_consider)

                    ball_found = try_to_move_ball(map, balls_to_consider, new_x, new_y)
                    if ball_found:
                        print("Ball found.")
                        print("Adding to solutions: ", pattern)
                        solutions_holder.save_solution(color, True if pattern.count("SAME") >= 4 else False,
                                                       len(pattern),
                                                       ball_found[0], ball_found[1], new_x,
                                                       new_y)
                    else:
                        print("Ball not found.")

            print("nie znalazłem pattern w -180'")

            # JW rotated map part 270' antyclockwise
            # trzeba pomieszać z indeksami
            rotate_matrix(rotated_map)
            print("Rotated by 270': ")
            print_map(rotated_map)
            for y, line in enumerate(rotated_map):
                line_str = listToString(line)
                index = line_str.find(pattern_str)
                if index != -1:
                    local_map = [row[:] for row in rotated_map]  # really makes COPY
                    add_to_x = pattern_str.find(" ")
                    print(index + add_to_x, y, sep=":")
                    mark_xes(local_map, changed_pattern, index, y)
                    balls_to_consider = find_not_considered_ball(local_map, color)
                    for point in balls_to_consider:
                        tmp_x = point[0]
                        tmp_y = point[1]
                        point[0] = tmp_y
                        point[1] = 6 - tmp_x
                        # JW
                    new_x = y
                    new_y = 6 - (index + add_to_x)

                    # tutaj posortowac balls to consider po signal
                    balls_to_consider = add_signal(balls_to_consider, signal_map)
                    balls_to_consider = sort_balls_to_consider(balls_to_consider)

                    ball_found = try_to_move_ball(map, balls_to_consider, new_x, new_y)
                    if ball_found:
                        print("Ball found.")
                        print("Adding to solutions: ", pattern)
                        solutions_holder.save_solution(color, True if pattern.count("SAME") >= 4 else False,
                                                       len(pattern),
                                                       ball_found[0], ball_found[1], new_x,
                                                       new_y)
                    else:
                        print("Ball not found.")

            print("nie znalazłem pattern w -270'")
    solutions_holder.show_best_solutions()
