"""Multi-agent highway with ramps example.

Trains a non-constant number of agents, all sharing the same policy, on the
highway with ramps network.
"""
import json
import ray
import argparse
try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from ray.rllib.agents.ppo.ppo_tf_policy import PPOTFPolicy
from ray import tune
from ray.tune.registry import register_env
from ray.tune import run_experiments

from flow.controllers import RLController, SimCarFollowingController
from flow.core.params import EnvParams, NetParams, InitialConfig, InFlows, \
                             VehicleParams, SumoParams, \
                             SumoCarFollowingParams, SumoLaneChangeParams

from flow.utils.registry import make_create_env
from flow.utils.rllib import FlowParamsEncoder

from flow.envs.multiagent import MultiAgentHighwayPOEnvMerge4ModifyDistCollaborate
from flow.envs.ring.accel import ADDITIONAL_ENV_PARAMS
from flow.networks import MergeNetwork
from flow.networks.merge import ADDITIONAL_NET_PARAMS
from copy import deepcopy
from flow.visualize.visualizer_util import reset_inflows

EXAMPLE_USAGE = """
example usage:
    python xxxx.py --attr value
"""
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="[Flow] Evaluates a Flow Garden solution on a benchmark.",
    epilog=EXAMPLE_USAGE)
# optional input parameters
parser.add_argument(
    '--avp',
    type=int,
    default=10,
    help="The percentage of autonomous vehicles. value between 0-100")
parser.add_argument(
    '--num_rl',
    type=int,
    default=10,
    help="The percentage of autonomous vehicles. value between 0-100")
parser.add_argument('--handset_inflow', type=int, nargs="+",help="Manually set inflow configurations, notice the order of inflows when they were added to the configuration")
parser.add_argument('--exp_folder_mark', type=str, help="Attach a string to the experiment folder name for easier identification")
parser.add_argument('--preset_inflow', type=int, help="Program inflow to different lane (check visualizer code (add_preset_inflows() in flow/visualize/visualizer_util.py) for the value (0,1,2...).\n \t 0: rl vehicles on the right lane, and no lane change.\n \t 1: rl vehicles on the right lane, and only lane change for human drivers on the left lane. \n\t 2: rl vehicles on the left lane, and only lane change for human drivers on the right lane.")
parser.add_argument('--lateral_resolution', type=float, help='input laterial resolution for lane changing.') 
parser.add_argument('--to_probability', action='store_true', help='input an avp and we will convert it to probability automatically')
#parser.add_argument('--exp_prefix', type=str, help="To name the experiment folder under ray_results with a prefix")
parser.add_argument('--random_inflow', action='store_true')
parser.add_argument(
        '--main_merge_human_inflows',
        type=int,
        nargs="+",
        help="This is often used for evaluating human baseline")

parser.add_argument('--cpu', type=int, help='set the number of cpus used for training')

parser.add_argument('--human_inflows', type=int, nargs="+", help='the human inflows for both lanes.') 
parser.add_argument('--rl_inflows', type=int, nargs="+", help='the rl inflows for both lanes.') 
parser.add_argument('--human_lane_change', type=int, nargs="+", help='the rl inflows for both lanes.') 
parser.add_argument('--rl_lane_change', type=int, nargs="+", help='the rl lane change for right and left lanes.') 
parser.add_argument('--merge_inflow', type=int, help='merge inflow used for multilane highway.') 
parser.add_argument('--aggressive', type=float, help='float value from 0 to 1 to indicate how aggressive the vehicle is.') 
parser.add_argument('--assertive', type=float, help='float value from 0 to 1 to indicate how assertive the vehicle is (lc_assertive in SUMO). Is that between 0 and 1?') 
parser.add_argument('--lc_probability', type=float, help='float value from 0 to 1 to indicate the percentage of human drivers to change lanes in simple merge lane changer') 


args=parser.parse_args()

# SET UP PARAMETERS FOR THE SIMULATION

# number of training iterations
N_TRAINING_ITERATIONS = 500
# number of rollouts per training iteration
N_ROLLOUTS = 30 
# number of steps per rollout
HORIZON = 2000
# number of parallel workers
N_CPUS = 40
if args.cpu:
    N_CPUS=args.cpu

NUM_RL = 10
if args.num_rl:
    NUM_RL=args.num_rl

# inflow rate on the highway in vehicles per hour
FLOW_RATE = 2000
if args.handset_inflow:
    #additional_env_params['handset_inflow']=args.handset_inflow
    FLOW_RATE=args.handset_inflow[0]+args.handset_inflow[1] 
    print("main flow rate:",FLOW_RATE)

# inflow rate on each on-ramp in vehicles per hour
MERGE_RATE = 200
# percentage of autonomous vehicles compared to human vehicles on highway
RL_PENETRATION = 0.1 
if args.avp:
    RL_PENETRATION = (args.avp/100.0) 
# Selfishness constant
ETA_1 = 0.9
ETA_2 = 0.1


# SET UP PARAMETERS FOR THE NETWORK
additional_net_params = deepcopy(ADDITIONAL_NET_PARAMS)
additional_net_params["merge_lanes"] = 1
additional_net_params["highway_lanes"] = 1
additional_net_params["pre_merge_length"] = 500



# SET UP PARAMETERS FOR THE ENVIRONMENT

additional_env_params = ADDITIONAL_ENV_PARAMS.copy()


# CREATE VEHICLE TYPES AND INFLOWS
vehicles = VehicleParams()
inflows = InFlows()

mark=""
if args.exp_folder_mark:
    mark="_"+args.exp_folder_mark

random_prefix="Even"
if args.to_probability==True:
   random_prefix="Random" 
exp_tag_str='{}_modified_state_merge_placement_augmented'.format(random_prefix)+mark+'_merge4_Full_Collaborate_lr_schedule_eta1_{}_eta2_{}'.format(ETA_1, ETA_2)

flow_params = dict(
    exp_tag=exp_tag_str,
    env_name=MultiAgentHighwayPOEnvMerge4RandomMergeModifyDistCollaborate, #MultiAgentHighwayPOEnvMerge4Collaborate,
    network=MergeNetwork,
    simulator='traci',

    #env=EnvParams(
    #    horizon=HORIZON,
    #    warmup_steps=200,
    #    sims_per_step=1,  # do not put more than one #FIXME why do not put more than one
    #    additional_params=additional_env_params,
    #),

    sim=SumoParams(
        restart_instance=True,
        sim_step=0.5,
        render=False,
    ),

    # environment related parameters (see flow.core.params.EnvParams)
    env=EnvParams(
        horizon=HORIZON,
        sims_per_step=1,
        warmup_steps=0,
        additional_params={
            "max_accel": 2.6,
            "max_decel": 4.5,
            "target_velocity": 30,
            "num_rl": NUM_RL,
            "eta1": ETA_1,
            "eta2": ETA_2,
        },
    ),

    net=NetParams(
        inflows=None,
        additional_params=additional_net_params,
    ),

    veh=vehicles,
    initial=InitialConfig(),
)

reset_inflows(args, flow_params)

# SET UP EXPERIMENT

def setup_exps(flow_params):
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
    alg_run = 'PPO'
    agent_cls = get_agent_class(alg_run)
    config = agent_cls._default_config.copy()
    config['num_workers'] = N_CPUS
    config['train_batch_size'] = HORIZON * N_ROLLOUTS
    config['sgd_minibatch_size'] = 4096
    #config['simple_optimizer'] = True
    config['gamma'] = 0.998  # discount rate
    config['model'].update({'fcnet_hiddens': [100, 50, 25]})
    #config['lr'] = tune.grid_search([5e-4, 1e-4])
    config['lr_schedule'] = [
            [0, 5e-4],
            [1000000, 1e-4],
            [4000000, 1e-5],
            [8000000, 1e-6]]
    config['horizon'] = HORIZON
    config['clip_actions'] = False
    config['observation_filter'] = 'NoFilter'
    config["use_gae"] = True
    config["lambda"] = 0.95
    config["shuffle_sequences"] = True
    config["vf_clip_param"] = 1e8
    config["num_sgd_iter"] = 10
    #config["kl_target"] = 0.003
    config["kl_coeff"] = 0.01
    config["entropy_coeff"] = 0.001
    config["clip_param"] = 0.2
    config["grad_clip"] = None
    config["use_critic"] = True
    config["vf_share_layers"] = True
    config["vf_loss_coeff"] = 0.5


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

    return alg_run, env_name, config


# RUN EXPERIMENT

if __name__ == '__main__':
    alg_run, env_name, config = setup_exps(flow_params)
    ray.init(num_cpus=N_CPUS + 1)

    run_experiments({
        flow_params['exp_tag']: {
            'run': alg_run,
            'env': env_name,
            'checkpoint_freq': 5,
            'max_failures': 999,
            'checkpoint_at_end': True,
            'stop': {
                'training_iteration': N_TRAINING_ITERATIONS
            },
            'config': config,
            'num_samples':1,
        },
    })
