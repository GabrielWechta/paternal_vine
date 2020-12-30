import operator

from functions import *


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
                   ["SAME", "EMPTY", "EMPTY", "SAME", "SAME"],
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
                                                       pattern.count("SAME"),
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
                                                       pattern.count("SAME"),
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
                                                       pattern.count("SAME"),
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
                                                       pattern.count("SAME"),
                                                       ball_found[0], ball_found[1], new_x,
                                                       new_y)
                    else:
                        print("Ball not found.")

            print("nie znalazłem pattern w -270'")

            # JW diag down handling
            # trzeba jeszcze raz obr diag down
            rotate_matrix(rotated_map)

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
                                                       pattern.count("SAME"),
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
                                                       pattern.count("SAME"),
                                                       ball_found[0], ball_found[1], new_x,
                                                       new_y)
                    else:
                        print("Ball not found.")

            print("nie znalazłem pattern w diag_up")

    print(solutions_holder.show_best_solutions())
    ans = solutions_holder.decide(map, signal_map)
    return ans[0], ans[1], ans[2], ans[3], True


class SolutionsHolder:
    def __init__(self):
        self.red = [None]
        self.green = [None]
        self.blue = [None]
        self.yellow = [None]

    def save_solution(self, color: str, is_ending: bool, matching: int, ball_x: int, ball_y: int, hole_x: int,
                      hole_y: int):
        if color == "R" and self.red[0] is None:
            self.red = [is_ending, matching, ball_x, ball_y, hole_x, hole_y]
        if color == "G" and self.green[0] is None:
            self.green = [is_ending, matching, ball_x, ball_y, hole_x, hole_y]
        if color == "B" and self.blue[0] is None:
            self.blue = [is_ending, matching, ball_x, ball_y, hole_x, hole_y]
        if color == "Y" and self.yellow[0] is None:
            self.yellow = [is_ending, matching, ball_x, ball_y, hole_x, hole_y]

    def show_best_solutions(self):
        print("Red: ", self.red)
        print("Green: ", self.green)
        print("Blue: ", self.blue)
        print("Yellow: ", self.yellow)

    def decide(self, map, signal_map):
        solutions = []
        for solution in [self.red, self.green, self.blue, self.yellow]:
            if solution[0] is not None:
                solutions.append(solution)

        sorted_solutions = sorted(solutions, key=operator.itemgetter(1), reverse=True)
        ending_solutions = [solution if solution[0] is True else None for solution in sorted_solutions]
        for ending in ending_solutions:
            if ending is not None:
                return ending[2], ending[3], ending[4], ending[5]

        """ Signal map part """
        balls_by_signal = []
        for y, _ in enumerate(signal_map):
            for x, _ in enumerate(signal_map):
                if signal_map[y][x] >= 10:
                    balls_by_signal.append([signal_map[y][x], x, y])

        if len(balls_by_signal) > 0:
            sorted_balls_by_signal = sorted(balls_by_signal, key=lambda l: l[0], reverse=True)
            for ball in sorted_balls_by_signal:
                places_to_consider = bfs_for_most_sparse_place(map, ball[1], ball[2])
                if len(places_to_consider) == 0:
                    continue
                places_sorted = sorted(places_to_consider, key=operator.itemgetter(0), reverse=False)
                tar_x, tar_y = places_sorted[0][1], places_sorted[0][2]
                src_x, src_y = ball[1], ball[2]

                return src_x, src_y, tar_x, tar_y
            # for ball in sorted_balls_by_signal:
            #     ball_x, ball_y, ball_color = ball[1], ball[2], map[ball[2]][ball[1]]
            #     if ball_color == "R" and self.red[0] is not None:
            #         hole_x, hole_y = self.red[4], self.red[5]
            #         if bfs(map, ball_x, ball_y, hole_x, hole_y):
            #             return ball_x, ball_y, hole_x, hole_y
            #     if ball_color == "G" and self.green[0] is not None:
            #         hole_x, hole_y = self.green[4], self.green[5]
            #         if bfs(map, ball_x, ball_y, hole_x, hole_y):
            #             return ball_x, ball_y, hole_x, hole_y
            #     if ball_color == "B" and self.blue[0] is not None:
            #         hole_x, hole_y = self.blue[4], self.blue[5]
            #         if bfs(map, ball_x, ball_y, hole_x, hole_y):
            #             return ball_x, ball_y, hole_x, hole_y
            #     if ball_color == "Y" and self.yellow[0] is not None:
            #         hole_x, hole_y = self.yellow[4], self.yellow[5]
            #         if bfs(map, ball_x, ball_y, hole_x, hole_y):
            #             return ball_x, ball_y, hole_x, hole_y

        return sorted_solutions[0][2], sorted_solutions[0][3], sorted_solutions[0][4], sorted_solutions[0][5]
