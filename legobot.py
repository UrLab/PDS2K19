import socket
from utils import SERV_PORT
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


s = socket.socket()          # Create a socket object
host = socket.gethostname()  # Get local machine name
s.bind((host, SERV_PORT))    # Bind to the port
s.listen(1)
nxt_sock, addr = s.accept()


while True:
    action = recv_action()
    actions[action]()
    state = get_state()
    send_state(state)
