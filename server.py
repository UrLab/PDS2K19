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
    data = nxt_sock.recv(4096)
    return p.loads(data)


def send_action(action):
    global nxt_sock
    nxt_sock.send(p.dumps(action))


def is_out(state):
    # TODO: define when the bot is out of the circuit, given its sensors state
    return True


def reward(state):
    return -1 if is_out(state) else 1


s = socket.socket()          # Create a socket object
host = socket.gethostname()  # Get local machine name
s.bind((host, SERV_PORT))    # Bind to the port

s.listen(1)
nxt_sock, addr = s.accept()
print("Connected to the bot! (hopefully)")


while True:
    # Initialize the environment and state
    # TODO: Understand why this was done in the first place
    state = current_screen - last_screen
    for t in count():
        print("Current length of episode: ", t)
        print("Overall length of episode: ", end='')
        for episode in episode_durations:
            print(episode, end=", ")
        print()
        # Select and perform an action
        action = rql.select_action(state)
        send_action(action)
        bot_state = get_bot_state()
        reward = torch.tensor([reward(bot_state)], device=rql.device)

        # Observe new state
        done = is_out(bot_state)
        if not done:
            next_state = current_screen - last_screen
        else:
            next_state = None

        # Store the transition in memory
        rql.memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the target network)
        rql.optimize_model()
        if done:
            episode_durations.append(t + 1)
            break
        rql.target_update()
