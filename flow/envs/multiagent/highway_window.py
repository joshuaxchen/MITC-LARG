import numpy as np
from gym.spaces.box import Box
from flow.core.rewards import desired_velocity, average_velocity
from flow.envs.multiagent.base import MultiEnv
from flow.envs.multiagent.highway import MultiAgentHighwayPOEnvWindow
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

class MultiAgentHighwayPOEnvWindowFull(MultiAgentHighwayPOEnvWindow):
    @property
    def observation_space(self):
        #See class definition
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
            veh_dist = float('inf')
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
        junctions = set(self.k.network.get_junction_list())
        max_speed = 30.0 #m/s
        max_length = 1000.0 #m
        for rl_id in states:
            edge_id = self.k.vehicle.get_edge(rl_id)
            lane = self.k.vehicle.get_lane(rl_id)
            edge_len = self.k.network.edge_length(edge_id)
            rl_position = self.k.vehicle.get_position(rl_id)
            rl_dist = max(edge_len-rl_position, 0) / max_length
            veh_vel = []
            for veh_id in self.k.vehicle.get_ids_by_edge(edge_id):
                veh_position = self.k.vehicle.get_position(veh_id)
                if veh_position > rl_position:
                    veh_vel.append(self.k.vehicle.get_speed(veh_id))
            if len(veh_vel) > 0:
                veh_vel = np.mean(veh_vel)
            else:
                veh_vel = 30.0 #self.k.network.speed_limit(edge_id)
            veh_vel /= max_speed
            merge_dist, merge_vel = self._merging_vehicle_forward_pass(edge_id, lane, edge_id, junctions)
            merge_dist /= max_length
            merge_vel /= max_speed
            if merge_dist == float('inf'):
                merge_dist = 1.0
            states[rl_id] = np.array(list(states[rl_id]) + [rl_dist, veh_vel, merge_dist, merge_vel])
        #if states and merge_vel>0:
        #    print(states)
        #    from IPython import embed; embed()
        return states

class MultiAgentHighwayPOEnvWindowFullCollaborate(MultiAgentHighwayPOEnvWindowFull):
    def compute_reward(self, rl_actions, **kwargs):
        if rl_actions is None:
            return {}

        rewards = {}
        eta1 = 0.9
        eta2 = 0.1
        reward1 = -0.1
        current_rl_vehs = self.rl_veh
        edges = []
        for veh_id in current_rl_vehs:
            edge = self.k.vehicle.get_edge(veh_id)
            if edge not in edges:
                edges.append(edge)
        interested_vehs = self.k.vehicle.get_ids_by_edge(edges)
        if len(interested_vehs) >0:
            reward2 = np.mean(self.k.vehicle.get_speed(interested_vehs))/300
        else:
            reward2 = 0

        reward  = reward1 * eta1 + reward2 * eta2
        for rl_id in self.rl_veh:
            rewards[rl_id] = reward
        return rewards

