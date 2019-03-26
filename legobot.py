import socket
from utils import SERV_PORT
import pickle as p
from nxt_raspi_interface.interface import Interface


interface = Interface()
print("Connected to the nxt")
actions = [interface.forward, interface.left, interface.right, interface.back]


def get_state():
    global interface
    img = interface.take_pic()
    # TODO
    ground = interface.touch_sensor()
    # TODO
    return (img, ground)


def send_state(state):
    global s
    s.send(p.dumps(state))


def recv_action():
    global s
    action = s.recv(1024)
    return p.loads(action)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          # Create a socket object
s.bind(('', SERV_PORT))    # Bind to the port
s.listen(1)
nxt_sock, addr = s.accept()


while True:
    state = get_state()
    send_state(state)
    action = recv_action()
    actions[action]()
