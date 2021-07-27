from flow.envs.multiagent.highway import MultiAgentHighwayPOEnv
import numpy as np
from gym.spaces.box import Box
from flow.core.rewards import desired_velocity, average_velocity
from flow.envs.multiagent.base import MultiEnv
import collections
import os
from copy import deepcopy

class MultiAgentHighwayPOEnvDistanceMergeInfoMOR(MultiAgentHighwayPOEnv):
    @property
    def observation_space(self):
        return Box(low=-1, high=1, shape=(7, ), dtype=np.float32)

    def get_state(self):
        """See class definition."""
        obs = {}

        # normalizing constants
        max_speed = self.k.network.max_speed()
        max_length = self.k.network.length()
        for rl_id in self.k.vehicle.get_rl_ids():
            this_speed = self.k.vehicle.get_speed(rl_id)
            lead_id = self.k.vehicle.get_leader(rl_id)
            follower = self.k.vehicle.get_follower(rl_id)

            if lead_id in ["", None]:
                # in case leader is not visible
                lead_speed = max_speed
                lead_head = max_length
            else:
                lead_speed = self.k.vehicle.get_speed(lead_id)
                lead_head = self.k.vehicle.get_headway(rl_id)

            if follower in ["", None]:
                # in case follower is not visible
                follow_speed = 0
                follow_head = max_length
            else:
                follow_speed = self.k.vehicle.get_speed(follower)
                follow_head = self.k.vehicle.get_headway(follower)
            
            veh_x = self.k.vehicle.get_x_by_id(rl_id)
            merge_edge = None
            merge_edge_pos = float('inf')
            for e in self.env_params.additional_params['merging_edges']:
                p = self.k.network.total_edgestarts_dict[e]
                # TODO (yulin): edge_pos should be merge_edge_pos
                if p < edge_pos and p > veh_x:
                    merge_edge_pos = p
                    merge_edge = e
            merge_distance = 1
            if merge_edge is not None:
                len_merge = self.k.network.edge_length("merge_edge")
                merge_vehs = self.k.vehicle.get_ids_by_edge(merge_edge)
                merge_dists = [self.k.vehicle.get_position(veh) for veh in merge_vehs]
                if len(merge_dists) > 0:
                    merge_pos = max(merge_dists)
                    merge_distance = (len_merge - merge_pos)/len_merge

            edge = self.k.vehicle.get_edge(rl_id)
            length = self.k.network.edge_length(edge)
            pos = self.k.vehicle.get_position(rl_id)
            distance = (length - pos)/(length)

            observation = np.array([
                this_speed / max_speed,
                (lead_speed - this_speed) / max_speed,
                lead_head / max_length,
                (this_speed - follow_speed) / max_speed,
                follow_head / max_length,
                np.clip(distance,-1,1),
                np.clip(merge_distance,-1,1),

            ])

            obs.update({rl_id: observation})

        return obs
    
class MultiAgentHighwayPOEnvDistanceMergeInfoCollaborateMOR(MultiAgentHighwayPOEnvDistanceMergeInfoMOR):
    def compute_reward(self, rl_actions, **kwargs):
        if rl_actions is None:
            return {}

        rewards = {}
        eta1 = 0.5
        eta2 = 0.5
        reward1 = -0.1
        reward2 = average_velocity(self)/300
        reward  = reward1 * eta1 + reward2 * eta2
        for rl_id in self.k.vehicle.get_rl_ids():
            rewards[rl_id] = reward
        return rewards

class MultiAgentHighwayPOEnvMerge4MOR(MultiAgentHighwayPOEnv):
    @property
    def observation_space(self):
        #See class definition
        # 5-tule + distance + merge info + ?
        return Box(-float('inf'), float('inf'), shape=(9,), dtype=np.float32)

    def _closest_vehicle(self, edge, lane, base_edge):
        if edge == base_edge: return float('inf'), 0
        if edge == '': return float('inf'), 0
        veh = self.k.vehicle.get_ids_by_edge(edge)
        if len(veh) == 0:
            veh_pos = 0
            veh_id = None
        else:
            veh_ind = np.argmax(self.k.vehicle.get_position(veh))
            veh_id = veh[veh_ind]
            veh_pos = self.k.vehicle.get_position(veh_id)
        veh_dist = self.k.network.edge_length(edge)-veh_pos
        if veh_id:
            veh_speed = self.k.vehicle.get_speed(veh_id)
        else:
            veh_speed = 0
        return veh_dist, veh_speed

    def _merging_vehicle_backward_pass(self, edge, lane, base_edge, junctions):
        try:
            return min(self._merging_vehicle_backward_pass(e, l, base_edge, junctions) if e in junctions else self._closest_vehicle(e, l, base_edge)
                    for e,l in self.k.network.prev_edge(edge, lane))
        except ValueError:
            return float('inf'), 0

    def _merging_vehicle_forward_pass(self, edge, lane, base_edge, junctions):
        try:
            return min(self._merging_vehicle_forward_pass(e, l, base_edge, junctions) if e in junctions else self._merging_vehicle_backward_pass(e, l, base_edge, junctions)
                    for e,l in self.k.network.next_edge(edge, lane))
        except ValueError:
            return float('inf'), 0

    def get_state(self):
        states = super().get_state() # 5 state
        junctions = set(self.k.network.get_junction_list())

        # normalizing constants
        max_speed = 30.0 #self.k.network.max_speed()
        max_length = 1000.0#self.k.network.length()
        
        for rl_id in states:
            veh_x = self.k.vehicle.get_x_by_id(rl_id)
            merge_edge = None
            merge_edge_pos = float('inf')
            # find the closest merging edge
            for e in self.env_params.additional_params['merging_edges']:
                p = self.k.network.total_edgestarts_dict[e]
                if p < merge_edge_pos and p > veh_x:
                    merge_edge_pos = p
                    merge_edge = e
            # obtain the distance to the merge and the velocity of the merging
            # vehicle
            merge_distance = 1
            merge_vel = 0
            if merge_edge is not None:
                len_merge = self.k.network.edge_length(merge_edge)
                merge_vehs = self.k.vehicle.get_ids_by_edge(merge_edge)
                merge_dists = [(self.k.vehicle.get_position(veh), veh) for veh in merge_vehs]
                if len(merge_dists) > 0:
                    merge_pos, merge_veh = max(merge_dists, key=lambda i:i[0])
                    merge_distance = (len_merge - merge_pos)/len_merge # normalized by len_merge 
                    merge_vel = self.k.vehicle.get_speed(merge_veh)
            # TODO (yulin): what if there is not merging vehicle
            edge_id = self.k.vehicle.get_edge(rl_id)
            lane = self.k.vehicle.get_lane(rl_id)
            edge_len = self.k.network.edge_length(edge_id)
            rl_position = self.k.vehicle.get_position(rl_id)
            rl_x = self.k.vehicle.get_x_by_id(rl_id)
            #rl_dist = max(edge_len-rl_position, 0) / max_length
            veh_vel = []
            
            #calculate RL distance to the center junction
            # edge = self.k.vehicle.get_edge(rl_id)
            # length = self.k.network.edge_length(edge)
            #rl_dist = 1
            # TODO (yulin): Is this negative?
            rl_dist = (edge_len-rl_position)/edge_len
            #if edge in ["inflow_highway","left","center"]:
            #    rl_dist = (veh_x - center_x)/(center_x)
            #else:
            #    pass #FIXME: not yet implemented
            num_veh_ahead = 0 
            # TODO (yulin): number of vehicles in current edge or the edge
            # ahead ?
            for veh_id in self.k.vehicle.get_ids_by_edge(edge_id):
                veh_position = self.k.vehicle.get_x_by_id(veh_id)
                if veh_position > rl_x:
                    veh_vel.append(self.k.vehicle.get_speed(veh_id))
                    num_veh_ahead += 1
            # mean speed of the vehicles ahead
            if len(veh_vel) > 0:
                veh_vel = np.mean(veh_vel)
            else:
                veh_vel = self.k.network.speed_limit(edge_id)
            veh_vel /= max_speed
            
            if edge_id in ["highway_2"]: # TODO (yulin): what is center? probably highway_2
                states[rl_id] = np.array(list(states[rl_id]) + [rl_dist, veh_vel, 1.0, 0.0])
            else:
                states[rl_id] = np.array(list(states[rl_id]) + [rl_dist, veh_vel, merge_distance, merge_vel])
        #print(states)
        return states


class MultiAgentHighwayPOEnvMerge4CollaborateMOR(MultiAgentHighwayPOEnvMerge4MOR):
# AAMAS policy
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
