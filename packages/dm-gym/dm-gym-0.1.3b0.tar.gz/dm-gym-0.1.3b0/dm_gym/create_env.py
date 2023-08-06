import gym


def ray_create_env(config, *args, **kwargs):

    if type(config) == dict:
        env_name = config['env']
    else:
        env_name = config
    if env_name == 'clustering-v0':
        from dm_gym.envs.clustering_env_v0 import ClusteringEnv_0 as env
    elif env_name == 'clustering-v1':
        from dm_gym.envs.clustering_env_v1 import ClusteringEnv_1 as env
    else:
        raise NotImplementedError(
            'Environment {} not recognized.'.format(env_name))
    return env


def create_env(name, *args, **kwargs):
    if name == "clustering-v0":
        env = gym.make("dm_gym:clustering-v0", **kwargs)
    elif name == "clustering-v1":
        env = gym.make("dm_gym:clustering-v1", **kwargs)
    else:
        raise NotImplementedError(
            'Environment {} not recognized.'.format(name))

    return env
