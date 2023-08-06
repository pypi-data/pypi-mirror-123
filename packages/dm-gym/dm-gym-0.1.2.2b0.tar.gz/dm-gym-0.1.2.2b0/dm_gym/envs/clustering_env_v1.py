import gym
from gym import spaces

import pandas as pd
import numpy as np
from dm_gym.rewards.ClusteringEnv_1_reward import Reward_Function
from sklearn.utils import shuffle
from copy import deepcopy

from dm_gym.env_conf import assign_env_config

#import matplotlib.pyplot as plt


class ClusteringEnv_1(gym.Env):

    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, *args, **kwargs):
        super(ClusteringEnv_1, self).__init__()

        assign_env_config(self, kwargs)
        self.current_step = 0

        self.total_data_size = len(self.data.index)

        self.reward_range = (-1000, 1000)

        min_val = self.data.min().tolist()
        max_val = self.data.max().tolist()

        min_val = [x-1 for x in min_val]
        max_val = [x+1 for x in max_val]

        max_dist = np.linalg.norm(np.array(max_val)-np.array(min_val))

        self.action_space = spaces.Discrete(self.k)

        self.R = Reward_Function(max_dist)

        self.observation_space = spaces.Box(low=np.array(
            min_val), high=np.array(max_val), dtype=np.float64)

    def reset(self):
        self.current_step = 0

        self.data_env = deepcopy(self.data)
        self.data_env = shuffle(self.data_env)
        self.data_env.reset_index(inplace=True, drop=True)
        col = self.data_env.columns.tolist()+['action']
        self.final_state_data = pd.DataFrame(columns=col)

        self.prev_obs = self.data_env.iloc[self.current_step].tolist()

        return (self.data_env.iloc[self.current_step]).tolist()

    def _update_env(self, action):
        self.prev_obs.append(action)
        self.final_state_data = pd.concat([self.final_state_data, pd.DataFrame(
            [self.prev_obs], columns=self.final_state_data.columns.tolist())], ignore_index=True)

    def step(self, action):

        action = int(action) + 1
        self.current_step += 1
        obs = (self.data_env.iloc[self.current_step]).tolist()

        self._update_env(action)

        if self.current_step >= len(self.data_env.index) - 1:
            done = True
        else:
            done = False

        reward, accuracy = self.R.reward_function(
            self.final_state_data, self.k, self.total_data_size, obs, action, done)

        self.prev_obs = obs

        return obs, reward, done, {'final_state_data': self.final_state_data, 'accuracy': accuracy}

    def render(self, mode='human', close=False):

        print('Step: ', self.current_step)
        print('Current reward, accuracy: ', self.R.reward_function(
            self.final_state_data, self.k, self.total_data_size))
