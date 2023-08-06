import gym
from gym import spaces

import numpy as np
from dm_gym.rewards.ClusteringEnv_3_reward import Reward_Function
from sklearn.utils import shuffle
from copy import deepcopy

from dm_gym.env_conf import assign_env_config

from dm_gym.utils.data_gen import data_gen_clustering



class ClusteringEnv_3(gym.Env):

    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, *args, **kwargs):
        super(ClusteringEnv_3, self).__init__()

        assign_env_config(self, kwargs)
        self.current_step = 0

        self.total_data_size = len(self.data.index)

        self.R = Reward_Function()

        self.reward_range = (-1, 1)

        min_val = self.data.min().tolist()
        max_val = self.data.max().tolist()

        min_val = [x-1 for x in min_val]
        max_val = [x+1 for x in max_val]

        self.action_space = spaces.Discrete(self.k)

        self.observation_space = spaces.Box(low=np.array(
            min_val), high=np.array(max_val), dtype=np.float64)
        data_gen = data_gen_clustering()
        _, self.prototype_centroids = data_gen.gen_model_Kmeans(self.data, self.k)
        
        self.centroids = deepcopy(self.prototype_centroids)

    def reset(self):
        self.current_step = 0

        self.data_env = deepcopy(self.data)
        self.data_env = shuffle(self.data_env)
        self.data_env.reset_index(inplace=True, drop=True)

        self.prev_obs = self.data_env.iloc[self.current_step].tolist()

        return self.prev_obs

    def step(self, action):

        action = int(action)
        self.current_step += 1

        if self.current_step >= self.total_data_size - 1:
            done = True
        else:
            done = False

        reward = self.R.reward_function(self.prev_obs, action, self.centroids)

        obs = self.data_env.iloc[self.current_step].tolist()
        self.prev_obs = obs

        return obs, reward, done, {'centroids': self.centroids}

    def render(self, mode='human', close=False):

        print('Step: ', self.current_step)
        print('Current reward: ', self.R.reward_function(
            self.final_state_data, self.k, self.total_data_size))