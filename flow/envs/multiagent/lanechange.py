from flow.envs.multiagent import MultiAgentHighwayPOEnvMerge4Collaborate
from flow.envs.multiagent import MultiAgentHighwayPOEnv
from flow.core.rewards import desired_velocity, average_velocity
import numpy as np
from gym.spaces.box import Box

class LeftLaneOvalHighwayPOEnvMerge4(MultiAgentHighwayPOEnv):
    @property
    def observation_space(self):
        #See class definition
        # basic 5 states
        # leader and follower at the other lane 
        # number of vehicles on the right lane that are about to move
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
        states = super().get_state()
                
        for rl_id in states:
            edge_id = self.k.vehicle.get_edge(rl_id)
            lane = self.k.vehicle.get_lane(rl_id)

            lead_ids = self.k.vehicle.get_lane_leaders(rl_id)
            follow_ids = self.k.vehicle.get_lane_followers(rl_id)

            headways= self.k.vehicle.get_lane_headways(rl_id)
            tailways= self.k.vehicle.get_lane_tailways(rl_id)
            all_lane_ids=[i for i in range(0, len(headways))]
            
            other_lane_leader=None
            shortest_headway=float('inf')
            other_lane_leader_id=None

            other_lane_follower=None
            shortest_tailway=float('inf')
            other_lane_follower_id=None

            max_speed = 30.0
            max_length = 1000.0

            for other_lane in all_lane_ids:
                if lane==other_lane:
                    continue
                h=headways[other_lane] 
                t=tailways[other_lane] 

                if h <shortest_headway:
                    shortest_headway=h
                    other_lane_leader_id=lead_ids[other_lane]
                if t < shortest_tailway:
                    shortest_tailway=t
                    other_lane_follower_id=follow_ids[other_lane]

            other_lane_leader_head=0
            other_lane_leader_speed=0
            other_lane_follower_tail=0
            other_lane_follower_speed=0
            if other_lane_leader_id in ["", None]:
                other_lane_leader_head=max_length
                other_lane_leader_speed=max_speed
            else:
                other_lane_leader_speed=self.k.vehicle.get_speed(other_lane_leader_id)
                other_lane_leader_head=shortest_headway
            
            if other_lane_follower_id in ["", None]:
                other_lane_follower_tail=max_length
                other_lane_follower_speed=max_speed
            else:
                other_lane_follower_tail=shortest_tailway
                other_lane_follower_speed=self.k.vehicle.get_speed(other_lane_follower_id)
            
            states[rl_id] = np.array(list(states[rl_id]) + [other_lane_leader_speed/max_speed, other_lane_leader_head/max_length, other_lane_follower_speed/max_speed, other_lane_follower_tail/max_length])
        #print(states)
        return states

class LeftLaneOvalAboutToMergeHighwayPOEnvMerge4(LeftLaneOvalHighwayPOEnvMerge4):
    @property
    def observation_space(self):
        #See class definition
        # basic 5 states
        # leader and follower at the other lane 
        # number of vehicles on the right lane that are about to move
        return Box(-float('inf'), float('inf'), shape=(8,), dtype=np.float32)

    def get_state(self):
        states = super().get_state()

        # obtain the number of vehicles that are about to change lane
        # the lateral location is specified with respect to the center line of the lane, negative goes below, postive goes above
        # it seems that all vehicles that are larger than 1 from the right are likely to merge

        max_length = 1000.0
        for rl_id in states:
            edge_id=self.k.vehicle.get_edge()
            lane_id= self.k.vehicle.get_lane(rl_id)
            rl_x=self.k.vehicle.get_x_by_id(rl_id)
            # find the closest vehicle that is about to merge to this lane
            closest_x=float('inf')
            closest_merger=None
            for veh_id in self.k.vehicle.get_ids_by_edge(edge_id):
                veh_lane_id= self.k.vehicle.get_lane(veh_id)
                if lane_id<=veh_lane_id or veh_id==rl_id: # on the left or is current vehicle
                    continue
                veh_x=self.k.vehicle.get_x_by_id(veh_id)
                if veh_x<rl_x:
                    continue
                lateral_pos=self.k.vehicle.get_lateral_lane_pos(veh_id) 
                if lateral_pos>=1.0:
                    # it is about to merge the left lane
                    if closest_x>veh_x:
                        closest_x=veh_x
                        closest_merger=veh_id
            closest_dist=closest_x-rl_x
            if closest_merger is None:
                closest_dist=1
            else:
                closest_dist/=max_length
            states[rl_id] = np.array(list(states[rl_id])+[closest_dist])                   
        return states
   

class LeftLaneOvalHighwayPOEnvMerge4Collaborate(LeftLaneOvalHighwayPOEnvMerge4):
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


class LeftLaneOvalAboutToMergeHighwayPOEnvMerge4Collaborate(LeftLaneOvalAboutToMergeHighwayPOEnvMerge4):
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

