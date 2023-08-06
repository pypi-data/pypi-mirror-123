import numpy as np

class Reward_Function:

    def __init__(self):
        pass

    def reward_function(self, obs, action, centroids):
        reward = 0

        y_i = self.get_yi(centroids, obs, action)

        if(y_i == 1):
            reward = 1
        else:
            reward = -1

        return reward

    def get_yi(self, coordinates, obs, action):
        dist = []
        for coor in coordinates:
            c = np.array(coor)
            d = np.array(obs)
            dist.append(np.linalg.norm(c-d))

        y_i = dist.index(min(dist))
        if(y_i == action):
            y_i = 1
        else:
            y_i = 0

        return y_i

