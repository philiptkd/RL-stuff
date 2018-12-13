import numpy as np

class RandomWalkEnv():
    def __init__(self):
        self.num_states = 19 # not counting terminal state(s)
        self.start = 9   # start state
        self.true_values = [i/20 for i in range(1,20)] 
        self.np_random = np.random.RandomState()
        self.reset()

    def reset(self):
        self.state = self.start

    # returns (reward, done)
    def step(self):
        self.state += np_random.choice([-1,1])
        if self.state == -1:
            self.reset()
            return -1, True
        if self.state == self.num_states:
            self.reset()
            return 1, True
        return 0, False
