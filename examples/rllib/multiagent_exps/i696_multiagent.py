"""Multi-agent highway with ramps example.

Trains a non-constant number of agents, all sharing the same policy, on the
highway with ramps network.
"""
import json
import ray
import os
try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from ray.rllib.agents.ppo.ppo_tf_policy import PPOTFPolicy
from ray import tune
from ray.tune.registry import register_env
from ray.tune import run_experiments
from flow.networks import Network
from flow.controllers import SimCarFollowingController,IDMController, RLController, SimLaneChangeController, ContinuousRouter

from flow.core.params import EnvParams, NetParams, InitialConfig, InFlows, \
                             VehicleParams, SumoParams, \
                             SumoCarFollowingParams, SumoLaneChangeParams

from flow.utils.registry import make_create_env
from flow.utils.rllib import FlowParamsEncoder

from flow.envs.multiagent import MultiAgentI696POEnvParameterizedWindowSizeCollaborate
from flow.envs.ring.accel import ADDITIONAL_ENV_PARAMS
from flow.networks import MergeNetwork
from flow.networks.merge import ADDITIONAL_NET_PARAMS
from copy import deepcopy
from flow.controllers import IDMController
from flow.visualize.visualizer_util import reset_inflows, set_argument

# SET UP PARAMETERS FOR THE SIMULATION
args=set_argument()

if args.window_size is not None:
    if len(args.window_size)!=2:
        print("The window size has to be two elements: the left distance to the junction, and the right distance to the junction")
        exit(-1)

# SET UP PARAMETERS FOR THE SIMULATION

# number of training iterations
N_TRAINING_ITERATIONS = 1#500
# number of rollouts per training iteration
N_ROLLOUTS = 30 
# number of steps per rollout
HORIZON = 2000
# number of parallel workers
N_CPUS = 1
if args.cpu:
    N_CPUS=args.cpu

NUM_RL = 30
# inflow rate on the highway in vehicles per hour
FLOW_RATE = 2000
# inflow rate on each on-ramp in vehicles per hour
MERGE_RATE = 200
# percentage of autonomous vehicles compared to human vehicles on highway
RL_PENETRATION = 0.1
ETA_1 = 0.9
ETA_2 = 0.1


window_size=tuple(args.window_size)

# SET UP PARAMETERS FOR THE NETWORK
additional_net_params = deepcopy(ADDITIONAL_NET_PARAMS)
from flow.scenarios import scenario_dir_path
scenarios_dir = scenario_dir_path
#from flow.scenarios import scenario_dir_path
scenarios_dir = scenario_dir_path
scenario_road_data = {"name" : "I696_ONE_LANE",
            "net" : os.path.join(scenarios_dir, 'i696', 'i696-three-merges.net.xml'), 
            #"net" : os.path.join(scenarios_dir, 'i696', 'osm.net.i696_onelane.xml'), 
            #"rou" : [os.path.join(scenarios_dir, 'i696', 'i696.rou.xml')],
            "rou" : [os.path.join(scenarios_dir, 'i696', 'i696.three.merges.rou.xml')],
            #"rou" : [os.path.join(scenarios_dir, 'i696', 'text.xml')],
            #"rou" : [os.path.join(scenarios_dir, 'i696', 'i696.rou.i696_onelane_Evenshorter.xml')],
            "edges_distribution" : ["59440544#0", "124433709.427", "8666737", "178253095"] 
            }



# SET UP PARAMETERS FOR THE ENVIRONMENT

additional_env_params = ADDITIONAL_ENV_PARAMS.copy()



# CREATE VEHICLE TYPES AND INFLOWS

vehicles = VehicleParams()
# human vehicles
vehicles.add(
    veh_id="human",
    acceleration_controller=(IDMController, {}), #SimCarFollowingController
    car_following_params=SumoCarFollowingParams(
        speed_mode=15,  # for safer behavior at the merges
        #tau=1.5  # larger distance between cars
    ),
    #lane_change_params=SumoLaneChangeParams(lane_change_mode=1621)
    num_vehicles=0)

# autonomous vehicles
vehicles.add(
    veh_id="rl",
    acceleration_controller=(RLController, {}),
    car_following_params=SumoCarFollowingParams(
        speed_mode=9,
    ),
    num_vehicles=0)


# Vehicles are introduced from both sides of merge, with RL vehicles entering
# from the highway portion as well
inflow = InFlows()

inflow.add(
    veh_type="rl",
    edge="59440544#0", # flow id sw2w1 from xml file
    begin=10,#0,
    end=90000,
    vehs_per_hour = RL_PENETRATION * FLOW_RATE,
    departSpeed=7.5,
    depart_lane="free",
    )
#"404969345#0", "124433709.427", "8666737", "178253095"
inflow.add(
    veh_type="human",
    edge="59440544#0", # flow id se2w1 from xml file
    begin=10,#0,
    end=90000,
    vehs_per_hour = (1 - RL_PENETRATION)*FLOW_RATE,
    departSpeed=10,
    departLane="free",
    )
inflow.add(
    veh_type="human",
    edge="8666737", # flow id se2w1 from xml file
    begin=10,#0,
    end=90000,
    vehs_per_hour = 200, #(1 - RL_PENETRATION)*FLOW_RATE,
    departSpeed=10,
    departLane="free",
    )
inflow.add(
    veh_type="human",
    edge="178253095", # flow id se2w1 from xml file
    begin=10,#0,
    end=90000,
    vehs_per_hour = 200, #(1 - RL_PENETRATION)*FLOW_RATE,
    departSpeed=10,
    departLane="free",
    )
inflow.add(
    veh_type="human",
    edge="124433709.427", # flow id se2w1 from xml file
    begin=10,#0,
    end=90000,
    vehs_per_hour = 200, #(1 - RL_PENETRATION)*FLOW_RATE,
    departSpeed=10,
    departLane="free",
    )

mark=""
if args.exp_folder_mark:
    mark="_"+args.exp_folder_mark

exp_tag_str='multiagent'+mark+'_i696_Full_Collaborate_lr_schedule_eta1_{}_eta2_{}'.format(ETA_1, ETA_2)


flow_params = dict(
    exp_tag=exp_tag_str, #'multiagent_highway_i696_1merge_Collaborate_lrschedule'
    env_name=MultiAgentI696POEnvParameterizedWindowSizeCollaborate,
    network=Network, #MergeNetwork,
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
        sims_per_step=2, #5,
        warmup_steps=0,
        additional_params={
            "max_accel": 2.6,
            "max_decel": 4.5,
            "target_velocity": 30,
            "num_rl": NUM_RL, # used by WaveAttenuationMergePOEnv e.g. to fix action dimension
            "eta1": ETA_1,
            "eta2": ETA_2,
            "window_size": window_size
            #"max_inflow":FLOW_RATE + 3*MERGE_RATE,
        },
    ),
    net=NetParams(
        inflows=inflow,
        #no_internal_links=False,
        additional_params=additional_net_params,
        template={
          "net" : scenario_road_data["net"],# see above
          "rou" : scenario_road_data["rou"],# see above 
        }
    ),


    veh=vehicles,
    initial=InitialConfig(
      # Distributing only at the beginning of routes
      scenario_road_data["edges_distribution"]
    ),

)


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
            'checkpoint_freq': 1,
            'checkpoint_at_end': True,
            'stop': {
                'training_iteration': N_TRAINING_ITERATIONS
            },
            'config': config,
            'restore': args.restore,
            'num_samples':1,
        },
    })
