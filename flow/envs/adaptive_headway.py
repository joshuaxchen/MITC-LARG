"""Environment used to train vehicles to improve traffic on a highway."""
import numpy as np
from gym.spaces.box import Box
from gym.spaces import Discrete, MultiBinary 
from flow.core.rewards import desired_velocity, average_velocity
from flow.envs import MergePOEnvArrive
import collections
import os
from copy import deepcopy
from flow.envs import MergePOEnv 

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

class MergePOEnvAdaptiveHeadway(MergePOEnvArrive):
    @property
    def action_space(self):
        """Identify the dimensions and bounds of the action space.

        MUST BE implemented in new environments.

        Returns
        -------
        gym Box or Tuple type
            a bounded box depicting the shape and bounds of the action space
        """

        """See class definition."""
        #import pdb; pdb.set_trace()
        #return Discrete(100)
        return Box(low=-float('inf'), high=float('inf'), shape=(self.num_rl,), dtype=np.float32)
        #return MultiBinary(self.num_rl)
        #return Box(low=np.array([0.0]), high=np.array([1.0]), shape=(1,), dtype=np.float32)
        #return Box(low=np.float32(np.array([0.0])), high=np.float32(np.array([1.0])), shape=(1,), dtype=np.float32)

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

    def apply_rl_actions(self, rl_follower_or_leaders):
        """Specify the actions to be performed by the rl agent(s).

        If no actions are provided at any given step, the rl agents default to
        performing actions specified by SUMO.

        Parameters
        ----------
        rl_actions : array_like
            list of actions provided by the RL algorithm
        """
        #print(rl_follower_or_leaders)
        # ignore if no actions are issued
        if rl_follower_or_leaders is None:
            return
        # maintain the a headway discounted by action 
        rl_actions=[]
        for i, rl_id in enumerate(self.rl_veh):
            # ignore rl vehicles outside the network
            if rl_id not in self.k.vehicle.get_rl_ids():
                rl_follower_or_leaders[i]=0
                continue
            chosen_act=rl_follower_or_leaders[i]
            if chosen_act<0:
                chosen_act=0
            accel=self.idm_acceleration(rl_id, chosen_act)
            rl_follower_or_leaders[i]=accel
        rl_clipped = self.clip_actions(rl_follower_or_leaders)
        self._apply_rl_actions(rl_clipped)

    def compute_reward(self, rl_actions, **kwargs):
        """See class definition."""
        if self.env_params.evaluate:
            return np.mean(self.k.vehicle.get_speed(self.k.vehicle.get_ids()))
        if kwargs['fail']:
            # reward is 0 if a collision occurred
            reward = 0
        if rl_actions is None:
            return {}
        reward=super().compute_reward(rl_actions, **kwargs)
        #print("rewards:",rewards)
        #print("actions:",rl_actions)

        for i, rl_id in enumerate(self.rl_veh):
            act=rl_actions[i]
            penality=((2*(act-0.5))**6-1)*0.01 
            #print("act=",act,"reward=",reward,"penality=",penality)
            reward = reward-penality
        return reward


