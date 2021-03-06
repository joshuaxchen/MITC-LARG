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

class MultiAgentHighwayPOEnvMerge4AdaptiveHeadway(MultiAgentHighwayPOEnvMerge4Collaborate):
    @property
    def action_space(self):
        """See class definition."""
        return Box(
            low=0,#-np.abs(self.env_params.additional_params['max_decel']),
            high=1,#self.env_params.additional_params['max_accel'],
            shape=(1,),  # (4,),
            dtype=np.float32)

    def idm_acceleration(self, veh_id, rl_action):
            #print(veh_id, "chooses to be a leader with probability:",rl_action)
            if rl_action is None:
                return None
            a=1 # max acceleration, in m/s2 (default: 1)
            delta=4 # acceleration exponent (default: 4)
            s0=2 # linear jam distance, in m (default: 2)
            MAX_T=self.env_params.additional_params['max_headway']
            b=1.5 # comfortable deceleration, in m/s2 (default: 1.5)
            v0=30 # desirable velocity, in m/s (default: 30)
            T=MAX_T*rl_action # safe time headway, in s (default: 1)
            if T<=1:
                T=1
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

        clipped_actions = self.clip_actions(rl_actions)
        if rl_actions!=clipped_actions:
            print("********network gives an action out of bound********************")
            import sys
            sys.exit(-1)
            #print("action bound:[",self.action_space.low[0], ",", self.action_space.high[0],"]")
            #print("actions from the network:",rl_actions)
            #print("actions after clipped:",clipped_actions)
            #print("within bound:[",self.action_space.low[0], ",", self.action_space.high[0],"]")
        rl_acceleration={}
        for rl_id, actions in clipped_actions.items():
            chosen_act=actions[0]
            #print(rl_id, "chooses to be a leader with probability:", chosen_act)
            accel=self.idm_acceleration(rl_id, chosen_act)
            rl_acceleration[rl_id]=np.array([accel])  
        #print("before clip:", rl_acceleration)
        clipped_acceleration=self.clip_acceleration(rl_acceleration)
        #print("after clip:", clipped_acceleration)
        self._apply_rl_actions(clipped_acceleration)
    
    def compute_reward(self, rl_actions, **kwargs):
        """See class definition."""
        if rl_actions is None:
            return {}
        rewards=super().compute_reward(rl_actions, **kwargs)
        #print("rewards:",rewards)
        #print("actions:",rl_actions)
        for rl_id in self.k.vehicle.get_rl_ids():
            if self.env_params.evaluate:
                # reward is speed of vehicle if we are in evaluation mode
                reward = self.k.vehicle.get_speed(rl_id)
            elif kwargs['fail']:
                # reward is 0 if a collision occurred
                reward = 0
            else:
                # reward from parent class
                if rl_id in rl_actions.keys():
                    act=rl_actions[rl_id][0]
                    #print("action is:",act)
                    reward=rewards[rl_id]
                    # compute penality for action
                    if act>=self.action_space.low and act<=self.action_space.high:
                        penality=0
                    elif act<self.action_space.low:
                        penality=self.action_space.low-act
                    else:
                        penality=act-self.action_space.high
                    #print("reward=", reward, "penality=", penality)
                    rewards[rl_id] = reward-penality
        return rewards


class MultiAgentHighwayPOEnvMerge4AdaptiveHeadwayCountAhead(MultiAgentHighwayPOEnvMerge4AdaptiveHeadway):
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

