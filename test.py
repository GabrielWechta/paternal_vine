import subprocess
from skimage import io
from skimage.viewer import ImageViewer
import numpy as np
from skimage import filters, morphology
from skimage.draw import polygon
from flask import Flask, jsonify, abort

board_size = 7
colors = [[240, 240, 240, " "],
          [90, 110, 240, "B"],
          [240, 240, 30, "Y"],
          [30, 240, 30, "G"],
          [230, 150, 60, "O"],
          [120, 30, 190, "V"],
          [240, 30, 240, "P"],
          [220, 220, 220, "S"],
          [30, 240, 240, "C"],
          [240, 30, 30, "R"],

          [90, 110, 230, "B"],
          [230, 230, 30, "Y"],
          [30, 230, 30, "G"],
          [230, 140, 60, "O"],
          [120, 30, 190, "V"],
          [230, 30, 230, "P"],
          [220, 220, 220, "S"],
          [30, 230, 230, "C"],
          [230, 30, 30, "R"]]

screenshot = "c:\\kulki\\screen.png"
screenshot_command = "adb  exec-out screencap -p > " + screenshot

start_x = 0
start_y = 0
field_width = 0
gap_width = 0
field_height = 0
gap_height = 0

initDone = False

app = Flask(__name__)


@app.route('/init')
def init():
    global initDone
    global start_x
    global start_y
    global field_width
    global gap_width
    global field_height
    global gap_height

    adb_devices = "adb devices"
    output = subprocess.check_output(adb_devices, shell=True)
    output = subprocess.check_output(screenshot_command, shell=True)
    screen_RGB = io.imread(screenshot)
    screen = io.imread(screenshot, as_gray=True)

    size_y = screen.size
    size_x = screen[0].size

    size_y = size_y / size_x

    histo, bins = np.histogram(screen * 256, bins=np.arange(0, 256))
    # remove all black and all white pixels from histogram.
    histo[:10] = [0] * 10
    histo[-10:] = [0] * 10

    max = np.argmax(histo)

    th1 = (max - 1) / 256
    th2 = (max + 1) / 256

    thr1 = screen >= th1
    thr2 = screen <= th2
    thr = thr1 * thr2

    thr = morphology.erosion(thr, morphology.square(int(size_x / 80)))

    field_width = size_x / board_size
    start_y = 0

    # find first y line
    for y in range(0, int(size_y), 2):
        counter = 0
        for x in range(0, int(size_x), 1):
            if thr[y][x]:
                counter += 1
        if counter > 40:
            start_y = y
            break
    print("start_Y = {}".format(start_y))

    # find first and last column
    for x in range(0, int(size_x), 1):
        counter = 0
        for y in range(start_y, start_y + int(size_y / 2), 1):
            if thr[y][x]:
                counter += 1
        if counter > 40:
            start_x = x
            break

    for x in range(size_x - 1, 0, -1):
        counter = 0
        for y in range(start_y, start_y + int(size_y / 2), 1):
            if thr[y][x]:
                counter += 1
        if counter > 40:
            stop_x = x
            break

    # determine field sizes and gaps
    fields_x = []
    gaps_x = []

    print("start {} stop {}".format(start_x, stop_x))
    is_on_field = True
    temp = 0
    for x in range(start_x, stop_x + 2, 1):
        if thr[start_y + 5][x] == is_on_field:
            temp += 1
        else:
            if is_on_field:
                fields_x.append(temp)
            else:
                gaps_x.append(temp)
            is_on_field = not is_on_field
            temp = 1

    print(fields_x)
    print(gaps_x)

    # determine field sizes and gaps
    fields_y = []
    gaps_y = []

    print("start {}".format(start_y))
    is_on_field = True
    temp = 0
    for y in range(start_y, int(size_y), 1):
        if thr[y][start_x + 5] == is_on_field:
            temp += 1
        else:
            if is_on_field:
                fields_y.append(temp)
            else:
                gaps_y.append(temp)
            is_on_field = not is_on_field
            temp = 1

    print(fields_y)
    print(gaps_y)

    bins = np.bincount(fields_x)
    field_width = np.argmax(bins)
    print(field_width)

    bins = np.bincount(gaps_x)
    gap_width = np.argmax(bins)
    print(gap_width)

    bins = np.bincount(fields_y)
    field_height = np.argmax(bins)
    print(field_height)

    bins = np.bincount(gaps_y)
    gap_height = np.argmax(bins)
    print(gap_height)

    initDone = True

    return "Init done"


def get_color(values):
    for c in colors:
        if c[0] == values[0] and c[1] == values[1] and c[2] == values[2]:
            return c[3]
    return None


def readBoard():
    subprocess.check_output(screenshot_command, shell=True)
    screen_RGB = io.imread(screenshot)

    board = {}

    for x in range(0, board_size, 1):
        for y in range(0, board_size, 1):
            slice_x1 = start_x + ((field_width + gap_width) * x)
            slice_x2 = slice_x1 + field_width
            slice_y1 = start_y + ((field_height + gap_height) * y)
            slice_y2 = slice_y1 + field_height
            slice = screen_RGB[slice_y1:slice_y2, slice_x1:slice_x2]
            avg_color = np.floor(np.mean(slice, axis=(0, 1)) / 10) * 10
            if get_color(avg_color) is not " ":
                print(avg_color)
            board[x, y] = get_color(avg_color)

            poly = np.array((
                (slice_y1, slice_x1),
                (slice_y1, slice_x2),
                (slice_y2, slice_x2),
                (slice_y2, slice_x1)
            ))

            rr, cc = polygon(poly[:, 0], poly[:, 1])
            screen_RGB[rr, cc, 1] = 1
            print("board[{}][{}] = {}".format(x, y, board[x, y]))
    board_txt = ""
    for y in range(0, board_size, 1):
        str = ""
        for x in range(0, board_size, 1):
            str += "[{}]".format(board[x, y])
        board_txt += str
        if y is not board_size - 1:
            board_txt += ",\n"
        print(str)
    return "[{}]".format(board_txt)


# screen_RGB[thr] = [0, 255, 0, 255]
# viewer = ImageViewer(screen_RGB)
# viewer.show()
# for i in range(0,30):
def tap(x, y):
    bashCommand = "adb shell input tap {} {}".format(start_x + (x * (gap_width + field_width)),
                                                     start_y + (y * (gap_height + field_height)))
    subprocess.check_output(bashCommand, shell=True)


@app.route('/getmap')
def getMap():
    print("initDone {}".format(initDone))
    if (not initDone):
        abort(500)
    return readBoard()


@app.route('/move/<int:x1>/<int:y1>/<int:x2>/<int:y2>', methods=['GET'])
def move(x1, y1, x2, y2):
    if x1 not in range(0, board_size) or y1 not in range(0, board_size) or x2 not in range(0,
                                                                                           board_size) or y2 not in range(
            0, board_size):
        abort(404)

    tap(x1, y1)
    tap(x2, y2)
    return "{} {} {} {}".format(x1, y1, x2, y2)


if __name__ == '__main__':
    app.run(debug=True)
