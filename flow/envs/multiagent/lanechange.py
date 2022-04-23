from flow.envs.multiagent import MultiAgentHighwayPOEnvMerge4Collaborate
from flow.envs.multiagent import MultiAgentHighwayPOEnv, MultiAgentHighwayPOEnvMerge4
from flow.core.rewards import desired_velocity, average_velocity
import numpy as np
from gym.spaces.box import Box
from statistics import mean
from IPython.core.debugger import set_trace
from collections import defaultdict

class DoubleLaneController(MultiAgentHighwayPOEnvMerge4):
    def __init__(self, env_params, sim_params, network, simulator='traci'):
        super().__init__(env_params, sim_params, network, simulator)
    
    @property
    def observation_space(self):
        #See class definition
        # 9 states: basic 5 states + average speed of the vehicles on the right lane
        # average speed ahead on the right lane
        return Box(-float('inf'), float('inf'), shape=(10,), dtype=np.float32)

    def get_state(self):
        states = super().get_state()
        BEFORE_MERGE = 588
        LOOK_AHEAD = 120
        MAX_SPEED = 30
        # print("rl_ids", self.k.vehicle.get_rl_ids())
        for rl_id in states:
            veh_ahead_on_the_right = list()
            self_veh_x = self.k.vehicle.get_x_by_id(rl_id)
            for other_veh_id in self.k.vehicle.get_ids():
                lane_id = self.k.vehicle.get_lane(other_veh_id)
                other_veh_x = self.k.vehicle.get_x_by_id(other_veh_id)
                if lane_id == 0 and self_veh_x < other_veh_x and other_veh_x < BEFORE_MERGE and other_veh_x < self_veh_x + LOOK_AHEAD:  # 120
                    other_veh_vel = self.k.vehicle.get_speed(other_veh_id)
                    veh_ahead_on_the_right.append(other_veh_vel)
            if len(veh_ahead_on_the_right) == 0:
                mean_vel = 1 
            else:
                mean_vel = mean(veh_ahead_on_the_right) / MAX_SPEED
            states[rl_id] = np.array(list(states[rl_id]) + [mean_vel])
        # print("states", states)

        return states

    def avg_velocity_behind_and_ahead(self):
        # print("rl_ids", self.k.vehicle.get_rl_ids())
        result = dict()
        for rl_id in self.k.vehicle.get_rl_ids():
            rl_lane_id = self.k.vehicle.get_lane(rl_id)
            rl_veh_x = self.k.vehicle.get_x_by_id(rl_id)
            veh_ahead_same_lane = list()
            veh_behind_same_lane = list()
            for other_veh_id in self.k.vehicle.get_ids():
                if other_veh_id == rl_id:
                    continue
                other_veh_lane_id = self.k.vehicle.get_lane(other_veh_id)
                other_veh_x = self.k.vehicle.get_x_by_id(other_veh_id)
                other_veh_vel = self.k.vehicle.get_speed(other_veh_id)
                # print(rl_id, rl_veh_x, rl_lane_id, other_veh_id, other_veh_x, other_veh_lane_id)
                if rl_veh_x < other_veh_x:  # the other veh is ahead 
                    if rl_lane_id == other_veh_lane_id: # same lane
                        veh_ahead_same_lane.append(other_veh_vel)
                    else: # different lane
                        pass 
                else: # the other veh is behind
                    if rl_lane_id == other_veh_lane_id:
                        veh_behind_same_lane.append(other_veh_vel)

            mean_vel_behind = 0            
            if len(veh_behind_same_lane) == 0:
                mean_vel_behind = 0 # 0 means this is undesired, since no vehicles are behind and the rl must have blocked the traffic. 
            else:
                mean_vel_behind = mean(veh_behind_same_lane) 

            mean_vel_ahead = 0            
            if len(veh_ahead_same_lane) == 0:
                mean_veh_ahead = 1 # 1 means that this is desired, since the congested traffic ahead has exited the network
            else:
                mean_vel_ahead = mean(veh_ahead_same_lane) 
                 
            result[rl_id] = [mean_vel_behind, mean_vel_ahead]
        return result 

    def compute_reward(self, rl_actions, **kwargs):
        # print("compute reward")
        if rl_actions is None:
            return {}

        rewards = {}
        if "eta1" in self.env_params.additional_params.keys():
            eta1 = self.env_params.additional_params["eta1"]
            eta2 = self.env_params.additional_params["eta2"]
        else:
            eta1 = 0.9
            eta2 = 0.1

        if "eta3" in self.env_params.additional_params.keys():
            eta3 = self.env_params.additional_params["eta3"]
        else:
            eta3 = 0

        reward1 = -0.1
        # reward2 = average_velocity(self)/300
        reward = reward1 * eta1 
        avg_velocity_behind_ahead_dict = self.avg_velocity_behind_and_ahead()
        # print(avg_velocity_behind_ahead_dict)
        for rl_id in self.k.vehicle.get_rl_ids():
            avg_vel_behind, avg_vel_ahead = avg_velocity_behind_ahead_dict[rl_id][0], avg_velocity_behind_ahead_dict[rl_id][1]
            reward2 = avg_vel_behind * eta2 + avg_vel_ahead * eta2
            rewards[rl_id] = reward + reward2

        return rewards

class SingleLaneController(DoubleLaneController):
    
    @property
    def observation_space(self):
        #See class definition
        # 9 states: basic 5 states + average speed of the vehicles on the right lane
        # average speed ahead on the right lane
        return Box(-float('inf'), float('inf'), shape=(9,), dtype=np.float32)

    def get_state(self):
        states = super().get_state()
        for rl_id in states:
            states[rl_id] = states[rl_id][0:9]
        # print("states", states)

        return states

    def compute_reward(self, rl_actions, **kwargs):
        # print("compute reward")
        if rl_actions is None:
            return {}

        rewards = {}
        if "eta1" in self.env_params.additional_params.keys():
            eta1 = self.env_params.additional_params["eta1"]
            eta2 = self.env_params.additional_params["eta2"]
        else:
            eta1 = 0.9
            eta2 = 0.1

        if "eta3" in self.env_params.additional_params.keys():
            eta3 = self.env_params.additional_params["eta3"]
        else:
            eta3 = 0

        reward1 = -0.9
        # reward2 = average_velocity(self)/300
        reward = reward1 * eta1 
        avg_velocity_behind_ahead_dict = self.avg_velocity_behind_and_ahead()
        # print(avg_velocity_behind_ahead_dict)

        MAX_SPEED = 30
        for rl_id in self.k.vehicle.get_rl_ids():
            avg_vel_behind, avg_vel_ahead = avg_velocity_behind_ahead_dict[rl_id][0], avg_velocity_behind_ahead_dict[rl_id][1]
            rl_veh_vel = self.k.vehicle.get_speed(rl_id)
            reward2 = avg_vel_behind/MAX_SPEED * eta3 + avg_vel_ahead/MAX_SPEED * eta2 + rl_veh_vel/MAX_SPEED * eta3
            rewards[rl_id] = reward + reward2

        return rewards


class LeftLaneHeadwayControlledMerge4(MultiAgentHighwayPOEnvMerge4):
    def __init__(self, env_params, sim_params, network, simulator='traci'):
        super().__init__(env_params, sim_params, network, simulator)
        self.right_before_rls = defaultdict(lambda: set())
        # print("left lane headway controlled")

    @property
    def observation_space(self):
        #See class definition
        # basic 5 states + average speed of the vehicles on the right lane
        # leader and follower at the other lane
        # number of vehicles on the right lane that are about to move
        return Box(-float('inf'), float('inf'), shape=(10,), dtype=np.float32)

    def get_state(self):
        states = super().get_state()
        BEFORE_MERGE = 588
        LOOK_AHEAD = 120
        MAX_SPEED = 30
        # print("rl_ids", self.k.vehicle.get_rl_ids())
        for rl_id in states:
            veh_ahead_on_the_right = list()
            self_veh_x = self.k.vehicle.get_x_by_id(rl_id)
            for other_veh_id in self.k.vehicle.get_ids():
                lane_id = self.k.vehicle.get_lane(other_veh_id)
                other_veh_x = self.k.vehicle.get_x_by_id(other_veh_id)
                if lane_id == 0 and self_veh_x < other_veh_x and other_veh_x < BEFORE_MERGE and other_veh_x < self_veh_x + LOOK_AHEAD:  # 120
                    other_veh_vel = self.k.vehicle.get_speed(other_veh_id)
                    veh_ahead_on_the_right.append(other_veh_vel)
            if len(veh_ahead_on_the_right) == 0:
                mean_vel = 1 
            else:
                mean_vel = mean(veh_ahead_on_the_right) / MAX_SPEED
            states[rl_id] = np.array(list(states[rl_id]) + [mean_vel])
        # print("states", states)
        return states

    def compute_reward(self, rl_actions, **kwargs):
        # print("compute reward")
        if rl_actions is None:
            return {}

        rewards = {}
        if "eta1" in self.env_params.additional_params.keys():
            eta1 = self.env_params.additional_params["eta1"]
            eta2 = self.env_params.additional_params["eta2"]
        else:
            eta1 = 0.9
            eta2 = 0.1

        if "eta3" in self.env_params.additional_params.keys():
            eta3 = self.env_params.additional_params["eta3"]
        else:
            eta3 = 0

        reward1 = -0.1
        reward2 = average_velocity(self)/300
        reward = reward1 * eta1 + reward2 * eta2
        for rl_id in self.k.vehicle.get_rl_ids():
            rewards[rl_id] = reward

        #lane_change_human_ids = self.k.vehicle.get_lane_change_human_ids()
        #for rl_id in self.k.vehicle.get_rl_ids():
        #    veh_id = rl_id
        #    # compute the number of lane change vehicles as reward
        #    lane_id = self.k.vehicle.get_lane(rl_id)
        #    lead_ids = self.k.vehicle.get_lane_leaders(veh_id)
        #    lead_id = lead_ids[lane_id]
        #    additional_cutting_in = set()
        #    # print("check heads of rl_id ", rl_id)
        #    while lead_id in lane_change_human_ids:
        #        if lead_id not in self.right_before_rls[rl_id]:
        #            additional_cutting_in.add(lead_id)
        #            #self.right_before_rls[rl_id].add(lead_id)
        #        veh_id = lead_id
        #        lead_ids = self.k.vehicle.get_lane_leaders(veh_id)
        #        lead_id = lead_ids[lane_id]
        #    lane_change_reward = len(additional_cutting_in)
        #    self.right_before_rls[rl_id] |= additional_cutting_in
        #    # set_trace()
        #    # print("num of lane change", lane_change_reward)
        #    rewards[rl_id] = reward + eta3 * lane_change_reward 
        # print(rewards)
        return rewards

    
class LeftLaneHeadwayControlledMultiAgentEnv(MultiAgentHighwayPOEnv):
    def __init__(self, env_params, sim_params, network, simulator='traci'):
        super().__init__(env_params, sim_params, network, simulator)
        self.right_before_rls = defaultdict(lambda: set())
        # print("left lane headway controlled")

    @property
    def observation_space(self):
        #See class definition
        # basic 5 states + average speed of the vehicles on the right lane
        # leader and follower at the other lane
        # number of vehicles on the right lane that are about to move
        return Box(-float('inf'), float('inf'), shape=(6,), dtype=np.float32)

    @property
    def action_space(self):
        # the desired time headway of this agent
        return Box(
            low=0,
            high=50,
            shape=(1,),  # (4,),
            dtype=np.float32)

    def get_state(self):
        states = super().get_state()
        BEFORE_MERGE = 588
        LOOK_AHEAD = 120
        MAX_SPEED = 30
        # print("rl_ids", self.k.vehicle.get_rl_ids())
        for rl_id in states:
            veh_ahead_on_the_right = list()
            self_veh_x = self.k.vehicle.get_x_by_id(rl_id)
            for other_veh_id in self.k.vehicle.get_ids():
                lane_id = self.k.vehicle.get_lane(other_veh_id)
                other_veh_x = self.k.vehicle.get_x_by_id(other_veh_id)
                if lane_id == 0 and self_veh_x < other_veh_x and other_veh_x < BEFORE_MERGE and other_veh_x < self_veh_x + LOOK_AHEAD:  # 120
                    other_veh_vel = self.k.vehicle.get_speed(other_veh_id)
                    veh_ahead_on_the_right.append(other_veh_vel)
            if len(veh_ahead_on_the_right) == 0:
                mean_vel = MAX_SPEED
            else:
                mean_vel = mean(veh_ahead_on_the_right)
            states[rl_id] = np.array(list(states[rl_id]) + [mean_vel])
        # print("states", states)
        return states

    def compute_reward(self, rl_actions, **kwargs):
        # print("compute reward")
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
        reward = reward1 * eta1 + reward2 * eta2
        lane_change_human_ids = self.k.vehicle.get_lane_change_human_ids()
        for rl_id in self.k.vehicle.get_rl_ids():
            veh_id = rl_id
            # compute the number of lane change vehicles as reward
            lane_id = self.k.vehicle.get_lane(rl_id)
            lead_ids = self.k.vehicle.get_lane_leaders(veh_id)
            lead_id = lead_ids[lane_id]
            additional_cutting_in = set()
            # print("check heads of rl_id ", rl_id)
            while lead_id in lane_change_human_ids:
                if lead_id not in self.right_before_rls[rl_id]:
                    additional_cutting_in.add(lead_id)
                    #self.right_before_rls[rl_id].add(lead_id)
                veh_id = lead_id
                lead_ids = self.k.vehicle.get_lane_leaders(veh_id)
                lead_id = lead_ids[lane_id]
            lane_change_reward = len(additional_cutting_in)
            self.right_before_rls[rl_id] |= additional_cutting_in
            # set_trace()
            # print("num of lane change", lane_change_reward)
            rewards[rl_id] = reward + 0.03 * lane_change_reward 
        # print(rewards)
        return rewards

    def idm_headway_to_accel(self, 
        veh_id, 
        desired_time_headway, 
        v0=30, 
        a=1, 
        b=1.5, 
        delta=4,
        s0=2, 
        time_delay=0.0, 
        dt=0.1):

        # self.k.vehicle.update_leader_if_near_junction(veh_id, junc_dist_threshold=1000)#150)
        v = self.k.vehicle.get_speed(veh_id)

        lane_id=self.k.vehicle.get_lane(veh_id)
        # Fix the leader to be the leader on the same lane
        # set_trace()
        try:
            lead_ids = self.k.vehicle.get_lane_leaders(veh_id)
        except:
            print("rl_ids", self.k.vehicle.get_rl_ids()) 
            print("veh_id", veh_id) 
            print("lane_id", lane_id)
        lead_id = lead_ids[lane_id]

        #h = env.k.vehicle.get_headway(self.veh_id)
        # Fix the heaway to be the headway on the same lane accordingly
        headways = self.k.vehicle.get_lane_headways(veh_id)
        h = headways[lane_id]
        T = desired_time_headway

        # in order to deal with ZeroDivisionError
        if abs(h) < 1e-3:
            h = 1e-3

        if lead_id is None or lead_id == '':  # no car ahead
            s_star = 0
        else:
            lead_vel = self.k.vehicle.get_speed(lead_id)
            s_star = s0 + max(
                0, v * T + v * (v - lead_vel) /
                (2 * np.sqrt(a * b)))
        output_accel = a * (1 - (v / v0)**delta - (s_star / h)**2)
        return output_accel

    def _apply_rl_actions(self, rl_actions):
        """See class definition."""
        # in the warmup steps, rl_actions is None
        if rl_actions:
            for rl_id, actions in rl_actions.items():
                if rl_id not in self.k.vehicle.get_rl_ids():
                    continue
                desired_time_headway= actions[0]

                # lane_change_softmax = np.exp(actions[1:4])
                # lane_change_softmax /= np.sum(lane_change_softmax)
                # lane_change_action = np.random.choice([-1, 0, 1],
                #                                       p=lane_change_softmax)
                accel = self.idm_headway_to_accel(rl_id, desired_time_headway)
                self.k.vehicle.apply_acceleration(rl_id, accel)
                # self.k.vehicle.apply_lane_change(rl_id, lane_change_action)


class LeftLaneOvalHighwayPOEnvMerge4(MultiAgentHighwayPOEnv):
    @property
    def observation_space(self):
        #See class definition
        # basic 5 states
        # leader and follower at the other lane
        # number of vehicles on the right lane that are about to move
        return Box(-float('inf'), float('inf'), shape=(9,), dtype=np.float32)

    def _closest_vehicle(self, edge, lane, base_edge):
        if edge == base_edge:
            return float('inf'), 0
        if edge == '':
            return float('inf'), 0
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
                       for e, l in self.k.network.prev_edge(edge, lane))
        except ValueError:
            return float('inf'), 0

    def _merging_vehicle_forward_pass(self, edge, lane, base_edge, junctions):
        try:
            return min(self._merging_vehicle_forward_pass(e, l, base_edge, junctions) if e in junctions else self._merging_vehicle_backward_pass(e, l, base_edge, junctions)
                       for e, l in self.k.network.next_edge(edge, lane))
        except ValueError:
            return float('inf'), 0

    def get_state(self):
        states = super().get_state()

        for rl_id in states:
            edge_id = self.k.vehicle.get_edge(rl_id)
            lane = self.k.vehicle.get_lane(rl_id)

            lead_ids = self.k.vehicle.get_lane_leaders(rl_id)
            follow_ids = self.k.vehicle.get_lane_followers(rl_id)

            headways = self.k.vehicle.get_lane_headways(rl_id)
            tailways = self.k.vehicle.get_lane_tailways(rl_id)
            all_lane_ids = [i for i in range(0, len(headways))]

            other_lane_leader = None
            shortest_headway = float('inf')
            other_lane_leader_id = None

            other_lane_follower = None
            shortest_tailway = float('inf')
            other_lane_follower_id = None

            max_speed = 30.0
            max_length = 1000.0

            for other_lane in all_lane_ids:
                if lane == other_lane:
                    continue
                h = headways[other_lane]
                t = tailways[other_lane]

                if h < shortest_headway:
                    shortest_headway = h
                    other_lane_leader_id = lead_ids[other_lane]
                if t < shortest_tailway:
                    shortest_tailway = t
                    other_lane_follower_id = follow_ids[other_lane]

            other_lane_leader_head = 0
            other_lane_leader_speed = 0
            other_lane_follower_tail = 0
            other_lane_follower_speed = 0
            if other_lane_leader_id in ["", None]:
                other_lane_leader_head = max_length
                other_lane_leader_speed = max_speed
            else:
                other_lane_leader_speed = self.k.vehicle.get_speed(other_lane_leader_id)
                other_lane_leader_head = shortest_headway

            if other_lane_follower_id in ["", None]:
                other_lane_follower_tail = max_length
                other_lane_follower_speed = max_speed
            else:
                other_lane_follower_tail = shortest_tailway
                other_lane_follower_speed = self.k.vehicle.get_speed(other_lane_follower_id)

            states[rl_id] = np.array(list(states[rl_id]) + [other_lane_leader_speed/max_speed, other_lane_leader_head /
                                     max_length, other_lane_follower_speed/max_speed, other_lane_follower_tail/max_length])
        #print(states)
        return states


class LeftLaneOvalAboutToMergeHighwayPOEnvMerge4(LeftLaneOvalHighwayPOEnvMerge4):
    @property
    def observation_space(self):
        #See class definition
        # basic 5 states
        # leader and follower at the other lane
        # number of vehicles on the right lane that are about to move
        return Box(-float('inf'), float('inf'), shape=(10,), dtype=np.float32)

    def get_state(self):
        states = super().get_state()

        # obtain the number of vehicles that are about to change lane
        # the lateral location is specified with respect to the center line of the lane, negative goes below, postive goes above
        # it seems that all vehicles that are larger than 1 from the right are likely to merge

        max_length = 1000.0
        for rl_id in states:
            edge_id = self.k.vehicle.get_edge(rl_id)
            lane_id = self.k.vehicle.get_lane(rl_id)
            rl_x = self.k.vehicle.get_x_by_id(rl_id)
            # find the closest vehicle that is about to merge to this lane
            closest_x = float('inf')
            closest_merger = None
            for veh_id in self.k.vehicle.get_ids_by_edge(edge_id):
                veh_lane_id = self.k.vehicle.get_lane(veh_id)
                if lane_id <= veh_lane_id or veh_id == rl_id:  # on the left or is current vehicle
                    continue
                veh_x = self.k.vehicle.get_x_by_id(veh_id)
                if veh_x < rl_x:
                    continue
                lateral_pos = self.k.vehicle.get_lateral_lane_pos(veh_id)
                if lateral_pos >= 1.0:
                    # it is about to merge the left lane
                    if closest_x > veh_x:
                        closest_x = veh_x
                        closest_merger = veh_id
            closest_dist = closest_x-rl_x
            if closest_merger is None:
                closest_dist = 1
            else:
                closest_dist /= max_length
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
        reward = reward1 * eta1 + reward2 * eta2
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
        reward = reward1 * eta1 + reward2 * eta2
        for rl_id in self.k.vehicle.get_rl_ids():
            rewards[rl_id] = reward
        return rewards
