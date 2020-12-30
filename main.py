from time import sleep

from interface import get_map_from_server
from interface import move_ball_on_server
import chooser


def check_if_valid(map):
    for line in map:
        for char in line:
            if char == 'None':
                return False
    return True


def print_map(map):
    for line in map:
        print(line)


map = get_map_from_server()
#
# diags_here = chooser.create_diag_up(map)
# print(diags_here)
#
# diags_here = chooser.create_diag_down(map)
# print(diags_here)

#after = chooser.add_signal([[0, 1, 0], [0, 2, 0], [0, 3, 0]], sig)
#print(after)
while True:
    sleep(1.0)
    map = get_map_from_server()
    sig = chooser.create_the_signal_map(map)
    local_map = [row[:] for row in map]  # really makes COPY
    Solution_For_Diag = 1
    if check_if_valid(map):
        print("Everything is ok.")
        if chooser.balls_number(map) == 49:
            print('\033[96m' + "Thank you for watching the game. I did my best.")
            break
        src_x, src_y, tar_x, tar_y, Solution_For_Diag = chooser.find_pattern(map)

        # Avoid collumn 0 and 6 cork

        if Solution_For_Diag == False:
            if tar_x == 6 or tar_x == 0:
                if ((tar_y < 6) and local_map[tar_y+1][tar_x] == ' '  and sig[tar_y][tar_x] < sig[tar_y+1][tar_x]):
                    print("próba odkorkowania - ruch kulki w górę", str(tar_y), str(tar_x))
                    tar_y = tar_y + 1
                    print("próba odkorkowania - ruch kulki w górę", str(tar_y), str(tar_x))
                elif ((tar_y > 0) and local_map[tar_y-1][tar_x] == ' '  and sig[tar_y][tar_x] < sig[tar_y-1][tar_x]):
                    print("próba odkorkowania - ruch kulki w doł", str(tar_y), str(tar_x))
                    tar_y = tar_y - 1
                    print("próba odkorkowania - ruch kulki w doł", str(tar_y), str(tar_x))

        # Avoid raw 0 and 6 cork
            elif tar_y == 6 or tar_y == 0:
                if ((tar_x < 6) and  local_map[tar_y][tar_x+1] == ' '  and sig[tar_y][tar_x] <  sig[tar_y][tar_x+1]):
                    print("próba odkorkowania - ruch kulki w górę", str(tar_y), str(tar_x))
                    tar_x = tar_x + 1
                    print("próba odkorkowania - ruch kulki w górę", str(tar_y), str(tar_x))
                elif ((tar_x > 0) and local_map[tar_y][tar_x-1] == ' ' and sig[tar_y][tar_x] < sig[tar_y][tar_x-1]):
                    print("próba odkorkowania - ruch kulki w doł", str(tar_y), str(tar_x))
                    tar_x = tar_x - 1
                    print("próba odkorkowania - ruch kulki w doł", str(tar_y), str(tar_x))

        move_ball_on_server(src_x, src_y, tar_x, tar_y)
    else:
        print("Check your screen.")
        sleep(0.7)

# number_of_balls = chooser.balls_number(map)
# print("Number of balls:", number_of_balls)
#
# print("The most common ball: ", chooser.get_most_common_ball(map))
