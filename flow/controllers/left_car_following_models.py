"""
Contains several custom car-following control models.

These controllers can be used to modify the acceleration behavior of vehicles
in Flow to match various prominent car-following models that can be calibrated.

Each controller includes the function ``get_accel(self, env) -> acc`` which,
using the current state of the world and existing parameters, uses the control
model to return a vehicle acceleration.
"""
import math
import numpy as np

from flow.controllers.base_controller import BaseController

class LeftIDMController(BaseController):
    """Intelligent Driver Model (IDM) controller.

    For more information on this controller, see:
    Treiber, Martin, Ansgar Hennecke, and Dirk Helbing. "Congested traffic
    states in empirical observations and microscopic simulations." Physical
    review E 62.2 (2000): 1805.

    Usage
    -----
    See BaseController for usage example.

    Attributes
    ----------
    veh_id : str
        Vehicle ID for SUMO identification
    car_following_params : flow.core.param.SumoCarFollowingParams
        see parent class
    v0 : float
        desirable velocity, in m/s (default: 30)
    T : float
        safe time headway, in s (default: 1)
    a : float
        max acceleration, in m/s2 (default: 1)
    b : float
        comfortable deceleration, in m/s2 (default: 1.5)
    delta : float
        acceleration exponent (default: 4)
    s0 : float
        linear jam distance, in m (default: 2)
    dt : float
        timestep, in s (default: 0.1)
    noise : float
        std dev of normal perturbation to the acceleration (default: 0)
    fail_safe : str
        type of flow-imposed failsafe the vehicle should posses, defaults
        to no failsafe (None)
    """

    def __init__(self,
                 veh_id,
                 v0=30,
                 T=1,
                 a=1,
                 b=1.5,
                 delta=4,
                 s0=2,
                 time_delay=0.0,
                 dt=0.1,
                 noise=0,
                 congest_spd_threshold=16,
                 self_spd_threshold=15,
                 dist_to_junction_threshold=500,
                 slow_down_headway=100,
                 fail_safe=None,
                 car_following_params=None):
        """Instantiate an IDM controller."""
        BaseController.__init__(
            self,
            veh_id,
            car_following_params,
            delay=time_delay,
            fail_safe=fail_safe,
            noise=noise)
        self.v0 = v0
        self.T = T
        self.a = a
        self.b = b
        self.delta = delta
        self.s0 = s0
        self.dt = dt
        self.congest_spd_threshold=congest_spd_threshold
        self.self_spd_threshold=self_spd_threshold
        self.dist_to_junction_threshold=dist_to_junction_threshold
        self.slow_down_headway=slow_down_headway

    def get_accel(self, env):
        """See parent class."""
        # solve leader issues near junctions using get_lane_leaders()
        # add from Daniel
        env.k.vehicle.update_leader_if_near_junction(self.veh_id, junc_dist_threshold=1000)#150)


        v = env.k.vehicle.get_speed(self.veh_id)

        lane_id=env.k.vehicle.get_lane(self.veh_id)
        #lead_id = env.k.vehicle.get_leader(self.veh_id)
        # Fix the leader to be the leader on the same lane
        lead_ids = env.k.vehicle.get_lane_leaders(self.veh_id)
        lead_id=lead_ids[lane_id]

        #h = env.k.vehicle.get_headway(self.veh_id)
        # Fix the heaway to be the headway on the same lane accordingly
        headways=env.k.vehicle.get_lane_headways(self.veh_id)
        h=headways[lane_id] 

        # in order to deal with ZeroDivisionError
        if abs(h) < 1e-3:
            h = 1e-3
        
        right_lane=0
        left_lane=1
        center_x = env.k.network.total_edgestarts_dict["center"]
        # Get how congested is the right lane
        right_lane_vehs=[]
        for other_id in env.k.vehicle.get_ids():
            if env.k.vehicle.get_lane(other_id)==right_lane\
                    and env.k.vehicle.get_edge(other_id) in ["left"]:
                        other_x = env.k.vehicle.get_x_by_id(other_id)
                        other_dist = center_x - other_x
                        if other_dist <150:
                            right_lane_vehs.append(env.k.vehicle.get_speed(other_id))
        if len(right_lane_vehs)>0:
            congest_spd=np.mean(right_lane_vehs)
        else:
            congest_spd=30
        # Get self speed
        self_spd=v
        # Get distance to the junction
        veh_x = env.k.vehicle.get_x_by_id(self.veh_id)
        edge = env.k.vehicle.get_edge(self.veh_id)
        dist_to_junction=center_x-veh_x
        if congest_spd<self.congest_spd_threshold \
            and self_spd>=self.self_spd_threshold \
            and dist_to_junction<=self.dist_to_junction_threshold \
            and dist_to_junction>=250 \
            and lead_id not in env.k.vehicle.get_lane_change_human_ids():
            # detect congestion
            # modify s_star
            print(congest_spd)
            if lead_id is None or lead_id == '':  # no car ahead
                s_star = 0
            else:
                lead_vel = env.k.vehicle.get_speed(lead_id)
                s_star = self.s0 + max(
                    0, self.slow_down_headway + v * (v - lead_vel) /
                    (2 * np.sqrt(self.a * self.b)))

        else:
            if lead_id is None or lead_id == '':  # no car ahead
                s_star = 0
            else:
                lead_vel = env.k.vehicle.get_speed(lead_id)
                s_star = self.s0 + max(
                    0, v * self.T + v * (v - lead_vel) /
                    (2 * np.sqrt(self.a * self.b)))
        output_accel=self.a * (1 - (v / self.v0)**self.delta - (s_star / h)**2)
        current_loc=env.k.vehicle.get_x_by_id(self.veh_id)
        current_edge=env.k.vehicle.get_edge(self.veh_id)

        return output_accel 


class SimCarFollowingController(BaseController):
    """Controller whose actions are purely defined by the simulator.

    Note that methods for implementing noise and failsafes through
    BaseController, are not available here. However, similar methods are
    available through sumo when initializing the parameters of the vehicle.

    Usage: See BaseController for usage example.
    """

    def get_accel(self, env):
        """See parent class."""
        return None
