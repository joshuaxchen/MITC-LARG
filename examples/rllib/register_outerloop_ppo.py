import ray
try:
    from ray.rllib.agents.agent import ALGORITHMS
except ImportError:
    from ray.rllib.agents.registry import ALGORITHMS

def _import_outerloop_ppo():
    from examples.rllib import outerloop_ppo
    return outerloop_ppo.outerloop_PPOTrainer#, outerloop_ppo.DEFAULT_CONFIG

def register_outerloop_ppo():
    ALGORITHMS["Outerloop-PPO"]=_import_outerloop_ppo        

