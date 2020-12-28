
from functions import *


def find_pattern(map, Solution_For_Diag):
    pattern_tab = [["SAME", "SAME", "SAME", "SAME", "EMPTY", "SAME", "SAME"],  # 6 in a raw, 5 SAME
                   ["SAME", "SAME", "SAME", "EMPTY", "SAME", "SAME", "SAME"],
                   ["SAME", "SAME", "EMPTY", "SAME", "SAME", "SAME", "SAME"],

                   ["SAME", "SAME", "SAME", "SAME", "EMPTY", "SAME"],  # 6 in a raw 5 SAME
                   ["SAME", "SAME", "SAME", "EMPTY", "SAME", "SAME"],
                   ["SAME", "SAME", "EMPTY", "SAME", "SAME", "SAME"],
                   ["SAME", "EMPTY", "SAME", "SAME", "SAME", "SAME"],
                   ["EMPTY", "SAME",  "SAME", "SAME", "SAME", "SAME"],

                   ["SAME", "SAME", "SAME", "SAME", "EMPTY"],  # 5 in a row 4 SAME
                   ["SAME", "SAME", "SAME", "EMPTY", "SAME"],
                   ["SAME", "SAME", "EMPTY", "SAME", "SAME"],
                   ["SAME", "EMPTY", "SAME", "SAME", "SAME"],
                   ["EMPTY", "SAME", "SAME", "SAME", "SAME"],

                   ["SAME", "SAME", "SAME", "EMPTY", "EMPTY"],  # 5 in a raw 3 SAME
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

    pattern_kork_tab = [["SAME", "SAME", "SAME", "SAME", "EMPTY", "SAME", "SAME"],  # 6 in a raw, 5 SAME
                   ["SAME", "SAME", "SAME", "EMPTY", "SAME", "SAME", "SAME"],
                   ["SAME", "SAME", "EMPTY", "SAME", "SAME", "SAME", "SAME"],

                   ["SAME", "SAME", "SAME", "SAME", "DIFF", "SAME"],  # 6 in a raw 5 SAME
                   ["SAME", "SAME", "SAME", "DIFF", "SAME", "SAME"],
                   ["SAME", "SAME", "DIFF", "SAME", "SAME", "SAME"],
                   ["SAME", "DIFF", "SAME", "SAME", "SAME", "SAME"],
                   ["DIFF", "SAME", "SAME", "SAME", "SAME", "SAME"],

                   ["SAME", "SAME", "SAME", "SAME", "DIFF"],  # 5 in a row 4 SAME
                   ["SAME", "SAME", "SAME", "DIFF", "SAME"],
                   ["SAME", "SAME", "DIFF", "SAME", "SAME"],
                   ["SAME", "DIFF", "SAME", "SAME", "SAME"],
                   ["DIFF", "SAME", "SAME", "SAME", "SAME"],

                   ["SAME", "SAME", "SAME", "DIFF"],  # 3 SAME
                   ["SAME", "SAME", "DIFF", "SAME"]]


    # pattern_tab = [["SAME", "SAME", "SAME", "SAME", "EMPTY"], ["SAME", "SAME", "EMPTY"], ["SAME", "EMPTY", "SAME"]]

    # create the signal map every time when new map is received from the mobile screen

    signal_map = create_the_signal_map(map)
    different_finder_and_signal_update(map, signal_map)

    diag_down_map = []
    diag_up_map = []



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
                        print("znalazłem kulkę")
                        #Solution_For_Diag = 1
                        if len(pattern) >= 6:
                            print('\033[96m' + str(pattern))
                        return ball_found[0], ball_found[1], new_x, new_y
                    else:
                        print("nie znalazłem kulki")

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
                        print("znalazłem kulkę")
                        Solution_For_Diag = 1
                        if len(pattern) >= 6:
                            print('\033[96m' + str(pattern))
                        return ball_found[0], ball_found[1], new_x, new_y
                    else:
                        print("nie znalazłem kulki")

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
                        print("znalazłem kulkę")
                        #Solution_For_Diag = 0
                        if len(pattern) >= 6:
                            print('\033[96m' + str(pattern))
                        return ball_found[0], ball_found[1], new_x, new_y
                    else:
                        print("nie znalazłem kulki")

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
                        print("znalazłem kulkę")
                        #Solution_For_Diag = 0
                        if len(pattern) >= 6:
                            print('\033[96m' + str(pattern))
                        return ball_found[0], ball_found[1], new_x, new_y
                    else:
                        print("nie znalazłem kulki")

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
                        print("znalazłem kulkę")
                        Solution_For_Diag = 0
                        if len(pattern) >= 6:
                            print('\033[96m' + str(pattern))
                        return ball_found[0], ball_found[1], new_x, new_y
                    else:
                        print("nie znalazłem kulki")

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
                        print("znalazłem kulkę")
                        #Solution_For_Diag = Fasle
                        if len(pattern) >= 6:
                            print('\033[96m' + str(pattern))
                        return ball_found[0], ball_found[1], new_x, new_y
                    else:
                        print("nie znalazłem kulki")

            print("nie znalazłem pattern w -270'")

            # rotate_matrix(rotated_map)
            #
            # # JW diag down handling
            # # trzeba jeszcze raz obr diag down
            #
            # print("Teraz diag down': mapa niepowinna rotowana")
            # print_map(rotated_map)
            #
            # diag_down_map = create_diag_down(rotated_map)
            # diag_down_map_orig_coordinates = create_diag_down_map_orig_coordinates()
            #
            # for y, line in enumerate(diag_down_map):
            #     line_str = listToString(line)
            #     index = line_str.find(pattern_str)
            #     if index != -1:
            #         local_map = [row[:] for row in rotated_map]  # really makes COPY
            #         add_to_x = pattern_str.find(" ")
            #         print(index + add_to_x, y, sep=":")
            #
            #         mark_diag_down_xes(local_map, changed_pattern, index, y)
            #
            #         balls_to_consider = find_not_considered_ball(local_map, color)
            #
            #         # JW wsp x and y m
            #
            #         new_x = diag_down_map_orig_coordinates[y][index + add_to_x][0]
            #         new_y = diag_down_map_orig_coordinates[y][index + add_to_x][1]
            #
            #         print(diag_down_map_orig_coordinates)
            #         print(balls_to_consider)
            #
            #         # tutaj posortowac balls to consider po signal
            #         balls_to_consider = add_signal(balls_to_consider, signal_map)
            #         balls_to_consider = sort_balls_to_consider(balls_to_consider)
            #
            #         ball_found = try_to_move_ball(map, balls_to_consider, new_x, new_y)
            #         if ball_found:
            #             print("znalazłem kulkę")
            #             if len(pattern) >= 6:
            #                 print('\033[96m' + str(pattern))
            #             return ball_found[0], ball_found[1], new_x, new_y
            #         else:
            #             print("nie znalazłem kulki")
            #
            # print("nie znalazłem pattern w diag_down")
            #
            # # JW diag up handling
            # # trzeba jeszcze raz obr diag up
            #
            # print("Teraz diag up': mapa powinna byc nierotowana ")
            # print_map(rotated_map)
            #
            # diag_up_map = create_diag_up(rotated_map)
            # diag_up_map_orig_coordinates = create_diag_up_map_orig_coordinates()
            #
            # for y, line in enumerate(diag_up_map):
            #     line_str = listToString(line)
            #     index = line_str.find(pattern_str)
            #     if index != -1:
            #         local_map = [row[:] for row in rotated_map]  # really makes COPY
            #         add_to_x = pattern_str.find(" ")
            #         print(index + add_to_x, y, sep=":")
            #
            #         mark_diag_up_xes(local_map, changed_pattern, index, y)
            #
            #         balls_to_consider = find_not_considered_ball(local_map, color)
            #
            #         # JW wsp x and y m
            #
            #         new_x = diag_up_map_orig_coordinates[y][index + add_to_x][0]
            #         new_y = diag_up_map_orig_coordinates[y][index + add_to_x][1]
            #
            #         print(diag_up_map_orig_coordinates)
            #         print(balls_to_consider)
            #
            #         # tutaj posortowac balls to consider po signal
            #         balls_to_consider = add_signal(balls_to_consider, signal_map)
            #         balls_to_consider = sort_balls_to_consider(balls_to_consider)
            #
            #         ball_found = try_to_move_ball(map, balls_to_consider, new_x, new_y)
            #         if ball_found:
            #             print("znalazłem kulkę")
            #             if len(pattern) >= 6:
            #                 print('\033[96m' + str(pattern))
            #             return ball_found[0], ball_found[1], new_x, new_y
            #         else:
            #             print("nie znalazłem kulki")
            #
            # print("nie znalazłem pattern w diag_up")


