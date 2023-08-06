import numpy as np
import math



class Reward_Function:

    def __init__(self):
        pass

    def reward_function(self, obs, action, centroids):
        reward = 0

        y_i = self.get_yi(centroids, obs, action)
        p = self.get_p_i(centroids[action], obs)

        '''
        p_is = []
        for coords in centroids:
            p_is.append(self.get_p_i(coords, obs))
        p_is = np.array(p_is)/sum(p_is)

        p = p_is[action]
        reward = p
        '''

        if(y_i == 1):
            #reward = 1/(y_i-p)
            #reward = 1
            reward =  p
        else:
            #reward = -1/(y_i-p)
            #reward = -1
            reward = -1*(1-p)

        return reward, y_i, p

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
    
    def get_p_i(self, coordinates, obs):
        s_i = np.linalg.norm(np.array(coordinates) - np.array(obs))
        f_si = 1 / 1 + math.exp(-s_i)
        p_i = 2 * (1 - f_si)
        return p_i

