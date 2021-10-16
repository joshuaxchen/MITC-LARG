from flow.controllers import IDMController, RLController, SimCarFollowingController
from flow.core.params import EnvParams, NetParams, InitialConfig, InFlows, \
                             VehicleParams, SumoParams, \
                             SumoCarFollowingParams, SumoLaneChangeParams
from flow.envs.multiagent.highway_MOR import MultiAgentHighwayPOEnvMerge4CollaborateMOR

from flow.controllers import SimLaneChangeController,SimpleMergeLaneChanger
import sys

LANE_CHANGE_REPECT_COLLISION_AVOID_AND_SAFETY_GAP=1621
LANE_CHANGE_REPECT_COLLISION_AVOID=1365
LANE_CHANGE_NO_REPECT_OTHERS=1109
LANE_CHANGE_OVERRIDING=2218
NO_LANE_CHANGE_COLLISION_AVOID_SAFETY_GAP_CHECK=512

LANE_CHANGE_MODE=LANE_CHANGE_REPECT_COLLISION_AVOID_AND_SAFETY_GAP #LANE_CHANGE_REPECT_COLLISION_AVOID#LANE_CHANGE_REPECT_COLLISION_AVOID_AND_SAFETY_GAP #LANE_CHANGE_NO_REPECT_OTHERS##LANE_CHANGE_NO_REPECT_OTHERS
NO_LANE_CHANGE_MODE=NO_LANE_CHANGE_COLLISION_AVOID_SAFETY_GAP_CHECK


def add_vehicles(vehicles, veh_type, lane_change_mode, speed_mode, num_vehicles, aggressive, assertive, lc_probability):                
    controller=None
    if "rl" in veh_type:
        controller=RLController
    elif "human" in veh_type:
        controller=IDMController #SimCarFollowingController#IDMController #

    my_lane_change_controller=(SimLaneChangeController, {})
    #if lc_probability >=0 and lc_probability <=1: # -1 probability indicating SUMO lane change controller, otherwise it indicates a simple merge lane changer
    #    simple_merge_lane_change={'lane_change_region_start_loc': 100, 'lane_change_region_end_loc': 600, 'lane_change_probability':lc_probability}
    #    my_lane_change_controller=(SimpleMergeLaneChanger, {'lane_change_params':simple_merge_lane_change})

    # CREATE VEHICLE TYPES AND INFLOWS
    # FIXME temporary fix; will change later 
    speed_gain = aggressive
    vehicles.add(
            veh_id=veh_type,
            acceleration_controller=(controller, {}),
            lane_change_controller=my_lane_change_controller,
            car_following_params=SumoCarFollowingParams(
                speed_mode=speed_mode,  # for safer behavior at the merges
            ),
            lane_change_params=SumoLaneChangeParams(
                model="SL2015", #"SL2015", #LC2013
                lane_change_mode=lane_change_mode,#0b011000000001, # (like default 1621 mode, but no lane changes other than strategic to follow route, # 512, #(collision avoidance and safety gap enforcement) # "strategic", 
                lc_speed_gain=speed_gain, #was 1000000,
                lc_keep_right=0, #was 0
                lc_pushy=0, #0.5, #1,
                lc_assertive=assertive, #[0,1] >1 also good,
                lc_pushy_gap=0.6, #default
                lc_impatience=1e-8, #1e-8,
                lc_time_to_impatience=1e12,
                ), 
            num_vehicles=num_vehicles
            )
    print(vehicles)
    #print(net_params.inflows)
def add_vehicles_no_lane_change(vehicles, veh_type, speed_mode, num_vehicles, aggressive, assertive, lc_probability):
    add_vehicles(vehicles, veh_type, NO_LANE_CHANGE_MODE, speed_mode, num_vehicles, aggressive, assertive, lc_probability)

def add_vehicles_with_lane_change(vehicles, veh_type, speed_mode, num_vehicles, aggressive, assertive, lc_probability):
    add_vehicles(vehicles, veh_type, LANE_CHANGE_MODE, speed_mode, num_vehicles, aggressive, assertive, lc_probability)


def add_veh_and_inflows_to_edge(inflows, vehicle_params, edge, rl_inflows, rl_lane_change, human_inflows, human_lane_change, aggressive, assertive, lc_probability):
    # rl_inflows: [0, 0] for right and left lanes
    # rl_lane_change: [0, 0] for right and left lanes
    # human_inflows: [2000, 2000] for right and left lanes
    # human_lane_change: [0, 1] for right and left lanes
    # edge="inflow_highway"
    rl_veh_left_or_right=0
    rl_veh_lane_change=0
    for i in range(0, len(rl_inflows)):
        if rl_inflows[i]>0:
            rl_veh_left_or_right+= 2**i
        if rl_lane_change[i]>0:
            rl_veh_lane_change+= 2**i
    #print("rl_veh_left_or_right", rl_veh_left_or_right)

    human_veh_left_or_right=0
    human_veh_lane_change=0
    for i in range(0, len(human_inflows)):
        if human_inflows[i]>0:
            human_veh_left_or_right+= 2**i
        if human_lane_change[i]>0:
            human_veh_lane_change+= 2**i
    #print("human_veh_left_or_right", human_veh_left_or_right)

    human_names=add_specified_vehicles(vehicle_params, edge+"_human", human_veh_left_or_right, human_veh_lane_change, aggressive, assertive, lc_probability)
    rl_names=add_specified_vehicles(vehicle_params, edge+"_rl", rl_veh_left_or_right, rl_veh_lane_change, aggressive, assertive, lc_probability)

    if rl_veh_left_or_right>0: 
        for i in range(0, len(rl_inflows)):
            if i<len(rl_names):
                veh_type=rl_names[i]
            else:
                veh_type=rl_names[-1]
            if veh_type is None:
                continue
            add_specified_inflow(inflows, veh_type, edge, i, rl_inflows[i])

    if human_veh_left_or_right>0:
        for i in range(0, len(human_inflows)):
            if i<len(human_names):
                veh_type=human_names[i]
            else:
                veh_type=human_names[-1]
            if veh_type is None:
                continue
            add_specified_inflow(inflows, veh_type, edge, i, human_inflows[i])

  
def add_specified_inflow(inflows, veh_type, edge, lane_index, inflow_rate):
    # This is for two-lane case, should be able to be generalized
    # veh_right_left_or_both: 
    #   1 (01) - rl right (the first lane)
    #   2 (10) - rl left (the second lane)
    #   3 (11) - rl on both
    #   0 (00) - no rl vehicles
    # veh_lane_change:
    #   1 (01) - rl right lane change
    #   2 (10) - rl left lane change
    #   3 (11) - rl both lane change
    #   0 (00) - rl neither lane change
    depart_speed=10
    if "merge" in edge:
        depart_speed=7.5
    inflows.add(veh_type=veh_type, edge=edge, vehs_per_hour=inflow_rate, depart_lane=lane_index, depart_speed=depart_speed)

def add_specified_vehicles(vehicle_params, veh_prefix, veh_right_left_or_both, veh_lane_change, aggressive, assertive, lc_probability):
    # This is for two-lane case, should be able to be generalized
    # veh_right_left_or_both: 
    #   1 (01) - veh right (the first lane)
    #   2 (10) - veh left (the second lane)
    #   3 (11) - veh on both
    #   0 (00) - no rl vehicles
    # veh_lane_change:
    #   1 (01) - veh right lane change, 
    #   2 (10) - veh left lane change
    #   3 (11) - veh both lane change
    #   0 (00) - veh neither lane change
    veh_names=[] 
    if veh_right_left_or_both==1:
        # rl on a single lane
        veh_names=[veh_prefix+"_r", None] 
    elif veh_right_left_or_both==2:
        veh_names=[None, veh_prefix+"_l"] 
    elif veh_right_left_or_both==3:
        # rl on both lanes
        veh_names=[veh_prefix+'_r', veh_prefix+'_l']

    # find the corrsponding operators to add rl vehicles
    add_veh_operators=[]
    #if len(veh_names)==1:
    #    if veh_lane_change<3 and veh_lane_change>0: # one single lane
    #        add_veh_operators=[add_vehicles_with_lane_change]
    #    elif veh_lane_change==0:
    #        add_veh_operators=[add_vehicles_no_lane_change]
    #    elif veh_lane_change==3:
    #        add_veh_operators=[add_vehicles_with_lane_change]
    if veh_lane_change==0:
        add_veh_operators=[add_vehicles_no_lane_change, add_vehicles_no_lane_change]
    elif veh_lane_change==3:
        add_veh_operators=[add_vehicles_with_lane_change, add_vehicles_with_lane_change]
    elif veh_lane_change==1:
        add_veh_operators=[add_vehicles_with_lane_change, add_vehicles_no_lane_change]
    elif veh_lane_change==2:
        add_veh_operators=[add_vehicles_no_lane_change, add_vehicles_with_lane_change]

    for i in range(0, len(veh_names)):
        veh_name=veh_names[i]
        if veh_name is None:
            continue
        operator=add_veh_operators[i]
        speed_mode=7
        veh_num=5
        if "human" in veh_name and i==0: # the right most lane and human
            speed_mode=15
        elif "rl" in veh_name:
            speed_mode=15
            veh_num=0
        operator(vehicle_params, veh_name, speed_mode, veh_num, aggressive, assertive, lc_probability)
    return veh_names
    
def add_preset_inflows(inflow_type, flow_params):
    merge_inflow_rate=200
    # see lane change mode https://sumo.dlr.de/docs/TraCI/Change_Vehicle_State.html#lane_change_mode_0xb6
    no_lane_change_mode=NO_LANE_CHANGE_COLLISION_AVOID_SAFETY_GAP_CHECK
    lane_change_mode=LANE_CHANGE_REPECT_COLLISION_AVOID_AND_SAFETY_GAP
    env_params = flow_params['env']
    net_params=flow_params['net']

    aggressive=1
    assertive=5
    if inflow_type==0:
        # pattern 1: this is a replication of our AAMAS setting where there is no lane change and the rl vehicle is only on the right lane
        #print("begin to set preset inflows")

        vehicles=VehicleParams()            
        lc_probability=0
        add_vehicles_no_lane_change(vehicles, "human_r", 15, 5, aggressive, assertive, lc_probability)
        add_vehicles_no_lane_change(vehicles, "human_l", 7, 5, aggressive, assertive, lc_probability)
        add_vehicles_no_lane_change(vehicles, "human", 7, 5, aggressive, assertive, lc_probability)
        add_vehicles_no_lane_change(vehicles, "rl", 15, 0, aggressive, assertive, lc_probability)
        flow_params['veh']=vehicles 

        # see speed mode 
        # https://sumo.dlr.de/docs/TraCI/Change_Vehicle_State.html#speed_mode_0xb3
        # rewrite the speed mode and lane change mode, according to the lane index 0: right lane, 1:left lane
        env_params.additional_params["human_speed_modes"]=[15, 7] #right 15, left 7 
        env_params.additional_params["rl_speed_modes"]=[15, 7] #right 15, left 7
        env_params.additional_params["human_lane_change_modes"]=[no_lane_change_mode, no_lane_change_mode]
        env_params.additional_params["rl_lane_change_modes"]=[no_lane_change_mode, no_lane_change_mode]

        inflow = InFlows()
        highway_right_lane=2000
        highway_left_lane=2000

        AVP_left=0 
        AVP_right=10 
        highway_right_lane_human=highway_right_lane*(100-AVP_right)/100.0
        highway_right_lane_rl=highway_right_lane*AVP_right/100.0
        highway_left_lane_human=highway_left_lane*(100-AVP_left)/100.0
        highway_left_lane_rl=highway_left_lane*AVP_left/100.0
    
        # add merge inflow
        inflow.add(
                veh_type="human",
                edge= "inflow_merge", 
                vehs_per_hour=merge_inflow_rate,
                depart_lane=0,
                depart_speed=7.5)

        # add inflow to highway right
        if highway_right_lane_human>0:
            inflow.add(
                    veh_type="human_r",
                    edge="inflow_highway",
                    vehs_per_hour=highway_right_lane_human,
                    depart_lane=0,
                    depart_speed=10)
        if highway_right_lane_rl>0:
            inflow.add(
                    veh_type="rl",
                    edge="inflow_highway",
                    vehs_per_hour=highway_right_lane_rl,
                    depart_lane=0,
                    depart_speed=10)

        # add inflow to highway left 
        if highway_left_lane_human>0:
            inflow.add(
                    veh_type="human_l",
                    edge="inflow_highway",
                    vehs_per_hour=highway_left_lane_human,
                    depart_lane=1,
                    depart_speed=10)
        if highway_left_lane_rl>0:
            inflow.add(
                    veh_type="rl",
                    edge="inflow_highway",
                    vehs_per_hour=highway_left_lane_rl,
                    depart_lane=1,
                    depart_speed=10)

        net_params.inflows=inflow
        print("set inflow",inflow)
    elif inflow_type==1:
        # pattern 2: this is AAMAS setting with human driver change lanes to escape from right lane
        vehicles=VehicleParams()            
        lc_probability=0.2
        add_vehicles_with_lane_change(vehicles, "human_r", 15, 5, aggressive, assertive, lc_probability)
        add_vehicles_no_lane_change(vehicles, "human_l", 7, 5, aggressive, assertive, lc_probability)
        add_vehicles_no_lane_change(vehicles, "human", 7, 5, aggressive, assertive, lc_probability)
        add_vehicles_no_lane_change(vehicles, "rl", 15, 0, aggressive, assertive, lc_probability)
        flow_params['veh']=vehicles 

        # rewrite the speed mode and lane change mode, according to the lane index 0: right lane, 1:left lane
        env_params.additional_params["human_speed_modes"]=[15, 7] #right 15, left 7 
        env_params.additional_params["rl_speed_modes"]=[15, 7] #right 15, left 7
        env_params.additional_params["human_lane_change_modes"]=[lane_change_mode, no_lane_change_mode]
        env_params.additional_params["rl_lane_change_modes"]=[no_lane_change_mode, no_lane_change_mode]

        inflow = InFlows()
        highway_right_lane=2000
        highway_left_lane=2000

        AVP_left=0 
        AVP_right=10 
        highway_right_lane_human=highway_right_lane*(100-AVP_right)/100.0
        highway_right_lane_rl=highway_right_lane*AVP_right/100.0
        highway_left_lane_human=highway_left_lane*(100-AVP_left)/100.0
        highway_left_lane_rl=highway_left_lane*AVP_left/100.0
    
        # add merge inflow
        inflow.add(
                veh_type="human",
                edge= "inflow_merge", 
                vehs_per_hour=merge_inflow_rate,
                depart_lane=0,
                depart_speed=7.5)

        # add inflow to highway right
        if highway_right_lane_human>0:
            inflow.add(
                    veh_type="human_r",
                    edge="inflow_highway",
                    vehs_per_hour=highway_right_lane_human,
                    depart_lane=0,
                    depart_speed=10)
        if highway_right_lane_rl>0:
            inflow.add(
                    veh_type="rl",
                    edge="inflow_highway",
                    vehs_per_hour=highway_right_lane_rl,
                    depart_lane=0,
                    depart_speed=10)

        # add inflow to highway left 
        if highway_left_lane_human>0:
            inflow.add(
                    veh_type="human_l",
                    edge="inflow_highway",
                    vehs_per_hour=highway_left_lane_human,
                    depart_lane=1,
                    depart_speed=10)
        if highway_left_lane_rl>0:
            inflow.add(
                    veh_type="rl",
                    edge="inflow_highway",
                    vehs_per_hour=highway_left_lane_rl,
                    depart_lane=1,
                    depart_speed=10)

        net_params.inflows=inflow

    elif inflow_type==2:
        # Pattern 3: rl vehicles on the left lane but there is human drivers cut in from the right lane.

        #print("begin to set preset inflows")
        vehicles=VehicleParams()            
        lc_probability=0.2
        add_vehicles_with_lane_change(vehicles, "human_r", 15, 5, aggressive, assertive, lc_probability)
        add_vehicles_no_lane_change(vehicles, "human_l", 7, 5, aggressive, assertive, lc_probability)
        add_vehicles_no_lane_change(vehicles, "human", 7, 5, aggressive, assertive, lc_probability)
        add_vehicles_no_lane_change(vehicles, "rl", 15, 0, aggressive, assertive, lc_probability)
        flow_params['veh']=vehicles 

        # rewrite the speed mode and lane change mode, according to the lane index 0: right lane, 1:left lane
        env_params.additional_params["human_speed_modes"]=[15, 7] #right 15, left 7 
        env_params.additional_params["rl_speed_modes"]=[15, 7] #right 15, left 7
        env_params.additional_params["human_lane_change_modes"]=[lane_change_mode, no_lane_change_mode]
        env_params.additional_params["rl_lane_change_modes"]=[no_lane_change_mode, no_lane_change_mode]

        inflow = InFlows()
        highway_right_lane=2000
        highway_left_lane=2000

        AVP_left=10 
        AVP_right=0 
        highway_right_lane_human=highway_right_lane*(100-AVP_right)/100.0
        highway_right_lane_rl=highway_right_lane*AVP_right/100.0
        highway_left_lane_human=highway_left_lane*(100-AVP_left)/100.0
        highway_left_lane_rl=highway_left_lane*AVP_left/100.0
    
        # add merge inflow
        inflow.add(
                veh_type="human",
                edge= "inflow_merge", 
                vehs_per_hour=merge_inflow_rate,
                depart_lane=0,
                depart_speed=7.5)

        # add inflow to highway right
        if highway_right_lane_human>0:
            inflow.add(
                    veh_type="human_r",
                    edge="inflow_highway",
                    vehs_per_hour=highway_right_lane_human,
                    depart_lane=0,
                    depart_speed=10)
        if highway_right_lane_rl>0:
            inflow.add(
                    veh_type="rl",
                    edge="inflow_highway",
                    vehs_per_hour=highway_right_lane_rl,
                    depart_lane=0,
                    depart_speed=10)

        # add inflow to highway left 
        if highway_left_lane_human>0:
            inflow.add(
                    veh_type="human_l",
                    edge="inflow_highway",
                    vehs_per_hour=highway_left_lane_human,
                    depart_lane=1,
                    depart_speed=10)
        if highway_left_lane_rl>0:
            inflow.add(
                    veh_type="rl",
                    edge="inflow_highway",
                    vehs_per_hour=highway_left_lane_rl,
                    depart_lane=1,
                    depart_speed=10)

        net_params.inflows=inflow

    
def reset_inflows(args, flow_params):
    env_params = flow_params['env']
    net_params=flow_params['net']
    veh_params=flow_params['veh'] 
    env_name=flow_params['env_name']

    if veh_params is None:
        veh_params=VehicleParams()

    # Inflows        
    # This is implemented in flow.envs.base or flow.envs.multiagent.base
    if args.random_inflow:
        env_params.additional_params['reset_inflow']=True
        env_params.additional_params['inflow_range']=[0.5, 1.5]

    # collect all mergers or on ramps
    merge_names=list()
    for inflow in net_params.inflows.get():
        if 'merge' in inflow['edge'] or 'on_ramp' in inflow['edge']:
            merge_names.append(inflow['edge'])
    # for training, the net_params may be empty, we add inflow_merge as the default one
    if len(merge_names)==0:
        merge_names.append("inflow_merge")
        
    # This is used by human baseline
    if args.main_merge_human_inflows:
        input_inflows=args.main_merge_human_inflows
        inflow = InFlows()
        main_human_inflow_rate=input_inflows[0] 
        merge_human_inflow_rate=input_inflows[1]
        print('begin set human baseline inflows')
        if main_human_inflow_rate>0:
            if env_name!=MultiAgentHighwayPOEnvMerge4CollaborateMOR:
                inflow.add(
                    veh_type="human",
                    edge="inflow_highway",
                    vehs_per_hour=main_human_inflow_rate,
                    depart_lane="free",
                    depart_speed=10)
            else:
                inflow.add(
                    veh_type="human",
                    edge="highway_0",
                    vehs_per_hour=main_human_inflow_rate,
                    depart_lane="free",
                    depart_speed=10)

        if merge_human_inflow_rate>0:
            for merge_name in merge_names:
                inflow.add(
                    veh_type="human",
                    edge=merge_name,#"inflow_merge",
                    vehs_per_hour=merge_human_inflow_rate,
                    depart_lane="free",
                    depart_speed=7.5)
        net_params.inflows=inflow
        print("after set:",inflow.get())
    # set human and rl vehicles in highway, and human vehicles on every merge or on ramp
    if args.handset_inflow:
        # env_params.additional_params['handset_inflow']=args.handset_inflow
        # handset_inflow
        #vehicles = VehicleParams()
        ## human vehicles
        if "human" not in veh_params.type_parameters.keys():
            veh_params.add(
                veh_id="human",
                acceleration_controller=(SimCarFollowingController, {}),
                car_following_params=SumoCarFollowingParams(
                    speed_mode=9,  # for safer behavior at the merges
                    #tau=1.5  # larger distance between cars
                ),
                #lane_change_params=SumoLaneChangeParams(lane_change_mode=1621)
                num_vehicles=5)

        ## autonomous vehicles
        if "rl" not in veh_params.type_parameters.keys():
            veh_params.add(
                veh_id="rl",
                acceleration_controller=(RLController, {}),
                car_following_params=SumoCarFollowingParams(
                    speed_mode=9,
                ),
                num_vehicles=0)

        print("handset inflows")
        input_inflows=args.handset_inflow
        main_human_inflow_rate=input_inflows[0] 
        main_rl_inflow_rate=input_inflows[1] 
        merge_inflow_rate=input_inflows[2]
        inflow = InFlows()
        if main_human_inflow_rate>0:
            if env_name!=MultiAgentHighwayPOEnvMerge4CollaborateMOR:
                inflow.add(
                    veh_type="human",
                    edge="inflow_highway",
                    vehs_per_hour=main_human_inflow_rate,
                    depart_lane="free",
                    depart_speed=10)
            else:
                inflow.add(
                    veh_type="human",
                    edge="highway_0",
                    vehs_per_hour=main_human_inflow_rate,
                    depart_lane="free",
                    depart_speed=10)
        rl_depart_lane="free"
        if main_rl_inflow_rate>0:
            if env_name!=MultiAgentHighwayPOEnvMerge4CollaborateMOR:
                inflow.add(
                    veh_type="rl",
                    edge="inflow_highway",
                    vehs_per_hour=main_rl_inflow_rate,
                    depart_lane=rl_depart_lane,
                    depart_speed=10)
            else:
                inflow.add(
                    veh_type="rl",
                    edge="highway_0",
                    vehs_per_hour=main_rl_inflow_rate,
                    depart_lane=rl_depart_lane,
                    depart_speed=10)

        if merge_inflow_rate>0:
            for merge_name in merge_names:
                inflow.add(
                    veh_type="human",
                    edge= merge_name, #"inflow_merge",
                    vehs_per_hour=merge_inflow_rate,
                    depart_lane="free",
                    depart_speed=7.5)
        net_params.inflows=inflow

    if args.preset_inflow is not None:
        add_preset_inflows(args.preset_inflow, flow_params)

    if args.human_inflows is not None and args.rl_inflows is not None and args.rl_lane_change is not None and args.human_lane_change is not None and args.merge_inflow is not None and args.aggressive is not None and args.assertive is not None and args.lc_probability is not None:
        # check whether human inflows only contains 0 or 1
        for e in args.human_lane_change+args.rl_lane_change:
            if e not in [0,1]:
                print("The element in human_lane_change and rl_lane_change must be 0 or 1")
                sys.exit(-1)

        inflows = InFlows()

        veh_params=VehicleParams()
        print("aggressive", args.aggressive)
        add_veh_and_inflows_to_edge(inflows, veh_params, "inflow_highway", args.rl_inflows, args.rl_lane_change, args.human_inflows, args.human_lane_change, args.aggressive, args.assertive, args.lc_probability)
        add_veh_and_inflows_to_edge(inflows, veh_params, "inflow_merge", [], [], [args.merge_inflow], [0], args.aggressive, args.assertive, args.lc_probability)

        # set the lane change mode for both lanes in the highway edge 
        env_params.additional_params["human_speed_modes"]=[15, 7] #right 15, left 7 
        env_params.additional_params["rl_speed_modes"]=[15, 7] #right 15, left 7
        no_lane_change_mode=NO_LANE_CHANGE_MODE
        lane_change_mode=LANE_CHANGE_MODE #LANE_CHANGE_REPECT_COLLISION_AVOID #LANE_CHANGE_REPECT_COLLISION_AVOID_AND_SAFETY_GAP
        if args.human_lane_change[0]==0 and args.human_lane_change[1]==0:
            env_params.additional_params["human_lane_change_modes"]=[no_lane_change_mode, no_lane_change_mode]
        elif args.human_lane_change[0]==1 and args.human_lane_change[1]==0:
            env_params.additional_params["human_lane_change_modes"]=[lane_change_mode, no_lane_change_mode]
        elif args.human_lane_change[0]==0 and args.human_lane_change[1]==1:
            env_params.additional_params["human_lane_change_modes"]=[no_lane_change_mode, lane_change_mode]
        elif args.human_lane_change[0]==1 and args.human_lane_change[1]==1:
            env_params.additional_params["human_lane_change_modes"]=[lane_change_mode, lane_change_mode]
        else:
            print("error in setting lane chagne mode for edges")
            sys.exit(-1)
        env_params.additional_params["rl_lane_change_modes"]=[no_lane_change_mode, no_lane_change_mode]

        #print("rl_inflows", args.rl_inflows)
        #print("rl_lane_change", args.rl_lane_change)
        #print("human_inflows", args.human_inflows)
        #print("human_lane_change", args.human_lane_change)
        #add_veh_and_inflows_to_edge(inflows, veh_params, "inflow_highway", [1, 1], [0, 0], [1,0], [0, 0])

        net_params.inflows=inflows
        flow_params['net']=net_params
        flow_params['veh']=veh_params
        #print("lane change params:")
        #for veh_id, dict_value in veh_params.type_parameters.items():
        #    #print(veh_id, dict_value['car_following_params'].speed_mode)
        #    #print(veh_id, dict_value['lane_change_params'].lane_change_mode)
        #    print(veh_id, dict_value['lane_change_params'].controller_params['lcPushy'])
    # convert all inflows to probability
    net_params=flow_params['net']
    if args.to_probability:
        FLOW_RATE=0
        for inflow in net_params.inflows.get(): 
            if "merge" in inflow['edge'] or 'on_ramp' in inflow['edge']:
                continue
            if "on_ramp" in inflow['edge']:
                continue
            if 'probability' in inflow:
                continue
            
            if 'vehs_per_hour' in inflow:
                FLOW_RATE=inflow['vehs_per_hour']
                del inflow['vehs_per_hour']
            elif 'vehsPerHour' in inflow:
                FLOW_RATE=inflow['vehsPerHour']
                del inflow['vehsPerHour']
            else:
                print(inflow.keys()) 
                print("The inflow is not set by vehs_per_hour or probability. Please add their support to extrate FLOW_RATE.")
                sys.exit(-1)
            inflow['probability']=FLOW_RATE/3600.0 

    if args.merge_random_inflow_percentage:
        total_merge_inflow=0
        inflows_to_remove=list()
        # find the total inflows from merge
        for inflow in net_params.inflows.get(): 
            if 'merge' in inflow['edge']:
                if 'vehs_per_hour' in inflow:
                    total_merge_inflow+=inflow['vehs_per_hour']
                if 'vehsPerHour' in inflow:
                    total_merge_inflow+=inflow['vehsPerHour']
                if 'probability' in inflow:
                    total_merge_inflow+=inflow['probability']*3600
                inflows_to_remove.append(inflow)

        # remove all the inflows from merge
        for inflow in inflows_to_remove:
            net_params.inflows.get().remove(inflow)

        # set the merge inflows according to the percentage of random and even inflows
        random_percentage=args.merge_random_inflow_percentage/100.0
        even_percentage=1-random_percentage
        if random_percentage>0:
            random_inflow_rate=total_merge_inflow*random_percentage
            probability=random_inflow_rate/3600
            net_params.inflows.add(name="inflow_human_merge", veh_type="human", edge="inflow_merge",
                    probability=probability, depart_lane="free",
                    depart_speed=7.5)
        if even_percentage>0:
            even_inflow_rate=total_merge_inflow*even_percentage
            net_params.inflows.add(name="inflow_human_merge", veh_type="human", edge="inflow_merge",
                    vehs_per_hour=even_inflow_rate, depart_lane="free",
                    depart_speed=7.5)

    if args.main_random_inflow_percentage:
        total_main_human_inflow=0
        inflows_to_remove=list()
        for inflow in net_params.inflows.get():
            if 'merge' in inflow['edge']:
                continue
            if 'human' in inflow['vtype']:
                if 'vehs_per_hour' in inflow:
                    total_main_human_inflow+=inflow['vehs_per_hour']
                if 'vehsPerHour' in inflow:
                    total_main_human_inflow+=inflow['vehsPerHour']
                if 'probability' in inflow:
                    total_main_human_inflow+=inflow['probability']*3600
                inflows_to_remove.append(inflow)
        # remove all the inflows from merge
        for inflow in inflows_to_remove:
            net_params.inflows.get().remove(inflow)

        # set the main human inflows according to the percentage of random and even inflows
        random_percentage=args.main_random_inflow_percentage/100.0
        even_percentage=1.0-random_percentage
        if random_percentage>0:
            random_inflow_rate=total_main_human_inflow*random_percentage
            probability=random_inflow_rate/3600.0
            net_params.inflows.add(name="inflow_human_highway", veh_type="human", edge="inflow_highway",
                    probability=probability, depart_lane="free",
                    depart_speed=7.5)
        if even_percentage>0:
            even_inflow_rate=total_main_human_inflow*even_percentage
            net_params.inflows.add(name="inflow_human_highway", veh_type="human", edge="inflow_highway",
                    vehs_per_hour=even_inflow_rate, depart_lane="free",
                    depart_speed=7.5)

