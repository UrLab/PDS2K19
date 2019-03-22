import socket
import utils
import pickle as p
from nxt_raspi_interface import left, right, forward, back


actions = [forward, left, right, back]


def get_state():
    # TODO: INSERT CODE FOR RETREIVING CAM AND SENSORS INPUT
    pass


def send_state(state):
    s.send(p.dumps(state))


def recv_action():
    global s
    action = s.recv(1024)
    return p.loads(action)


s = socket.socket()
host = input()
port = utils.SERV_PORT

s.connect((host, port))


while True:
    action = recv_action()
    actions[action]()
    state = get_state()
    send_state(state)
