
import ray
from flow.utils.rllib import get_rllib_config, get_rllib_pkl
from flow.utils.rllib import get_flow_params
from flow.utils.registry import make_create_env
from ray.tune.registry import register_env,get_trainable_cls
try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class

from ray.rllib.agents.callbacks import DefaultCallbacks

class MyCallbacks(DefaultCallbacks):
    def on_episode_start(self, worker, base_env, policies, episode, **kwargs):
        # save env state when an episode starts
        env = base_env.get_unwrapped()[0]
        state = env.get_state()
        episode.user_data["initial_state"] = state

def init_policy_agent(result_dir, checkpoint):
    print("load trained dir:",result_dir)
    config=get_rllib_config(result_dir)
    config['callbacks'] = MyCallbacks
    config['num_workers'] = 0
    if config.get('multiagent',{}).get('policies', None):
        pkl=get_rllib_pkl(result_dir)
        config['multiagent'] = pkl['multiagent']
    else:
        import sys
        sys.exit(-1)
    config_run=config['env_config']['run']
    flow_params = get_flow_params(config)
    create_env, env_name = make_create_env(params=flow_params, version=0)
    register_env(env_name, create_env)
    agent_cls = get_trainable_cls(config_run)
    agent = agent_cls(env=env_name, config=config) 
    agent.restore(checkpoint)
    #accel_agent=agent
    #accel_policy=agent.get_policy("av")
    #print(accel_agent)
    #print(accel_policy)
    #accel_agent=ray.put(agent)
    #accel_policy=ray.put(agent.get_policy("av"))
    #print("ref:",accel_agent)
    return agent 

