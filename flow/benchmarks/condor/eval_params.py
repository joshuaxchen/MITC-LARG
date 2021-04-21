"""Multi-agent highway with ramps example.

Trains a non-constant number of agents, all sharing the same policy, on the
highway with ramps network.
"""
import json
import ray
try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
#from ray.rllib.agents.ppo.ppo_policy import PPOTFPolicy
from ray import tune
from ray.tune.registry import register_env
from ray.tune import run_experiments

from flow.controllers import RLController
from flow.core.params import EnvParams, NetParams, InitialConfig, InFlows, \
                             VehicleParams, SumoParams, \
                             SumoCarFollowingParams, SumoLaneChangeParams

from flow.utils.registry import make_create_env
from flow.utils.rllib import FlowParamsEncoder
from flow.controllers import IDMController, SimCarFollowingController

from flow.envs.multiagent import MultiAgentHighwayPOEnv
from flow.envs.ring.accel import ADDITIONAL_ENV_PARAMS
from flow.networks import HighwayRampsNetwork
from flow.networks.highway_ramps import ADDITIONAL_NET_PARAMS
import numpy as np
import gym
import argparse

#scenarios_dir = '/scratch/cluster/wmacke/MITC/flow/core/kernel/network/debug/cfg'
HORIZON = None
controller = None




# SET UP PARAMETERS FOR THE SIMULATION

# number of training iterations
N_TRAINING_ITERATIONS = 200
# number of rollouts per training iteration
N_ROLLOUTS = 20
# number of parallel workers
N_CPUS = 8

def setup_exps(flow_params, args=None):
    """Create the relevant components of a multiagent RLlib experiment.

    Parameters
    ----------
    flow_params : dict
        input flow-parameters

    Returns
    -------
    str
        name of the training algorithm
    str
        name of the gym environment to be trained
    dict
        training configuration parameters
    """
    if args:
        params = read_params(args.params)
        vehicles = VehicleParams()
        vehicles.add(
            veh_id="human",
            acceleration_controller=(SimCarFollowingController, {}),
            car_following_params=SumoCarFollowingParams(
                speed_mode=9,
            ),
            num_vehicles=5)
        vehicles.add(
            veh_id="rl",
            acceleration_controller=(controller, params),
            car_following_params=SumoCarFollowingParams(
                speed_mode=9,
            ),
            num_vehicles=0)
        flow_params['veh'] = vehicles
    alg_run = 'PPO'
    agent_cls = get_agent_class(alg_run)
    config = agent_cls._default_config.copy()
    config['num_workers'] = N_CPUS
    config['train_batch_size'] = HORIZON * N_ROLLOUTS
    config['simple_optimizer'] = True
    config['gamma'] = 0.999  # discount rate
    config['model'].update({'fcnet_hiddens': [32, 32]})
    config['lr'] = tune.grid_search([1e-5])
    config['horizon'] = HORIZON
    config['clip_actions'] = False
    config['observation_filter'] = 'NoFilter'

    # save the flow params for replay
    flow_json = json.dumps(
        flow_params, cls=FlowParamsEncoder, sort_keys=True, indent=4)
    config['env_config']['flow_params'] = flow_json
    config['env_config']['run'] = alg_run

    create_env, env_name = make_create_env(params=flow_params, version=0)

    # register as rllib env
    register_env(env_name, create_env)

    # multiagent configuration
    temp_env = create_env()
    """
    policy_graphs = {'av': (PPOTFPolicy,
                            temp_env.observation_space,
                            temp_env.action_space,
                            {})}

    def policy_mapping_fn(_):
        return 'av'

    config.update({
        'multiagent': {
            'policies': policy_graphs,
            'policy_mapping_fn': tune.function(policy_mapping_fn),
            'policies_to_train': ['av']
        }
    })
    """

    return alg_run, env_name, config

def read_params(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    params = {}
    for l in lines:
        s = l.split('\t')
        params[s[0]] = float(s[-1][:-1])
    #print(params)
    return params


# RUN EXPERIMENT

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='Output File')
    parser.add_argument('--params', type=str, help='IDM Parameters File')
    parser.add_argument(
        "--benchmark_name", type=str, help="File path to solution environment.")
    parser.add_argument(
            "--controller_name", type=str, help='name of controller')
    args = parser.parse_args()
    print(args.output)
    print(args.params)
    print(args.benchmark_name)
    print(args.controller_name)
    benchmark = __import__(
        "flow.benchmarks.%s" % args.benchmark_name, fromlist=["flow_params"])
    flow_params = benchmark.flow_params
    flow_params['env_name']=MultiAgentHighwayPOEnv
    HORIZON = benchmark.HORIZON

    controller_class = __import__('flow.benchmarks.condor.es_controllers.%s' % args.controller_name, fromlist=["Controller"])

    controller = controller_class.Controller


    alg_run, env_name, config = setup_exps(flow_params, args)
    env = gym.make(env_name)
    env.restart_simulation(sim_params=flow_params['sim'], render=False)
    mean_vel = []
    std_vel = []
    final_inflows = []
    final_outflows = []
    times = []
    for i in range(30):
        print(f"Rollout: {i}")
        vel = []
        state = env.reset()
        time = 0
        for _ in range(HORIZON):
            vehicles = env.unwrapped.k.vehicle
            veh_vel = vehicles.get_speed(vehicles.get_ids())
            if len(veh_vel) > 0:
                vel.append(np.mean(veh_vel))
            state, reward, done, _ = env.step({})
            time += 1
            if done['__all__']:
                break
        mean_vel.append(np.mean(vel))
        std_vel.append(np.std(vel))
        final_inflows.append(vehicles.get_inflow_rate(500))
        final_outflows.append(vehicles.get_outflow_rate(500))
        times.append(time)
    #print(np.mean(final_outflows))
    if args.output:
        with open(args.output, 'w') as f:
            f.write(str(np.mean(final_outflows)))


