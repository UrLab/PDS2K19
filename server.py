import reinforcement_q_learning as rql

import torch
from utils import SERV_PORT
from itertools import count
import pickle as p
import socket


episode_durations = []


def get_bot_state():
    # note: nxt bot should have transformed image to gray before sending it
    global nxt_sock
    data = ""
    d_len = p.loads(nxt_sock.recv(32))
    while d_len > data:
        data += nxt_sock.recv(d_len)
    return p.loads(data)


def send_action(action):
    global nxt_sock
    nxt_sock.send(p.dumps(action))


def is_out(state):
    # TODO: define when the bot is out of the circuit, given its sensors state
    return True


def reward(state):
    return -1 if is_out(state) else 1


nxt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to the bot...")
host = input("Please enter the bot's IP: ")
port = SERV_PORT
print("Using port ", port)
nxt_sock.connect((host, port))
print("Connected to the bot! (hopefully) at ", host, ":", port)


bot_state, ground = get_bot_state()
action = rql.select_action(bot_state)
send_action(action)
while True:
    # Initialize the environment and state
    for t in count():
        print("Current length of episode: ", t+1)

        # Select and perform an action
        prev_state = bot_state
        bot_state, ground = get_bot_state()
        reward = torch.tensor([reward(ground)], device=rql.device)
        done = is_out(ground)
        if done:
            send_action(3)
        else:
            action = rql.select_action(bot_state)
            send_action(action)

        # Store the transition in memory
        rql.memory.push(prev_state, action, bot_state, reward)

        # Perform one step of the optimization (on the target network)
        rql.optimize_model()
        if done:
            episode_durations.append(t + 1)
            break

    rql.target_update()
