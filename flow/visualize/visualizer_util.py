from flow.controllers import IDMController, RLController, SimCarFollowingController
from flow.core.params import EnvParams, NetParams, InitialConfig, InFlows, \
                             VehicleParams, SumoParams, \
                             SumoCarFollowingParams, SumoLaneChangeParams

from flow.controllers import SimLaneChangeController

def add_vehicles(vehicles, veh_type, lane_change_mode, speed_mode, num_vehicles):                
    controller=None
    if "rl" in veh_type:
        controller=RLController
    elif "human" in veh_type:
        controller= IDMController #SimCarFollowingController#

    # CREATE VEHICLE TYPES AND INFLOWS
    vehicles.add(
        veh_id=veh_type,
        acceleration_controller=(controller, {}),
        lane_change_controller=(SimLaneChangeController, {}),
        car_following_params=SumoCarFollowingParams(
            speed_mode=speed_mode,  # for safer behavior at the merges
        ),
        lane_change_params=SumoLaneChangeParams(
            model="SL2015", #"SL2015", #LC2013
          lane_change_mode=lane_change_mode,#0b011000000001, # (like default 1621 mode, but no lane changes other than strategic to follow route, # 512, #(collision avoidance and safety gap enforcement) # "strategic", 
          lc_speed_gain=1000000,
          lc_pushy=1, #0.5, #1,
          lc_assertive=5, #20,
          lc_impatience=1e-8,
          lc_time_to_impatience=1e12
         ), 
        num_vehicles=num_vehicles
        )


    #print(net_params.inflows)
def add_vehicles_no_lane_change(vehicles, veh_type, speed_mode, num_vehicles):
    add_vehicles(vehicles, veh_type, 512, speed_mode, num_vehicles)

def add_vehicles_with_lane_change(vehicles, veh_type, speed_mode, num_vehicles):
    add_vehicles(vehicles, veh_type, 1621, speed_mode, num_vehicles)

def add_preset_inflows(inflow_type, flow_params):
    merge_inflow_rate=200
    # see lane change mode https://sumo.dlr.de/docs/TraCI/Change_Vehicle_State.html#lane_change_mode_0xb6
    no_lane_change_mode=512
    lane_change_mode=1621
    env_params = flow_params['env']
    net_params=flow_params['net']

    if inflow_type==0:
        # pattern 1: this is a replication of our AAMAS setting where there is no lane change and the rl vehicle is only on the right lane
        #print("begin to set preset inflows")

        vehicles=VehicleParams()            
        add_vehicles_no_lane_change(vehicles, "human_r", 15, 5)
        add_vehicles_no_lane_change(vehicles, "human_l", 7, 5)
        add_vehicles_no_lane_change(vehicles, "human", 7, 5)
        add_vehicles_no_lane_change(vehicles, "rl", 15, 0)
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
        add_vehicles_with_lane_change(vehicles, "human_r", 15, 5)
        add_vehicles_no_lane_change(vehicles, "human_l", 7, 5)
        add_vehicles_no_lane_change(vehicles, "human", 7, 5)
        add_vehicles_no_lane_change(vehicles, "rl", 15, 0)
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
        add_vehicles_with_lane_change(vehicles, "human_r", 15, 5)
        add_vehicles_no_lane_change(vehicles, "human_l", 7, 5)
        add_vehicles_no_lane_change(vehicles, "human", 7, 5)
        add_vehicles_no_lane_change(vehicles, "rl", 15, 0)
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
        
    # This is used by human baseline
    print("set main merge human inflows")
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
    print("handset inflows")
    if args.handset_inflow:
        # env_params.additional_params['handset_inflow']=args.handset_inflow
        # handset_inflow
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
        if args.rl_left:
            rl_depart_lane=1
        elif args.rl_right:
            rl_depart_lane=0
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

    # convert all inflows to probability
    if args.to_probability:
        FLOW_RATE=0
        for inflow in net_params.inflows.get(): 
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

