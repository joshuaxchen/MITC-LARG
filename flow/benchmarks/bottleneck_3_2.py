"""Benchmark for merge0.

Trains a small percentage of autonomous vehicles to dissipate shockwaves caused
by merges in an open network. The autonomous penetration rate in this example
is 0%.

# Not relevant with 0 RL agents? Action Dimension: (5, )

# Not relevant with 0 RL agents? Observation Dimension: (25, )

Horizon: 750 steps
"""

from copy import deepcopy
from flow.envs import MergePOEnv
from flow.networks import BottleneckNetwork3to2
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams, \
    InFlows, SumoCarFollowingParams
from flow.core.params import VehicleParams, SumoCarFollowingParams, SumoLaneChangeParams
from flow.controllers import SimCarFollowingController, RLController, IDMController, SimLaneChangeController
import os

# time horizon of a single rollout
HORIZON = 6000  # divide by sim_step to get total simulation time. 1000 seconds seems too long since usually there's a crash between two humans, so RL might prefer to do things that extend simulation and not necessarily reducing congestion(that's a hypothesis).
# inflow rate at the highway
FLOW_RATE = 3600 #2000
# percent of autonomous vehicles
RL_PENETRATION = 0.1
# num_rl term (see ADDITIONAL_ENV_PARAMs)
NUM_RL = 20 # hopefully up to 20 RL cars (this is the output of the network)

# We consider a highway network with an upstream merging lane producing
# shockwaves
# is the following OK

# RL vehicles constitute 5% of the total number of vehicles
#
# Here vehicles are defined similarly to in stabilizing_i696.py
vehicles = VehicleParams()
vehicles.add(
    veh_id="human",
    #acceleration_controller=(SimCarFollowingController, {}),
    acceleration_controller=(IDMController, {
        #"noise": 0.2
    }),
    lane_change_controller=(SimLaneChangeController, {}),
    #routing_controller=(ContinuousRouter, {}),
    car_following_params=SumoCarFollowingParams(
      # Define speed mode that will minimize collisions: https://sumo.dlr.de/wiki/TraCI/Change_Vehicle_State#speed_mode_.280xb3.29
      speed_mode="right_of_way", #"all_checks", #no_collide",
      decel=7.5,  # avoid collisions at emergency stops 
      # desired time-gap from leader
      tau=1.5, #7,
      min_gap=2.5,
      speed_factor=1,
      speed_dev=0.1
    ),
    lane_change_params=SumoLaneChangeParams(
      model="SL2015",
      # Define a lane changing mode that will allow lane changes
      # See: https://sumo.dlr.de/wiki/TraCI/Change_Vehicle_State#lane_change_mode_.280xb6.29
      # and: ~/local/flow_2019_07/flow/core/params.py, see LC_MODES = {"aggressive": 0 /*bug, 0 is no lane-changes*/, "no_lat_collide": 512, "strategic": 1621}, where "strategic" is the default behavior
      lane_change_mode=1621,#0b011000000001, # (like default 1621 mode, but no lane changes other than strategic to follow route, # 512, #(collision avoidance and safety gap enforcement) # "strategic", 
      lc_speed_gain=1000000,
      lc_pushy=0, #0.5, #1,
      lc_assertive=1.5, #1, #2, #0.1, #5, #20, ## 1.5 seems more natural from the numbers here
      # the following two replace default values which are not read well by xml parser
      lc_impatience=1e-8,
      lc_time_to_impatience=1e12
    ), 
    num_vehicles=0)
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
      tau=1.5, #7,
      min_gap=2.5,
      speed_factor=1,
      speed_dev=0.1
    ),
    lane_change_params=SumoLaneChangeParams(
      model="SL2015",
      # Define a lane changing mode that will allow lane changes
      # See: https://sumo.dlr.de/wiki/TraCI/Change_Vehicle_State#lane_change_mode_.280xb6.29
      # and: ~/local/flow_2019_07/flow/core/params.py, see LC_MODES = {"aggressive": 0 /*bug, 0 is no lane-changes*/, "no_lat_collide": 512, "strategic": 1621}, where "strategic" is the default behavior
      lane_change_mode=0, #0b011000000001, # (like default 1621 mode, but no lane changes other than strategic to follow route, # 512, #(collision avoidance and safety gap enforcement) # "strategic", 
      lc_speed_gain=1000000,
      lc_pushy=0, #0.5, #1,
      lc_assertive=1.5, #1, #2, #0.1, #5, #20, ## 1.5 seems more natural from the numbers here
      # the following two replace default values which are not read well by xml parser
      lc_impatience=1e-8,
      lc_time_to_impatience =1e12
    ), 
    num_vehicles=0)

# Vehicles are introduced from both sides of merge, with RL vehicles entering
# from the highway portion as well
inflow = InFlows()
inflow.add(
    veh_type="human",
    edge="inflow_highway",
    begin=10,#0,
    end=90000,
    probability=(1 - RL_PENETRATION), #* FLOW_RATE,
    #vehs_per_hour= 1 * FLOW_RATE,
    depart_speed=30, #"random", #30, #"max",
    depart_lane="random", #"free", 
    )
inflow.add(
    veh_type="rl",
    edge="inflow_highway",
    begin=10,#0,
    end=90000,
    probability=RL_PENETRATION, # * 0.8, #* FLOW_RATE,
    depart_speed=30, #"random", #30, #"max",
    depart_lane=0, #"random", #"free",
    )

flow_params = dict(
    # name of the experiment
    exp_tag="bottleneck_3_2",

    # name of the flow environment the experiment is running on
    env_name=MergePOEnv,

    # name of the scenario class the experiment is running on
    network=BottleneckNetwork3to2, #"Scenario", # Scenario is for xml template, but has some bug with internal edges that don't appear. Fixed it in BottleneckNetwork3to2

    # simulator that is used by the experiment
    simulator='traci',

    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=SumoParams(
        #emission_path="/home/dzgnkq/ray_results/straight_multilane_baseline/",
        no_step_log=False,       # this disables log writing?
        sim_step=0.1, #0.25, #0.5,
        lateral_resolution=0.25, # determines lateral discretization of lanes
        render=True, #False, #True, #False,
        restart_instance=True,
    ),

    # environment related parameters (see flow.core.params.EnvParams)
    env=EnvParams(
        horizon=HORIZON,
        sims_per_step=5,
        warmup_steps=0,
        additional_params={
            "max_accel": 1.5,
            "max_decel": 1.5,
            "target_velocity": 20,
            "num_rl": NUM_RL,
        },
    ),

    # network-related parameters (see flow.core.params.NetParams and the
    # scenario's documentation or ADDITIONAL_NET_PARAMS component)
    net=NetParams(
        ## template had a bug of missing internal edges so when vehicle is on a zipper it doesn't have an "edge" and it's stuck
        #template= {
        #  "net" : os.path.join(os.path.dirname(os.path.abspath(__file__)), "bottleneck_3_2.net.xml"),
        #  "rou" : os.path.join(os.path.dirname(os.path.abspath(__file__)), "bottleneck_3_2.rou.xml")
        #},
        inflows=inflow,
        #no_internal_links=False,
        additional_params = {"scaling" : 1, "speed_limit": 30} 
    ),

    # vehicles to be placed in the network at the start of a rollout (see
    # flow.core.vehicles.Vehicles)
    veh=vehicles,

    # parameters specifying the positioning of vehicles upon initialization/
    # reset (see flow.core.params.InitialConfig)
    initial=InitialConfig(),
)
