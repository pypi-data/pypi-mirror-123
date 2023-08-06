from gym.envs.registration import register

register(id='clustering-v0', entry_point='dm_gym.envs.clustering.clustering_env_v0:ClusteringEnv_0',)
register(id='clustering-v1', entry_point='dm_gym.envs.clustering.clustering_env_v1:ClusteringEnv_1',)
register(id='clustering-v2', entry_point='dm_gym.envs.clustering.clustering_env_v2:ClusteringEnv_2',)

#register(id='basic-v2', entry_point='gym_basic.envs:BasicEnv2',)
