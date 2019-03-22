import reinforcement_q_learning as rql

import torch
from utils import SERV_PORT
from itertools import count
import pickle as p
import socket
# Get screen size so that we can initialize layers correctly based on shape
# returned from AI gym. Typical dimensions at this point are close to 3x40x90
# which is the result of a clamped and down-scaled render buffer in get_screen()


episode_durations = []


######################################################################
# Training loop
# ^^^^^^^^^^^^^
#
# Finally, the code for training our model.
#
# Here, you can find an ``optimize_model`` function that performs a
# single step of the optimization. It first samples a batch, concatenates
# all the tensors into a single one, computes :math:`Q(s_t, a_t)` and
# :math:`V(s_{t+1}) = \max_a Q(s_{t+1}, a)`, and combines them into our
# loss. By defition we set :math:`V(s) = 0` if :math:`s` is a terminal
# state. We also use a target network to compute :math:`V(s_{t+1})` for
# added stability. The target network has its weights kept frozen most of
# the time, but is updated with the policy network's weights every so often.
# This is usually a set number of steps but we shall use episodes for
# simplicity.
#

######################################################################
#
# Below, you can find the main training loop. At the beginning we reset
# the environment and initialize the ``state`` Tensor. Then, we sample
# an action, execute it, observe the next screen and the reward (always
# 1), and optimize our model once. When the episode ends (our model
# fails), we restart the loop.
#
# Below, `num_episodes` is set small. You should download
# the notebook and run lot more epsiodes, such as 300+ for meaningful
# duration improvements.


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


######################################################################
# Here is the diagram that illustrates the overall resulting data flow.
#
# .. figure:: /_static/img/reinforcement_learning_diagram.jpg
#
# Actions are chosen either randomly or based on a policy, getting the next
# step sample from the gym environment. We record the results in the
# replay memory and also run optimization step on every iteration.
# Optimization picks a random batch from the replay memory to do training of the
# new policy. "Older" target_net is also used in optimization to compute the
# expected Q values; it is updated occasionally to keep it current.
#
