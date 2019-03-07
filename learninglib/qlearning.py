import numpy as np
import np.random as rng


class SelectionMethods:

    @staticmethod
    def _boltzman(tau, payoffs):
        probs = np.array([np.exp(payoffs[action] / tau)
                          for action in payoffs])
        probs = probs / np.sum(probs)
        return probs

    @staticmethod
    def random(expected, dummy):
        return (rng.choice(expected), dummy)

    @staticmethod
    def epsilon_greedy(expected, eps):
        if rng.uniform() < eps:
            return (rng.random(expected, eps), eps)
        else:
            return (np.argmax(expected), eps)

    @staticmethod
    def softmax(expected, tau):
        return (rng.choice(expected,
                           p=SelectionMethods._boltzman(tau, expected)), tau)

    @staticmethod
    def varying_softmax(expected, tick):
        return (SelectionMethods.softmax(expected, (4 - tick / 250)), tick + 1)

    @staticmethod
    def varying_egreedy(expected, tick):
        return (SelectionMethods.epsilon_greedy(expected, 1 / np.sqrt(tick)),
                tick + 1)


class QLearning:

    selection_strats = {"e-greedy": (SelectionMethods.epsilon_greedy, 0.1),
                        "softmax": (SelectionMethods.softmax, 0.1),
                        "random": (SelectionMethods.random, None),
                        "var_sotfmax": (SelectionMethods.varying_softmax, 0),
                        "var_egreedy": (SelectionMethods.varying_egreedy, 0)
                        }

    def __init__(self, actions, states, strat="var_egreedy",
                 alpha=None, gamma=None, sel_param=None):
        self.sel_strat, self.sel_param = QLearning.selection_strats[strat]
        self.sel_param = sel_param or self.sel_param
        self.alpha = alpha or 0.1
        self.gamma = gamma or 0.9
        self.actions = list(actions)
        self.states = list(states)
        self.estimated = np.zeros((len(self.states), len(self.actions)))

    def get_best_action(self, state):
        state_index = self.states.index(state)
        return self.actions[np.argmax(self.estimated[:, state_index])]

    def explore(self, state):
        state_index = self.states.index(state)
        action, self.sel_param = self.sel_strat(self.estimated[:, state_index],
                                                self.sel_param)
        return self.actions(action)

    def update_estimation(self, old_state, new_state, action, reward):
        self.estimated[old_state, action] = (1 - self.alpha) * self.estimated[old_state, action] \
                                            + self.alpha * (reward + self.gamma * np.max(self.estimated(new_state)))
