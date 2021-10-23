import numpy as np
from gym.spaces.box import Box
from flow.core.rewards import desired_velocity, average_velocity
from flow.envs.multiagent.base import MultiEnv
from flow.envs.multiagent.highway import MultiAgentHighwayPOEnvWindow,MultiAgentHighwayPOEnvMerge4
from flow.envs.multiagent import MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate #MultiAgentHighwayPOEnvWindowFullCollaborate
import collections
import os
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
}

main_roads_after_junction_from_right_to_left=["422314897#0", "40788302", "124433730#2-AddedOnRampEdge"]
merge_roads_from_right_to_left=["124433709.427", "8666737", "178253095"]

class MultiAgentI696POEnvParameterizedWindowSize(MultiAgentHighwayPOEnvMerge4):

    def __init__(self, env_params, sim_params, network, simulator='traci'):
        if "window_size" not in env_params.additional_params:
                raise KeyError(
                    'Environment parameter "{}" not supplied'.format("window_size"))

        self.junction_before, self.junction_after=env_params.additional_params['window_size']

        super().__init__(env_params, sim_params, network, simulator)

    def from_veh_to_edge(self, veh_id, target_edge_id):
        vehs_ahead=list()
        veh_edge_id=self.k.vehicle.get_edge(veh_id)
        edge_length=self.k.network.edge_length(veh_edge_id)
        next_edge_id=veh_edge_id
        total_length=edge_length - self.k.vehicle.get_position(veh_id)
        veh_ids_on_edge=self.k.vehicle.get_ids_by_edge(veh_edge_id)
        for v_id in veh_ids_on_edge:
            v_pos=self.k.vehicle.get_position(v_id)
            if v_pos>total_length: # ahead of veh_id
                vehs_ahead.append(v_id)
        next_edge_id=self.k.network.next_edge(veh_edge_id,0)
        while next_edge_id != target_edge_id:
            total_length+=self.k.network.edge_length(next_edge_id)
            next_edge_id=self.k.network.next_edge(veh_edge_id,0)
            veh_ids_on_edge=self.k.vehicle.get_ids_by_edge(veh_edge_id)
            vehs_ahead.extend(veh_ids_on_edge)
        return total_length, vehs_ahead

    def first_veh_at_edge_and_its_prev(self, from_edge, to_edge):
        veh_ids_on_edge=None
        edge_with_first_veh=None
        while from_edge != to_edge:
            temp_vehs=self.k.vehicle.get_ids_by_edge(from_edge)
            if temp_vehs and len(temp_vehs)>0:
                veh_ids_on_edge=temp_vehs
                edge_with_first_veh=from_edge
            from_edge=self.k.network.next_edge(from_edge,0)
        # find the first merging vehicle
        largest_pos=-1
        first_veh=None
        for veh_id in veh_ids_on_edge:
            veh_pos=self.k.vehicle.get_position(veh_id)
            if veh_pos>largest_pos:
                largest_pos=veh_pos
                first_veh=veh_id
        # find merging distance and velocity of the first vehicle
        edge_len=float('inf')-2
        if edge_with_first_veh:
            edge_len=self.k.network.edge_length(edge_with_first_veh)
        len_of_veh_to_junction=edge_len-largest_pos
        from_edge=self.k.network.next_edge(edge_with_first_veh)
        veh_vel=0
        if first_veh:
            veh_vel=self.k.vehicle.get_speed(first_veh)
        while from_edge != to_edge:
            len_of_veh_to_junction+=self.k.network.edge_length(from_edge)
        return first_veh, len_of_veh_to_junction, veh_vel

    def get_state(self):
        states = super().get_state()
        junctions = set(self.k.network.get_junction_list())

        # normalizing constants
        max_speed = 30.0 #self.k.network.max_speed()
        max_length = 1000.0#self.k.network.length()
        merge_vehs = self.k.vehicle.get_ids_by_edge(["bottom","inflow_merge"])
        #merge_dists = [self.k.vehicle.get_x(veh) for veh in merge_vehs]
               
        
        for rl_id in states:
            # compute the closest junction to the rl vehicle
            within_junctions=list()
            for junction_start in main_roads_after_junction_from_right_to_left:
                for rl_id in self.k.vehicle.get_rl_ids():
                    dist_from_rl_to_junction, vehs_ahead=self.from_veh_to_edge(rl_id, junction_start)
                    if dist_from_rl_to_junction<self.junction_before: # TODO: junction_after?
                        within_junctions.append((junction_start, dist_from_rl_to_junction,vehs_ahead))
            if len(within_junctions)>1:
                print("There are multiple junctions close to ", rl_id, ":", ",".join(within_junctions))
                exit(-1)
            elif len(within_junction)==0: # The vehicle is not within any window. It should behave like a human
                # None observation
                del states[rl_id]
                continue

            # compute the average velocity of the vehicles ahead
            closest_junction, dist_from_rl_to_junction, vehs_ahead=within_junctions[0]
            rl_dist=dist_from_rl_to_junction/self.junction_before
            veh_vel=list()
            for veh_id in vehs_ahead:
                veh_vel.append(self.k.vehicle.get_speed(veh_id))
            if len(veh_vel) > 0:
                veh_vel = np.mean(veh_vel)
            else:
                veh_vel = self.k.network.speed_limit(edge_id)
            
            # compute the merge information 
            junction_index=main_roads_after_junction_from_right_to_left.index(closet_junction)
            merge_edge=merge_roads_from_right_to_left[junction_index]
            first_merge_veh, dist_of_first_merge_veh_to_junction, vel_of_first_merge_veh=first_veh_at_edge_and_its_prev(merge_edge, closet_junction)
            vel_of_first_merge_veh/=max_speed 
            merge_distance = 1
            max_distance=1 # TODO: set up the maximum distance to be the length of the window
            max_distance=self.junction_before
            if dist_of_first_merge_veh_to_junction < max_distance:
                dist_of_first_merge_veh_to_junction/=max_distance
                        
            states[rl_id] = np.array(list(states[rl_id]) + [rl_dist, veh_vel, dist_of_first_merge_veh_to_junction, vel_of_first_merge_veh])
        return states


class MultiAgentI696POEnvParameterizedWindowSizeCollaborate(MultiAgentI696POEnvParameterizedWindowSize):

    def compute_reward(self, rl_actions, **kwargs):
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


