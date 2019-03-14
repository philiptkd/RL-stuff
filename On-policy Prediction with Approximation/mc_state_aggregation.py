# used to recreate Fig. 9.1

from random_walk_env import RandomWalkEnv
import numpy as np
import matplotlib.pyplot as plt
import pickle
from coarse_coding import approx_v, get_all_bounds


# returns a list of tuples (S_t, R_t)
#   the final tuple's state will be env.start and should not be used
def get_trajectory(env):
    trajectory = []
    env.reset() # redundancy
    trajectory.append((env.state, 0)) # R_0 = 0
    done = False
    while not done:
        next_state, reward, done = env.step()
        trajectory.append((next_state, reward))
    return trajectory


# gradient Monte Carlo as on page 202
# assumes 1000 states in env
def grad_mc(episodes, alpha, env, width, gamma=1, offset=None):
    if offset is None:
        offset = width   # no overlap between groups
    else:
        bounds = get_all_bounds(width, offset, range(env.num_states))
    
    num_features = (1000-width)//offset+1
    w = np.zeros(num_features)
    for episode in range(episodes):
        if episode%1000==0:
            print("episode: "+str(episode)+"/"+str(episodes))

        trajectory = get_trajectory(env)
        G = 0
        for t in range(len(trajectory)-2, -1, -1): # t = T-1,...,1,0
            r = trajectory[t+1][1]
            s = trajectory[t][0]
            G = gamma*G + r

            if offset == width: # faster version
                group = (s-1)//width  # 1<=s<=1000, but group indices start at 0
                w[group] += alpha*(G - w[group])    # v(s,w) = w[group]
            else:   # more general version
                left,right,v = approx_v(w,s-1,width,offset,bounds)
                w[left:right+1] += alpha*(G - v)
        yield w

# to plot things for the figure
def plot_approximation():
    env = RandomWalkEnv()
    episodes = 10000
    width = 100
    offset = 100
    w_generator = grad_mc(episodes, 0.0002, env, width, offset=offset)
    for episode in range(episodes): # we only need the last one
        w = next(w_generator)

    x = range(1,1001)
    bounds = get_all_bounds(width, offset, range(env.num_states))
    y = [approx_v(w,s,width,offset,bounds)[2] for s in range(1000)]
    plt.plot(x, y, label="aggregation")

    # load and plot "true" values
    with open("data/true_values.npy", "rb") as f:
        y2 = pickle.load(f)
    plt.plot(x, y2, label="true values")

    plt.ylim([-1,1])
    plt.show()

#plot_approximation()
