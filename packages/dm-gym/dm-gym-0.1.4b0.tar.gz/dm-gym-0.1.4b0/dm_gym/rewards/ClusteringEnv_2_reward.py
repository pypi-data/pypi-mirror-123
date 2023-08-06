import numpy as np
import pandas as pd

import math

from copy import deepcopy
from sklearn.metrics import davies_bouldin_score as dbindex


class Reward_Function:

    def __init__(self):
        pass

    def reward_function(self, obs, action, centroids):
        reward = 0

        y = self.get_yi(centroids, obs)

        if(y == action):
            reward = 1
        else:
            reward = -1
        
        return reward

    def get_yi(self, coordinates, obs):
        dist = []
        for coor in coordinates:
            c = np.array(coor)
            d = np.array(obs)
            dist.append(np.linalg.norm(c-d))

        y_i = dist.index(min(dist))

        return y_i
