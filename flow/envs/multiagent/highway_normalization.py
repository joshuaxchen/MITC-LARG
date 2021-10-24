"""Environment used to train vehicles to improve traffic on a highway."""
import numpy as np
from gym.spaces.box import Box
from flow.core.rewards import desired_velocity, average_velocity
from flow.envs.multiagent.base import MultiEnv
from flow.envs.multiagent.highway import MultiAgentHighwayPOEnv
import collections
import os
from copy import deepcopy

class MultiAgentHighwayPOEnvMerge4NormalizedToDistance(MultiAgentHighwayPOEnv):
    @property
    def observation_space(self):
        #See class definition
        return Box(-float('inf'), float('inf'), shape=(9,), dtype=np.float32)

    def get_state(self): # modification on the merge distance 
        states = super().get_state()
        junctions = set(self.k.network.get_junction_list())

        # normalizing constants
        max_speed = 30.0 #self.k.network.max_speed()
        max_length = 1000.0#self.k.network.length()
        
        merge_distance_base=self.k.network.edge_length("inflow_merge")
        merge_vehs = self.k.vehicle.get_ids_by_edge("bottom")
        if merge_vehs is not None or len(merge_vehs)==0:
            merge_vehs = self.k.vehicle.get_ids_by_edge(["inflow_merge"])
            merge_distance_base=0
        #merge_dists = [self.k.vehicle.get_x(veh) for veh in merge_vehs]
        merge_distance = 1
        merge_vel = 0
        len_merge = self.k.network.edge_length("bottom") + self.k.network.edge_length("inflow_merge")
        start_position = self.k.network.total_edgestarts_dict["inflow_merge"]
        if len(merge_vehs)>0: # if no merging vehicles are detected, then merge_vel=0 and merge_distance=1
            first_merge=None
            max_pos=0
            for veh in merge_vehs:
                veh_pos=self.k.vehicle.get_position(veh)
                if veh_pos>max_pos:
                    first_merge=veh
                    max_pos=veh_pos
            max_pos+=merge_distance_base
            merge_dist = (len_merge - 2*max_pos)/len_merge # TODO: normalize with speed?
            merge_vel = self.k.vehicle.get_speed(first_merge)/max_speed
                
        for rl_id in states:
            edge_id = self.k.vehicle.get_edge(rl_id)
            lane = self.k.vehicle.get_lane(rl_id)
            edge_len = self.k.network.edge_length(edge_id)
            rl_position = self.k.vehicle.get_position(rl_id)
            rl_x = self.k.vehicle.get_x_by_id(rl_id)
            #rl_dist = max(edge_len-rl_position, 0) / max_length
            veh_vel = []
            
            #calculate RL distance to the center junction
            veh_x = self.k.vehicle.get_x_by_id(rl_id)
            edge = self.k.vehicle.get_edge(rl_id)
            length = self.k.network.edge_length(edge)
            center_x = self.k.network.total_edgestarts_dict["center"]
            rl_dist = 1
            if edge in ["inflow_highway","left","center"]:
                rl_dist = (veh_x - center_x)/(center_x)
            else:
                pass #FIXME: not yet implemented
            num_veh_ahead = 0 
            for veh_id in self.k.vehicle.get_ids_by_edge(["left","inflow_highway"]):
                veh_position = self.k.vehicle.get_x_by_id(veh_id)
                if veh_position > rl_x:
                    veh_vel.append(self.k.vehicle.get_speed(veh_id))
                    num_veh_ahead += 1
            if len(veh_vel) > 0:
                veh_vel = np.mean(veh_vel)
            else:
                veh_vel = self.k.network.speed_limit(edge_id)
            veh_vel /= max_speed
            
            if edge in ["center"]:
                states[rl_id] = np.array(list(states[rl_id]) + [rl_dist, veh_vel, 1.0, 0.0])
            else:
                states[rl_id] = np.array(list(states[rl_id]) + [rl_dist, veh_vel, merge_distance, merge_vel])
        #print(states)
        return states

class MultiAgentHighwayPOEnvMerge4NormalizedToTime(MultiAgentHighwayPOEnv):
    @property
    def observation_space(self):
        #See class definition
        return Box(-float('inf'), float('inf'), shape=(9,), dtype=np.float32)

    def get_state(self): # modification on the merge distance 
        states = super().get_state()
        junctions = set(self.k.network.get_junction_list())

        # normalizing constants
        max_speed = 30.0 #self.k.network.max_speed()
        max_length = 1000.0#self.k.network.length()
        
        merge_distance_base=self.k.network.edge_length("inflow_merge")
        merge_vehs = self.k.vehicle.get_ids_by_edge("bottom")
        if merge_vehs is not None or len(merge_vehs)==0:
            merge_vehs = self.k.vehicle.get_ids_by_edge(["inflow_merge"])
            merge_distance_base=0
        #merge_dists = [self.k.vehicle.get_x(veh) for veh in merge_vehs]
        merge_distance = 1
        merge_vel = 0
        len_merge = self.k.network.edge_length("bottom") + self.k.network.edge_length("inflow_merge")
        start_position = self.k.network.total_edgestarts_dict["inflow_merge"]
        max_merging_time=100
        if len(merge_vehs)>0: # if no merging vehicles are detected, then merge_vel=0 and merge_distance=1
            first_merge=None
            max_pos=0
            for veh in merge_vehs:
                veh_pos=self.k.vehicle.get_position(veh)
                if veh_pos>max_pos:
                    first_merge=veh
                    max_pos=veh_pos
            max_pos+=merge_distance_base
            merge_vel = self.k.vehicle.get_speed(first_merge)/max_speed
            merge_dist = (len_merge - 2*max_pos)/(merge_vel*max_speed*max_merging_time) #TODO: normalize with speed?
                
        for rl_id in states:
            edge_id = self.k.vehicle.get_edge(rl_id)
            lane = self.k.vehicle.get_lane(rl_id)
            edge_len = self.k.network.edge_length(edge_id)
            rl_position = self.k.vehicle.get_position(rl_id)
            rl_x = self.k.vehicle.get_x_by_id(rl_id)
            #rl_dist = max(edge_len-rl_position, 0) / max_length
            veh_vel = []
            
            #calculate RL distance to the center junction
            veh_x = self.k.vehicle.get_x_by_id(rl_id)
            edge = self.k.vehicle.get_edge(rl_id)
            length = self.k.network.edge_length(edge)
            center_x = self.k.network.total_edgestarts_dict["center"]
            rl_dist = 1
            if edge in ["inflow_highway","left","center"]:
                rl_dist = (veh_x - center_x)/(center_x)
            else:
                pass #FIXME: not yet implemented
            num_veh_ahead = 0 
            for veh_id in self.k.vehicle.get_ids_by_edge(["left","inflow_highway"]):
                veh_position = self.k.vehicle.get_x_by_id(veh_id)
                if veh_position > rl_x:
                    veh_vel.append(self.k.vehicle.get_speed(veh_id))
                    num_veh_ahead += 1
            if len(veh_vel) > 0:
                veh_vel = np.mean(veh_vel)
            else:
                veh_vel = self.k.network.speed_limit(edge_id)
            veh_vel /= max_speed
            
            if edge in ["center"]:
                states[rl_id] = np.array(list(states[rl_id]) + [rl_dist, veh_vel, 1.0, 0.0])
            else:
                states[rl_id] = np.array(list(states[rl_id]) + [rl_dist, veh_vel, merge_distance, merge_vel])
            print(rl_id,len(states[rl_id]))
        return states

class MultiAgentHighwayPOEnvMerge4CollaborateNormalizedToDistance(MultiAgentHighwayPOEnvMerge4NormalizedToDistance):
    def compute_reward(self, rl_actions, **kwargs):
        if rl_actions is None:
            return {}

        rewards = {}
        if "eta1" in self.env_params.additional_params.keys():
            eta1 = self.env_params.additional_params["eta1"]
            eta2 = self.env_params.additional_params["eta2"]
        else:
            eta1 = 0.9
            eta2 = 0.1
        reward1 = -0.1
        reward2 = average_velocity(self)/300
        reward  = reward1 * eta1 + reward2 * eta2
        for rl_id in self.k.vehicle.get_rl_ids():
            rewards[rl_id] = reward
        return rewards

class MultiAgentHighwayPOEnvMerge4CollaborateNormalizedToTime(MultiAgentHighwayPOEnvMerge4NormalizedToTime):
    def compute_reward(self, rl_actions, **kwargs):
        if rl_actions is None:
            return {}

        rewards = {}
        if "eta1" in self.env_params.additional_params.keys():
            eta1 = self.env_params.additional_params["eta1"]
            eta2 = self.env_params.additional_params["eta2"]
        else:
            eta1 = 0.9
            eta2 = 0.1
        reward1 = -0.1
        reward2 = average_velocity(self)/300
        reward  = reward1 * eta1 + reward2 * eta2
        for rl_id in self.k.vehicle.get_rl_ids():
            rewards[rl_id] = reward
        return rewards



