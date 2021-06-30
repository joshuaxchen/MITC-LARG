"""Open merge example.

Trains a a small percentage of rl vehicles to dissipate shockwaves caused by
merges in an open network.
"""
import json
import os
import random
import numpy as np
import pickle
from argparse import ArgumentParser

import ray
try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from ray import tune
from ray.tune import run_experiments
from ray.tune.registry import register_env

from ray.rllib.agents.ppo.ppo_policy import PPOTFPolicy

from flow.envs import MergePOEnv
from flow.networks import Network
from flow.utils.registry import make_create_env
from flow.utils.rllib import FlowParamsEncoder
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams, \
    InFlows, SumoCarFollowingParams
#from flow.envs.multiagent.highway import MultiAgentHighwayPOEnvLocalRewardNewStates, MultiAgentHighwayPOEnvLocalReward
from flow.scenarios.merge import ADDITIONAL_NET_PARAMS
from flow.core.params import VehicleParams, SumoLaneChangeParams
from flow.controllers import IDMController, RLController, SimLaneChangeController, ContinuousRouter, SimCarFollowingController, CFMController, BCMController, LACController, OVMController
import gym

# TODO hard coded
#scenarios_dir = os.path.join(os.path.expanduser("~/"), 'local', 'flow_2019_07', 'flow', 'scenarios')
scenarios_dir = '/home/flow/Documents/MITC/flow/scenarios/'

# UNCOMMENT ONE OF THE FOLLOWING 3 VARIATIONS OF I696 SCENARIO 
#
#one-lane (no lane-changes), smaller
####################################
#scenario_road_data = {"name" : "I696_ONE_LANE_CROPPED",
#            "net" : os.path.join(scenarios_dir, 'i696', 'osm.net.i696_onelane_cropped.xml'), 
#            "rou" : [os.path.join(scenarios_dir, 'i696', 'i696.rou.i696_onelane_cropped.xml')],
#            "edges_distribution" : ["8666737", "124433709", "491266613", "404969345#1"] 
#            }
#
#one-lane (no lane-changes)
###########################
scenario_road_data = {"name" : "I696_ONE_LANE",
            "net" : os.path.join(scenarios_dir, 'i696', 'osm.net.i696_onelane.xml'), 
            "rou" : [os.path.join(scenarios_dir, 'i696', 'i696.rou.xml')],
            "edges_distribution" : ["404969345#0", "59440544#0", "124433709", "38726647"] 
            }
#
#the full I696 test
###################
#scenario_road_data = {"name" : "I696_FULL",
#            "net" : os.path.join(scenarios_dir, 'i696', 'osm.net.xml'), 
#            "rou" : [os.path.join(scenarios_dir, 'i696', 'i696.rou.xml')],
#            "edges_distribution" : ["404969345#0", "59440544#0", "124433709", "38726647"] 
#            }
            

# experiment number
# - 0: 10% RL penetration,  5 max controllable vehicles
# - 1: 25% RL penetration, 13 max controllable vehicles
# - 2: 33% RL penetration, 17 max controllable vehicles
EXP_NUM = 0

# time horizon of a single rollout
HORIZON = 2000 #128#600
# number of rollouts per training iteration
N_ROLLOUTS = 20#1#20
# number of parallel workers
N_CPUS = 8#1#8#2

# inflow rate at the highway
FLOW_RATE = 1500
MERGE_RATE = 160
# percent of autonomous vehicles
RL_PENETRATION = 0
# num_rl term (see ADDITIONAL_ENV_PARAMs)
#NUM_RL = [5, 13, 17][EXP_NUM]
NUM_RL = [0, 250, 333][EXP_NUM]

## We consider a highway network with an upstream merging lane producing
# shockwaves
def build_flow_params(args):
    additional_net_params = ADDITIONAL_NET_PARAMS.copy()
    #additional_net_params["merge_lanes"] = 1
    #additional_net_params["highway_lanes"] = 1
    #additional_net_params["pre_merge_length"] = 500
    
    # RL vehicles constitute 5% of the total number of vehicles
    # Daniel: adding vehicles and flow from osm.passenger.trips.xml
    vehicles = VehicleParams()
    vehicles.add(
        veh_id="human",
        acceleration_controller=(IDMController, {
            "noise": 0.2
        }),
        lane_change_controller=(SimLaneChangeController, {}),
        #routing_controller=(ContinuousRouter, {}),
        car_following_params=SumoCarFollowingParams(
          # Define speed mode that will minimize collisions: https://sumo.dlr.de/wiki/TraCI/Change_Vehicle_State#speed_mode_.280xb3.29
          speed_mode="obey_safe_speed", #"all_checks", #no_collide",
          decel=7.5,  # avoid collisions at emergency stops 
          # desired time-gap from leader
          tau=2, #7,
          min_gap=0,
          #min_gap=2.5,
          speed_factor=1,
          speed_dev=0.1
        ),
        lane_change_params=SumoLaneChangeParams(
          model="SL2015",
          # Define a lane changing mode that will allow lane changes
          # See: https://sumo.dlr.de/wiki/TraCI/Change_Vehicle_State#lane_change_mode_.280xb6.29
          # and: ~/local/flow_2019_07/flow/core/params.py, see LC_MODES = {"aggressive": 0 /*bug, 0 is no lane-changes*/, "no_lat_collide": 512, "strategic": 1621}, where "strategic" is the default behavior
          lane_change_mode=1621,#0b011000000001, # (like default 1621 mode, but no lane changes other than strategic to follow route, # 512, #(collision avoidance and safety gap enforcement) # "strategic", 
          #lc_speed_gain=1000000,
          lc_pushy=0, #0.5, #1,
          lc_assertive=5, #20,
          # the following two replace default values which are not read well by xml parser
          lc_impatience=1e-8,
          lc_time_to_impatience=1e12
        ), 
        num_vehicles=0)
    """
    vehicles.add(
        veh_id="rl",
        acceleration_controller=(RLController, {}),
        lane_change_controller=(SimLaneChangeController, {}),
        #routing_controller=(ContinuousRouter, {}),
        car_following_params=SumoCarFollowingParams(
          # Define speed mode that will minimize collisions: https://sumo.dlr.de/wiki/TraCI/Change_Vehicle_State#speed_mode_.280xb3.29
          speed_mode="right_of_way", #"all_checks", #no_collide",
          decel=7.5,  # avoid collisions at emergency stops 
          # desired time-gap from leader
          tau=2, #7,
          min_gap=0,
          #min_gap=2.5,
          speed_factor=1,
          speed_dev=0.1
        ),
        lane_change_params=SumoLaneChangeParams(
          model="SL2015",
          # Define a lane changing mode that will allow lane changes
          # See: https://sumo.dlr.de/wiki/TraCI/Change_Vehicle_State#lane_change_mode_.280xb6.29
          # and: ~/local/flow_2019_07/flow/core/params.py, see LC_MODES = {"aggressive": 0 /*bug, 0 is no lane-changes*/, "no_lat_collide": 512, "strategic": 1621}, where "strategic" is the default behavior
          lane_change_mode=1621,#0b011000000001, # (like default 1621 mode, but no lane changes other than strategic to follow route, # 512, #(collision avoidance and safety gap enforcement) # "strategic", 
          #lc_speed_gain=1000000,
          lc_pushy=0, #0.5, #1,
          lc_assertive=5, #20,
          # the following two replace default values which are not read well by xml parser
          lc_impatience=1e-8,
          lc_time_to_impatience=1e12
        ), 
        num_vehicles=0)
        """
    
    # Vehicles are introduced from both sides of merge, with RL vehicles entering
    # from the highway portion as well
    inflow = InFlows()
    inflow.add(
        veh_type="human",
        edge="404969345#0", # flow id sw2w1 from xml file
        begin=10,#0,
        end=90000,
        #probability=(1 - RL_PENETRATION), #* FLOW_RATE,
        vehs_per_hour=args.merge_rate,
        depart_speed="max",
        depart_lane="free",
        )
    inflow.add(
        veh_type="human",
        edge="59440544#0", # flow id se2w1 from xml file
        begin=10,#0,
        end=90000,
        #probability=(1 - RL_PENETRATION), #* FLOW_RATE,
        vehs_per_hour=args.flow_rate, #* FLOW_RATE,
        depart_speed="max",
        depart_lane="free",
        )
    inflow.add(
        veh_type="human",
        edge="124433709", # flow id e2w1 from xml file
        begin=10,#0,
        end=90000,
        #probability=(1 - RL_PENETRATION), #* FLOW_RATE,
        vehs_per_hour=args.merge_rate,
        depart_speed="max",
        depart_lane="free",
        )
    '''
    inflow.add(
        veh_type="rl",
        edge="124433709", # flow id e2w1 from xml file
        begin=10,#0,
        end=90000,
        probability=RL_PENETRATION, # * 0.8, # * FLOW_RATE,
        depart_speed="max",
        depart_lane="free",
        )
    '''
    inflow.add(
        veh_type="human",
        edge="38726647", # flow id n2w1 from xml file
        begin=10,#0,
        end=90000,
        #probability=(1 - RL_PENETRATION), # * FLOW_RATE,
        vehs_per_hour = args.merge_rate,
        depart_speed="max",
        depart_lane="free",
        )
    '''
    inflow.add(
        veh_type="rl",
        edge="38726647", # flow id n2w1 from xml file
        begin=10,#0,
        end=90000,
        probability=RL_PENETRATION, # * 0.8, # * FLOW_RATE,
        depart_speed="max",
        depart_lane="free",
        )
    '''
    
    
    flow_params = dict(
        # name of the experiment
        exp_tag="multiagent_i696_newParams",
    
        # name of the flow environment the experiment is running on
        env_name=MergePOEnv,
    
        # name of the scenario class the experiment is running on
        network=Network,
    
        # simulator that is used by the experiment
        simulator='traci',
    
        # sumo-related parameters (see flow.core.params.SumoParams)
        sim=SumoParams(
            no_step_log=False,       # this disables log writing?
            sim_step=0.2,            # Daniel updated from osm.sumocfg
            lateral_resolution=0.25, # determines lateral discretization of lanes
            render=True,#True,             # False for training, True for debugging
            restart_instance=True,
        ),
    
        # environment related parameters (see flow.core.params.EnvParams)
        env=EnvParams(
            horizon=HORIZON,
            sims_per_step=1, #5,
            warmup_steps=args.warmup,
            additional_params={
                "max_accel": 9,
                "max_decel": 9,
                "target_velocity": 20,
                "num_rl": NUM_RL, # used by WaveAttenuationMergePOEnv e.g. to fix action dimension
            },
        ),
    
        # network-related parameters (see flow.core.params.NetParams and the
        # scenario's documentation or ADDITIONAL_NET_PARAMS component)
        net=NetParams(
            inflows=inflow,
            #no_internal_links=False,
            additional_params=additional_net_params,
            template={
              "net" : scenario_road_data["net"],# see above
              "rou" : scenario_road_data["rou"],# see above 
            }
        ),
    
        # vehicles to be placed in the network at the start of a rollout (see
        # flow.core.params.VehicleParams)
        veh=vehicles,
    
        # parameters specifying the positioning of vehicles upon initialization/
        # reset (see flow.core.params.InitialConfig)
        initial=InitialConfig(
          # Distributing only at the beginning of routes 
          scenario_road_data["edges_distribution"]
        ),
    )
    return flow_params

def setup_exps(seeds_file=None, args = None):

    flow_params = build_flow_params(args)

    alg_run = "PPO"

    agent_cls = get_agent_class(alg_run)
    config = agent_cls._default_config.copy()
    config["num_workers"] = N_CPUS
    config["train_batch_size"] = HORIZON * N_ROLLOUTS
    config["gamma"] = 0.999  # discount rate
    config["model"].update({"fcnet_hiddens": [32, 32, 32]})
    config["use_gae"] = True
    config["lambda"] = 0.97
    config["kl_target"] = 0.02
    config["num_sgd_iter"] = 10
    config['clip_actions'] = False  # FIXME(ev) temporary ray bug
    config["horizon"] = HORIZON

    # save the flow params for replay
    flow_json = json.dumps(
        flow_params, cls=FlowParamsEncoder, sort_keys=True, indent=4)
    config['env_config']['flow_params'] = flow_json
    config['env_config']['run'] = alg_run

    create_env, gym_name = make_create_env(params=flow_params, version=0, seeds_file=seeds_file)

    # Register as rllib env
    register_env(gym_name, create_env)

    temp_env = create_env()
    policy_graphs = {'av': (PPOTFPolicy, temp_env.observation_space,
                            temp_env.action_space,
                            {})}

    def policy_mapping_fn(_):
        return 'av'

    config.update({
        'multiagent': {
            'policies': policy_graphs,
            'policy_mapping_fn': tune.function(policy_mapping_fn),
            'policies_to_train':['av']
            }
        })

    return alg_run, gym_name, config, flow_params


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-s", "--seeds_file", dest="seeds_file",
                        help="pickle file containing seeds", default=None)
    parser.add_argument('-o', '--output', help='output file')
    parser.add_argument('--flow_rate', type=int, help='flow rate')
    parser.add_argument('--merge_rate', type=int, help='merge rate')
    parser.add_argument('--warmup', type=int, help='warmup')
    args = parser.parse_args()

    alg_run, gym_name, config, flow_params = setup_exps(args.seeds_file, args)

    env = gym.make(gym_name)
    env.restart_simulation(sim_params=flow_params['sim'], render=False)
    mean_vel = []
    std_vel = []
    final_inflows = []
    final_outflows = []
    for i in range(1):
        print(f"Rollout: {i}")
        vel = []
        state = env.reset()
        for _ in range(HORIZON):
            print(_)
            vehicles = env.unwrapped.k.vehicle
            veh = vehicles.get_ids()
            if len(veh) > 0:
                vel.append(np.mean(vehicles.get_speed(veh)))
            state, reward, done, _ = env.step({})
        mean_vel.append(np.mean(vel))
        std_vel.append(np.std(vel))
        final_inflows.append(vehicles.get_inflow_rate(500))
        final_outflows.append(vehicles.get_outflow_rate(500))
    if args.output:
        np.savetxt(args.output, [mean_vel, std_vel, final_inflows, final_outflows])
