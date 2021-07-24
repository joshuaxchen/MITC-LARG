"""Environment used to train vehicles to improve traffic on a highway."""
import numpy as np
from gym.spaces.box import Box
from gym.spaces import Discrete 
from flow.core.rewards import desired_velocity, average_velocity
from flow.envs.multiagent.base import MultiEnv
import collections
import os
from copy import deepcopy
from flow.envs.multiagent import MultiAgentHighwayPOEnvMerge4,MultiAgentHighwayPOEnvMerge4Collaborate
from flow.utils.rllib import get_rllib_config, get_rllib_pkl
from flow.utils.rllib import get_flow_params
from flow.utils.registry import make_create_env
from ray.tune.registry import register_env,get_trainable_cls
try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class

from ray.rllib.agents.callbacks import DefaultCallbacks
from flow.envs.multiagent.trained_policy import init_policy_agent 
import ray

ADDITIONAL_ENV_PARAMS = {
    # maximum acceleration of autonomous vehicles
    'max_accel': 1,
    # maximum deceleration of autonomous vehicles
    'max_decel': 1,
    # desired velocity for all vehicles in the network, in m/s
    "target_velocity": 25,
    # selfishness, coeff before -1
    #"eta1": 0.9,
    # collaborative, coeff before average speed
    #"eta2": 0.1
    "max_headway": 1,
}


def policy_map_fn(_):
        return 'av'

class MultiAgentHighwayPOEnvMerge4Hierarchy(MultiAgentHighwayPOEnvMerge4Collaborate):
    #accel_agent_obj=None
    def __init__(self, env_params, sim_params, network, simulator='traci'):
        super().__init__(env_params, sim_params, network, simulator)
        #trained_agent_ref=env_params.additional_params['trained_agent_ref']
        #print("obtained ref:",trained_agent_ref)
        result_dir=env_params.additional_params['trained_dir']
        checkpoint=env_params.additional_params['checkpoint']
        print("load data from:", result_dir, "checkpoint", checkpoint)
        self.accel_agent_obj=init_policy_agent(result_dir,checkpoint)
        #if MultiAgentHighwayPOEnvMerge4Hierarchy.accel_agent_obj is None:
        #    MultiAgentHighwayPOEnvMerge4Hierarchy.accel_agent_obj=init_policy_agent(result_dir,checkpoint)

    def __del__(self):
        #super().__del__()
        del self.accel_agent_obj

    @property
    def action_space(self):
        """See class definition."""
        return Discrete(2)
        #return Box(
        #    low=0,#-np.abs(self.env_params.additional_params['max_decel']),
        #    high=1,#self.env_params.additional_params['max_accel'],
        #    shape=(1,),  # (4,),
        #    dtype=np.float32)

    def idm_acceleration(self, veh_id):
            #print(veh_id, "chooses to be a leader with probability:",rl_action)
            a=1 # max acceleration, in m/s2 (default: 1)
            delta=4 # acceleration exponent (default: 4)
            s0=2 # linear jam distance, in m (default: 2)
            MAX_T=self.env_params.additional_params['max_headway']
            b=1.5 # comfortable deceleration, in m/s2 (default: 1.5)
            v0=30 # desirable velocity, in m/s (default: 30)
            T=1 # safe time headway, in s (default: 1)
            v = self.k.vehicle.get_speed(veh_id) 
            lead_id = self.k.vehicle.get_leader(veh_id)
            h = self.k.vehicle.get_headway(veh_id)
             # in order to deal with ZeroDivisionError
            if abs(h) < 1e-3:
                h = 1e-3
            if lead_id is None or lead_id == '':  # no car ahead
                s_star = 0
            else:
                lead_vel = self.k.vehicle.get_speed(lead_id)
                s_star = s0 + max(0, v * T + v * (v - lead_vel) /(2 * np.sqrt(a * b)))
            return a * (1 - (v / v0)**delta - (s_star / h)**2)

    def clip_acceleration(self, rl_acceleration):
        """Clip the acceleartions passed from the RL agent.
        """
        # ignore if no actions are issued
        if rl_acceleration is None:
            return None

        # clip according to the action space requirements
        for key, acceleration in rl_acceleration.items():
            rl_acceleration[key] = np.clip(
                    acceleration,
                    a_min=-np.abs(self.env_params.additional_params['max_decel']), 
                    a_max=self.env_params.additional_params['max_decel'])
        return rl_acceleration


    def apply_rl_actions(self, rl_actions=None):
        """Specify the actions to be performed by the rl agent(s).

        If no actions are provided at any given step, the rl agents default to
        performing actions specified by sumo.

        Parameters
        ----------
        rl_actions : dict of array_like
            dict of list of actions provided by the RL algorithm
        """
        # ignore if no actions are issued
        if rl_actions is None:
            return

        #if 'trained_dir' in self.env_params.additional_params.keys() and MultiAgentHighwayPOEnvMerge4Hierarchy.accel_agent is None:
        #    print("load policy agent")
        #    result_dir=self.env_params.additional_params['trained_dir']
        #    checkpoint=self.env_params.additional_params['checkpoint']
        #    MultiAgentHighwayPOEnvMerge4Hierarchy.accel_agent=MultiAgentHighwayPOEnvMerge4Hierarchy.init_policy_agent(result_dir, checkpoint)

        #print("network choice:",rl_actions) 
        clipped_actions = self.clip_actions(rl_actions)
        if rl_actions!=clipped_actions:
            print("********network gives an action out of bound********************")
            import sys
            sys.exit(-1)
            #print("action bound:[",self.action_space.low[0], ",", self.action_space.high[0],"]")
            #print("actions from the network:",rl_actions)
            #print("actions after clipped:",clipped_actions)
            #print("within bound:[",self.action_space.low[0], ",", self.action_space.high[0],"]")

        leader_rl_acceleration={}
        follower_rl_acceleration={}
        acceleration={}
        for rl_id, choice in clipped_actions.items():
            # compute acceleration as a leader: the acceleration is from the headway
            if choice==0:# be a follower 
                #print(rl_id, "chooses to be a leader with probability:", chosen_act)
                leader_accel=self.idm_acceleration(rl_id)
                acceleration[rl_id]=np.array([leader_accel])  
            elif choice==1: # be a leader
                # compute acceleartion as a follower: the acceleration is from an existing policy
                state=self.get_state()
                if rl_id in state.keys():
                    #acceleration[rl_id]= MultiAgentHighwayPOEnvMerge4Hierarchy.accel_agent_obj.compute_action(state[rl_id][0:9], policy_id=policy_map_fn(rl_id)) 
                    acceleration[rl_id]= self.accel_agent_obj.compute_action(state[rl_id][0:9], policy_id=policy_map_fn(rl_id)) 
                #accel_policy_obj=ray.get(accel_policy)
                #acceleration[rl_id]= accel_policy_obj.compute_single_action(state[rl_id][0:9]) 
            else:
                print("action out of bound")
                import sys
                sys.exit(-1)

        #print("before clip acceleration:", acceleration)
        clipped_acceleration=self.clip_acceleration(acceleration)
        #print("after clip acceleration:", clipped_acceleration)
        self._apply_rl_actions(clipped_acceleration)
class MultiAgentHighwayPOEnvMerge4HierarchyVehiclesBetweenNextRL(MultiAgentHighwayPOEnvMerge4Hierarchy):
    @property
    def observation_space(self):
        #See class definition
        return Box(-float('inf'), float('inf'), shape=(10,), dtype=np.float32)

    def get_state(self):
        obs=super().get_state()
        # add the 10th state, the number of vehicles ahead for each RL vehicle (merge road excluded)
        for rl_id in self.k.vehicle.get_rl_ids():
            rl_x=self.k.vehicle.get_x_by_id(rl_id)
            rl_road_id=self.k.vehicle.get_edge(rl_id)
            num_between=0
            if rl_road_id in ["inflow_merge", "bottom", "center"]:
                # if rl vehicle is not before junction
                pass
            else:
                # if it is before the junction
                # find the nearest rl vehicle position
                closest_rl_x=10000 # a large number 
                # find the closest rl with the smallest x
                for next_rl_id in self.k.vehicle.get_rl_ids():
                    next_rl_x=self.k.vehicle.get_x_by_id(next_rl_id)
                    next_rl_road_id=self.k.vehicle.get_edge(rl_id)
                    if next_rl_road_id not in ["inflow_merge", "bottom", "center"] and next_rl_x>rl_x and next_rl_x<closest_rl_x: # ahead of current rl
                        closest_rl_x=next_rl_x

                for veh_id in self.k.vehicle.get_ids():
                    veh_x=self.k.vehicle.get_x_by_id(veh_id)
                    veh_road_id=self.k.vehicle.get_edge(rl_id)
                    if veh_id!=rl_id and veh_road_id not in ["inflow_merge", "bottom", "center"] and rl_x<veh_x and veh_x<closest_rl_x:
                        num_between+=1
                    else:
                        pass
            observation=obs[rl_id]
            max_ahead=50.0
            #print("num between:",num_between)
            observation = np.append(observation, num_between/max_ahead)
            obs.update({rl_id: observation})

        return obs

class MultiAgentHighwayPOEnvMerge4HierarchyCountAhead(MultiAgentHighwayPOEnvMerge4Hierarchy):
    @property
    def observation_space(self):
        #See class definition
        return Box(-float('inf'), float('inf'), shape=(10,), dtype=np.float32)

    def get_state(self):
        obs=super().get_state()
        # add the 10th state, the number of vehicles ahead for each RL vehicle (merge road excluded)
        for rl_id in self.k.vehicle.get_rl_ids():
            rl_x=self.k.vehicle.get_x_by_id(rl_id)
            rl_road_id=self.k.vehicle.get_edge(rl_id)
            num_ahead=0
            for veh_id in self.k.vehicle.get_ids():
                veh_x=self.k.vehicle.get_x_by_id(veh_id)
                veh_road_id=self.k.vehicle.get_edge(rl_id)
                if veh_id!=rl_id and veh_road_id not in ["inflow_merge", "bottom", "center"] and rl_x<veh_x:
                    num_ahead+=1
                else:
                    pass
            observation=obs[rl_id]
            max_ahead=100.0
            observation = np.append(observation, num_ahead/max_ahead)
            obs.update({rl_id: observation})

        return obs
class MultiAgentHighwayPOEnvMerge4HierarchyDensityAhead(MultiAgentHighwayPOEnvMerge4Hierarchy):
    @property
    def observation_space(self):
        #See class definition
        return Box(-float('inf'), float('inf'), shape=(10,), dtype=np.float32)

    def get_state(self):
        obs=super().get_state()
        # add the 10th state, the number of vehicles ahead for each RL vehicle (merge road excluded)
        for rl_id in self.k.vehicle.get_rl_ids():
            rl_x=self.k.vehicle.get_x_by_id(rl_id)
            rl_road_id=self.k.vehicle.get_edge(rl_id)
            num_ahead=0
            for veh_id in self.k.vehicle.get_ids():
                veh_x=self.k.vehicle.get_x_by_id(veh_id)
                veh_road_id=self.k.vehicle.get_edge(rl_id)
                if veh_id!=rl_id and veh_road_id not in ["inflow_merge", "bottom", "center"] and rl_x<veh_x:
                    num_ahead+=1
                else:
                    pass
            observation=obs[rl_id]
            # obtain the distance to the junction
            center_x = self.k.network.total_edgestarts_dict["center"]
            #print("center_x",center_x)
            merge_dist=obs[rl_id][5]*center_x
            veh_length=self.k.vehicle.get_length(rl_id)
            #print("merge_dist",merge_dist)
            #print("veh_length",veh_length)
            observation = np.append(observation, num_ahead*veh_length/merge_dist)
            #print("density", observation[-1])
            obs.update({rl_id: observation})

        return obs
