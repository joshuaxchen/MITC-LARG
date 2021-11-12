"""Contains a list of custom lane change controllers."""

from flow.controllers.base_lane_changing_controller import \
    BaseLaneChangeController

import random

PURPLE= (128,0,128)
YELLOW= (255,255,0) 
GREEN= (0,255,0) 

class SimLaneChangeController(BaseLaneChangeController):
    """A controller used to enforce sumo lane-change dynamics on a vehicle.

    Usage: See base class for usage example.
    """
    
    def get_lane_change_action(self, env):
        """See parent class."""
        #lane_change_probability=0.5
        #sampled_prob=random.random()
        #if sampled_prob<=lane_change_probability:
        #    lane_change_switch=True
        #else:
        #    lane_change_switch=False
        #if lane_change_switch:
        #    return None
        #else:
        #    return 0
        return None

class StochasticLaneChangeController(BaseLaneChangeController):
    """A lane-changing model used to keep a vehicle in the same lane.

    Usage: See base class for usage example.
    """
     
    def get_lane_change_action(self, env):
        """See parent class."""
        #print("lane changing in stochastic")
        if self.freeze_lane_change:
            return 0
        lane_change_probability=0.2
        sampled_prob=random.random()
        if sampled_prob<=lane_change_probability:
            lane_change_switch=True
        else:
            lane_change_switch=False
        if lane_change_switch:
            #print("lc", self.veh_id, "lateral lane pos", env.k.vehicle.get_lateral_lane_pos(self.veh_id))
            return None
        else:
            #print("no lc", self.veh_id, "lateral lane pos", env.k.vehicle.get_lateral_lane_pos(self.veh_id))
            #print(self.veh_id, "lc 0")
            return 0


class StaticLaneChanger(BaseLaneChangeController):
    """A lane-changing model used to keep a vehicle in the same lane.

    Usage: See base class for usage example.
    """

    def get_lane_change_action(self, env):
        """See parent class."""
        return 0

class SimpleMergeLaneChanger(BaseLaneChangeController):
    """A lane-changing model to control the amount of vehicles to do lane changing
    """

    """Specify the lane change action to be performed.

        If discrete lane changes are being performed, the action is a direction

        * -1: lane change right
        * 0: no lane change
        * 1: lane change left

        Parameters
        ----------
        env : flow.envs.Env
            state of the environment at the current time step

        Returns
        -------
        float or int
            requested lane change action
    """

    def __init__(self, veh_id, lane_change_params=None):
        super().__init__(veh_id, lane_change_params)
        if 'lane_change_region_start_loc' not in lane_change_params.keys():
            print('lane_change_region_start_loc is required in lane_change_params for SimpleMergeLaneChanger')
            exit(-1)
        if 'lane_change_region_end_loc' not in lane_change_params.keys():
            print('lane_change_region_end_loc is required in lane_change_params for SimpleMergeLaneChanger')
            exit(-1)
        if 'lane_change_probability' not in lane_change_params.keys():
            print('lane_change_probability is required in lane_change_params for SimpleMergeLaneChanger')

        self.lane_change_region_start_loc=lane_change_params['lane_change_region_start_loc']
        self.lane_change_region_end_loc=lane_change_params['lane_change_region_end_loc']
        self.lane_change_probability=lane_change_params['lane_change_probability']
        # TODO: log the seed used for experiment replay
        sampled_prob=random.random()
        if sampled_prob<=self.lane_change_probability:
            self.lane_change_switch=True
        else:
            self.lane_change_switch=False

        self.prev_lane=None
        self.changed_t=None


    def get_lane_change_action(self, env):
        lane_id=env.k.vehicle.get_lane(self.veh_id)
        r, g, b, t=env.k.vehicle.get_color_t(self.veh_id)
        if self.prev_lane is not None and self.prev_lane !=lane_id:
            env.k.vehicle.set_color(self.veh_id, YELLOW)
            self.changed_t=1
        elif self.changed_t is not None: # has changed lane
            if self.changed_t<=25:
                b=self.changed_t*10
                if b>255:
                    b=255
                env.k.vehicle.set_color(self.veh_id, (b,255,b))
                self.changed_t+=1
            else:
                self.changed_t=None
                WHITE = (255, 255, 255)
                env.k.vehicle.set_color(self.veh_id, WHITE)

        self.prev_lane=lane_id

            #env.k.vehicle.set_color(self.veh_id, PURPLE)
        if lane_id==1: # do nothing for left lane
            self.lane_change_switch=False
        loc=env.k.vehicle.get_x_by_id(self.veh_id)
        if self.lane_change_switch and loc>=self.lane_change_region_start_loc and loc<=self.lane_change_region_end_loc:
            return 1
        else:
            return 0
    
