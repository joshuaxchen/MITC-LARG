import numpy as np
from gym.spaces.box import Box
from flow.core.rewards import desired_velocity, average_velocity
from flow.envs.multiagent.base import MultiEnv
from flow.envs.multiagent.highway import MultiAgentHighwayPOEnv
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

class MultiAgentI696POEnvParameterizedWindowSize(MultiAgentHighwayPOEnv):

    def __init__(self, env_params, sim_params, network, simulator='traci'):
        if "window_size" not in env_params.additional_params:
                raise KeyError(
                    'Environment parameter "{}" not supplied'.format("window_size"))

        super().__init__(env_params, sim_params, network, simulator)
        self.junction_before, self.junction_after=env_params.additional_params['window_size']
        self.rl_to_ignore=list()

    @property
    def observation_space(self):
        #See class definition
        return Box(-float('inf'), float('inf'), shape=(9,), dtype=np.float32)

    def collect_next_edge(self, edge_id):
        next_junction=self.k.network.next_edge(edge_id, 0)
        if len(next_junction)==0:
            #print("no next_junction for",edge_id)
            return None
        #print("next_junction", next_junction)
        next_edge=self.k.network.next_edge(next_junction[0][0], 0)
        #print("next_edge", next_edge)
        return next_edge[0][0]

    def from_veh_to_edge(self, veh_id, target_edge_id):
        vehs_ahead=list()
        veh_edge_id=self.k.vehicle.get_edge(veh_id)
        edge_length=self.k.network.edge_length(veh_edge_id)
        next_edge_id=veh_edge_id
        v_ids_on_edge=self.k.vehicle.get_ids_by_edge(veh_edge_id)
        veh_x=self.k.vehicle.get_x_by_id(veh_id)
        for v_id in v_ids_on_edge:
            v_x=self.k.vehicle.get_x_by_id(v_id)
            if v_x<veh_x: # ahead of veh_id
                vehs_ahead.append(v_id)
        next_edge_id=self.collect_next_edge(veh_edge_id)
        # next_edge_id [(':4308145956_0', 0)]
        while next_edge_id is not None and next_edge_id != target_edge_id: 
            veh_ids_on_edge=self.k.vehicle.get_ids_by_edge(next_edge_id)
            vehs_ahead.extend(veh_ids_on_edge)
            next_edge_id=self.collect_next_edge(next_edge_id)
        return vehs_ahead

    def first_veh_at_edge_and_its_prev(self, from_edge, to_edge):
        # return the absolute distance and speed of the first merging vehicle.
        # if there is no merging vehicle, then the distance is close to inf, and the velocity is 0
        veh_ids_on_edge=None
        edge_with_first_veh=None
        while from_edge != to_edge:
            temp_vehs=self.k.vehicle.get_ids_by_edge(from_edge)
            if temp_vehs and len(temp_vehs)>0:
                veh_ids_on_edge=temp_vehs
                edge_with_first_veh=from_edge
            from_edge=self.collect_next_edge(from_edge)
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
        from_edge=self.collect_next_edge(edge_with_first_veh)
        veh_vel=0
        if first_veh:
            veh_vel=self.k.vehicle.get_speed(first_veh)
        while from_edge != to_edge:
            len_of_veh_to_junction+=self.k.network.edge_length(from_edge)
        return first_veh, len_of_veh_to_junction, veh_vel

    def get_state(self):
        states = super().get_state()
        #junctions = set(self.k.network.get_junction_list())

        # normalizing constants
        max_speed = 30.0 #self.k.network.max_speed()
        #max_length = 1000.0 #self.k.network.length()
        merge_vehs = self.k.vehicle.get_ids_by_edge(["bottom","inflow_merge"])
        #merge_dists = [self.k.vehicle.get_x(veh) for veh in merge_vehs]
        self.rl_to_ignore=list()       
        for rl_id in states:
            #print("original len", len(states[rl_id]))
            # compute the closest junction to the rl vehicle
            within_junctions=list()
            rl_x=self.k.vehicle.get_x_by_id(rl_id)
            smallest_dist=-1
            closest_edge=None
            for junction_start in main_roads_after_junction_from_right_to_left:
                edge_start=self.k.network.total_edgestarts_dict[junction_start]
                print("edge: ", junction_start, "start at", edge_start)
                if edge_start>rl_x:
                    continue
                if rl_x-edge_start<smallest_dist or smallest_dist<0:
                    smallest_dist=rl_x-edge_start
                    closest_edge=junction_start
            if closest_edge is not None and smallest_dist<=self.junction_before:
                vehs_ahead=self.from_veh_to_edge(rl_id, closest_edge)
                within_junctions.append((closest_edge, smallest_dist, vehs_ahead))
            
            if len(within_junctions)>1:
                print("There are multiple junctions close to ", rl_id, ":", ",".join(within_junctions))
                exit(-1)
            elif len(within_junctions)==0: # The vehicle is not within any window. It should behave like a human
                # None observation
                self.rl_to_ignore.append(rl_id)
                continue
            #print("within_junction", within_junctions)
            # compute the average velocity of the vehicles ahead
            closest_junction, dist_from_rl_to_junction, vehs_ahead=within_junctions[0]
            rl_dist=-1*dist_from_rl_to_junction/self.junction_before
            veh_vel=list()
            for veh_id in vehs_ahead:
                veh_vel.append(self.k.vehicle.get_speed(veh_id))
            if len(veh_vel) > 0:
                veh_vel = np.mean(veh_vel)
            else:
                rl_edge_id= self.k.vehicle.get_edge(rl_id)
                veh_vel = self.k.network.speed_limit(rl_edge_id)
            veh_vel/=max_speed
            
            #print("veh_vel", veh_vel)
            # compute the merge information 
            junction_index=main_roads_after_junction_from_right_to_left.index(closest_junction)
            merge_edge=merge_roads_from_right_to_left[junction_index]
            first_merge_veh, dist_of_first_merge_veh_to_junction, vel_of_first_merge_veh=self.first_veh_at_edge_and_its_prev(merge_edge, closest_junction)
            vel_of_first_merge_veh/=max_speed 
            #max_distance=1 # TODO: set up the maximum distance to be the length of the window
            #max_distance=self.junction_before
            len_merge=200
            #max_merging_time=100
            if dist_of_first_merge_veh_to_junction < len_merge:
                dist_of_first_merge_veh_to_junction=(len_merge-2*(len_merge-dist_of_first_merge_veh_to_junction))/len_merge
            else:
                dist_of_first_merge_veh_to_junction=1
            #if len(states[rl_id])==9:
            #    states[rl_id][-4] = rl_dist
            #    states[rl_id][-3] = veh_vel
            #    states[rl_id][-2] = dist_of_first_merge_veh_to_junction
            #    states[rl_id][-1] = vel_of_first_merge_veh
            #elif len(states[rl_id]==5):
            states[rl_id] = np.array(list(states[rl_id]) + [rl_dist, veh_vel, dist_of_first_merge_veh_to_junction, vel_of_first_merge_veh])
            #print("state", states[rl_id])
            #print("state", rl_id, len(states[rl_id]))
            #states[rl_id]=np.array([1]*9)
        for rl_id in self.rl_to_ignore:
            del states[rl_id]
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
        for rl_id in self.rl_to_ignore:
            del rewards[rl_id]
        return rewards


