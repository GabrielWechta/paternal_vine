import requests
import json


def get_map_from_server():
    response = requests.get('http://127.0.0.1:5000/getmap')
    # return response.text
    #
    xxx = response.text.split(',\n')
    #
    # #xxx=eval(response.text)
    # #xxx=json.loads(response.text)
    # print(xxx)
    #
    for idx, a in enumerate(xxx):
        xxx[idx] = a.split('][')
        for idx2, a2 in enumerate(xxx[idx]):
            xxx[idx][idx2] = xxx[idx][idx2].replace('[', '')
            xxx[idx][idx2] = xxx[idx][idx2].replace(']', '')
    return xxx


def move_ball_on_server(x0, y0, x1, y1):
    """
    :param x0 from x
    :param y0 from y
    :param x1 to x
    :param y1 to y
    """
    requests.get('http://127.0.0.1:5000/move/{}/{}/{}/{}'.format(x0, y0, x1, y1))
