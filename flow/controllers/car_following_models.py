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
from statistics import mean
from flow.controllers.base_controller import BaseController


class CFMController(BaseController):
    """CFM controller.

    Usage
    -----
    See BaseController for usage example.

    Attributes
    ----------
    veh_id : str
        Vehicle ID for SUMO identification
    car_following_params : SumoCarFollowingParams
        see parent class
    k_d : float
        headway gain (default: 1)
    k_v : float
        gain on difference between lead velocity and current (default: 1)
    k_c : float
        gain on difference from desired velocity to current (default: 1)
    d_des : float
        desired headway (default: 1)
    v_des : float
        desired velocity (default: 8)
    time_delay : float, optional
        time delay (default: 0.0)
    noise : float
        std dev of normal perturbation to the acceleration (default: 0)
    fail_safe : str
        type of flow-imposed failsafe the vehicle should posses, defaults
        to no failsafe (None)
    """

    def __init__(self,
                 veh_id,
                 car_following_params,
                 k_d=1,
                 k_v=1,
                 k_c=1,
                 d_des=1,
                 v_des=8,
                 time_delay=0.0,
                 noise=0,
                 fail_safe=None):
        """Instantiate a CFM controller."""
        BaseController.__init__(
            self,
            veh_id,
            car_following_params,
            delay=time_delay,
            fail_safe=fail_safe,
            noise=noise)

        self.veh_id = veh_id
        self.k_d = k_d
        self.k_v = k_v
        self.k_c = k_c
        self.d_des = d_des
        self.v_des = v_des

    def get_accel(self, env):
        """See parent class."""
        lead_id = env.k.vehicle.get_leader(self.veh_id)
        if not lead_id:  # no car ahead
            return self.max_accel

        lead_vel = env.k.vehicle.get_speed(lead_id)
        this_vel = env.k.vehicle.get_speed(self.veh_id)

        d_l = env.k.vehicle.get_headway(self.veh_id)

        return self.k_d*(d_l - self.d_des) + self.k_v*(lead_vel - this_vel) + \
            self.k_c*(self.v_des - this_vel)


class BCMController(BaseController):
    """Bilateral car-following model controller.

    This model looks ahead and behind when computing its acceleration.

    Usage
    -----
    See BaseController for usage example.

    Attributes
    ----------
    veh_id : str
        Vehicle ID for SUMO identification
    car_following_params : flow.core.params.SumoCarFollowingParams
        see parent class
    k_d : float
        gain on distances to lead/following cars (default: 1)
    k_v : float
        gain on vehicle velocity differences (default: 1)
    k_c : float
        gain on difference from desired velocity to current (default: 1)
    d_des : float
        desired headway (default: 1)
    v_des : float
        desired velocity (default: 8)
    time_delay : float
        time delay (default: 0.5)
    noise : float
        std dev of normal perturbation to the acceleration (default: 0)
    fail_safe : str
        type of flow-imposed failsafe the vehicle should posses, defaults
        to no failsafe (None)
    """

    def __init__(self,
                 veh_id,
                 car_following_params,
                 k_d=1,
                 k_v=1,
                 k_c=1,
                 d_des=1,
                 v_des=8,
                 time_delay=0.0,
                 noise=0,
                 fail_safe=None):
        """Instantiate a Bilateral car-following model controller."""
        BaseController.__init__(
            self,
            veh_id,
            car_following_params,
            delay=time_delay,
            fail_safe=fail_safe,
            noise=noise)

        self.veh_id = veh_id
        self.k_d = k_d
        self.k_v = k_v
        self.k_c = k_c
        self.d_des = d_des
        self.v_des = v_des

    def get_accel(self, env):
        """See parent class.

        From the paper:
        There would also be additional control rules that take
        into account minimum safe separation, relative speeds,
        speed limits, weather and lighting conditions, traffic density
        and traffic advisories
        """
        lead_id = env.k.vehicle.get_leader(self.veh_id)
        if not lead_id:  # no car ahead
            return self.max_accel

        lead_vel = env.k.vehicle.get_speed(lead_id)
        this_vel = env.k.vehicle.get_speed(self.veh_id)

        trail_id = env.k.vehicle.get_follower(self.veh_id)
        trail_vel = env.k.vehicle.get_speed(trail_id)

        headway = env.k.vehicle.get_headway(self.veh_id)
        footway = env.k.vehicle.get_headway(trail_id)

        return self.k_d * (headway - footway) + \
            self.k_v * ((lead_vel - this_vel) - (this_vel - trail_vel)) + \
            self.k_c * (self.v_des - this_vel)


class LACController(BaseController):
    """Linear Adaptive Cruise Control.

    Attributes
    ----------
    veh_id : str
        Vehicle ID for SUMO identification
    car_following_params : flow.core.params.SumoCarFollowingParams
        see parent class
    k_1 : float
        design parameter (default: 0.8)
    k_2 : float
        design parameter (default: 0.9)
    h : float
        desired time gap  (default: 1.0)
    tau : float
        lag time between control input u and real acceleration a (default:0.1)
    time_delay : float
        time delay (default: 0.5)
    noise : float
        std dev of normal perturbation to the acceleration (default: 0)
    fail_safe : str
        type of flow-imposed failsafe the vehicle should posses, defaults
        to no failsafe (None)
    """

    def __init__(self,
                 veh_id,
                 car_following_params,
                 k_1=0.3,
                 k_2=0.4,
                 h=1,
                 tau=0.1,
                 a=0,
                 time_delay=0.0,
                 noise=0,
                 fail_safe=None):
        """Instantiate a Linear Adaptive Cruise controller."""
        BaseController.__init__(
            self,
            veh_id,
            car_following_params,
            delay=time_delay,
            fail_safe=fail_safe,
            noise=noise)

        self.veh_id = veh_id
        self.k_1 = k_1
        self.k_2 = k_2
        self.h = h
        self.tau = tau
        self.a = a

    def get_accel(self, env):
        """See parent class."""
        lead_id = env.k.vehicle.get_leader(self.veh_id)
        lead_vel = env.k.vehicle.get_speed(lead_id)
        this_vel = env.k.vehicle.get_speed(self.veh_id)
        headway = env.k.vehicle.get_headway(self.veh_id)
        L = env.k.vehicle.get_length(self.veh_id)
        ex = headway - L - self.h * this_vel
        ev = lead_vel - this_vel
        u = self.k_1*ex + self.k_2*ev
        a_dot = -(self.a/self.tau) + (u/self.tau)
        self.a = a_dot*env.sim_step + self.a

        return self.a


class OVMController(BaseController):
    """Optimal Vehicle Model controller.

    Usage
    -----
    See BaseController for usage example.

    Attributes
    ----------
    veh_id : str
        Vehicle ID for SUMO identification
    car_following_params : flow.core.params.SumoCarFollowingParams
        see parent class
    alpha : float
        gain on desired velocity to current velocity difference
        (default: 0.6)
    beta : float
        gain on lead car velocity and self velocity difference
        (default: 0.9)
    h_st : float
        headway for stopping (default: 5)
    h_go : float
        headway for full speed (default: 35)
    v_max : float
        max velocity (default: 30)
    time_delay : float
        time delay (default: 0.5)
    noise : float
        std dev of normal perturbation to the acceleration (default: 0)
    fail_safe : str
        type of flow-imposed failsafe the vehicle should posses, defaults
        to no failsafe (None)
    """

    def __init__(self,
                 veh_id,
                 car_following_params,
                 alpha=1,
                 beta=1,
                 h_st=2,
                 h_go=15,
                 v_max=30,
                 time_delay=0,
                 noise=0,
                 fail_safe=None):
        """Instantiate an Optimal Vehicle Model controller."""
        BaseController.__init__(
            self,
            veh_id,
            car_following_params,
            delay=time_delay,
            fail_safe=fail_safe,
            noise=noise)
        self.veh_id = veh_id
        self.v_max = v_max
        self.alpha = alpha
        self.beta = beta
        self.h_st = h_st
        self.h_go = h_go

    def get_accel(self, env):
        """See parent class."""
        lead_id = env.k.vehicle.get_leader(self.veh_id)
        if not lead_id:  # no car ahead
            return self.max_accel

        lead_vel = env.k.vehicle.get_speed(lead_id)
        this_vel = env.k.vehicle.get_speed(self.veh_id)
        h = env.k.vehicle.get_headway(self.veh_id)
        h_dot = lead_vel - this_vel

        # V function here - input: h, output : Vh
        if h <= self.h_st:
            v_h = 0
        elif self.h_st < h < self.h_go:
            v_h = self.v_max / 2 * (1 - math.cos(math.pi * (h - self.h_st) /
                                                 (self.h_go - self.h_st)))
        else:
            v_h = self.v_max

        return self.alpha * (v_h - this_vel) + self.beta * h_dot


class LinearOVM(BaseController):
    """Linear OVM controller.

    Usage
    -----
    See BaseController for usage example.

    Attributes
    ----------
    veh_id : str
        Vehicle ID for SUMO identification
    car_following_params : flow.core.params.SumoCarFollowingParams
        see parent class
    v_max : float
        max velocity (default: 30)
    adaptation : float
        adaptation constant (default: 0.65)
    h_st : float
        headway for stopping (default: 5)
    time_delay : float
        time delay (default: 0.5)
    noise : float
        std dev of normal perturbation to the acceleration (default: 0)
    fail_safe : str
        type of flow-imposed failsafe the vehicle should posses, defaults
        to no failsafe (None)
    """

    def __init__(self,
                 veh_id,
                 car_following_params,
                 v_max=30,
                 adaptation=0.65,
                 h_st=5,
                 time_delay=0.0,
                 noise=0,
                 fail_safe=None):
        """Instantiate a Linear OVM controller."""
        BaseController.__init__(
            self,
            veh_id,
            car_following_params,
            delay=time_delay,
            fail_safe=fail_safe,
            noise=noise)
        self.veh_id = veh_id
        # 4.8*1.85 for case I, 3.8*1.85 for case II, per Nakayama
        self.v_max = v_max
        # TAU in Traffic Flow Dynamics textbook
        self.adaptation = adaptation
        self.h_st = h_st

    def get_accel(self, env):
        """See parent class."""
        this_vel = env.k.vehicle.get_speed(self.veh_id)
        h = env.k.vehicle.get_headway(self.veh_id)

        # V function here - input: h, output : Vh
        alpha = 1.689  # the average value from Nakayama paper
        if h < self.h_st:
            v_h = 0
        elif self.h_st <= h <= self.h_st + self.v_max / alpha:
            v_h = alpha * (h - self.h_st)
        else:
            v_h = self.v_max

        return (v_h - this_vel) / self.adaptation


class IDMController(BaseController):
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
        #self.prev_loc=0
        #self.prev_edge=None
        #self.loc_time_to_skip=200
        #self.edge_time_to_skip=200
        #self.track=False

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

        # 124433730#2-AddedOnRampEdge
        #if self.track:
        #    print("Track: veh_id", self.veh_id, "at", current_edge, "with intended accel", output_accel, "current speed", env.k.vehicle.get_speed(self.veh_id), "current loc", env.k.vehicle.get_x_by_id(self.veh_id))
        #if current_edge =="124433730#2-AddedOnRampEdge":
        #    print("veh_id", self.veh_id, "stucks at", current_edge, "with intended accel", output_accel, "current speed", env.k.vehicle.get_speed(self.veh_id), "current loc", env.k.vehicle.get_x_by_id(self.veh_id))
        #    if env.k.vehicle.get_speed(self.veh_id)==0:
        #        self.track=True

        #if self.prev_loc==current_loc and self.loc_time_to_skip==0:
        #    print("veh_id", self.veh_id, "stops", "with intended accel", output_accel)
        #    self.loc_time_to_skip=200
        #if self.prev_edge==current_edge and self.edge_time_to_skip==0:
        #    print("veh_id", self.veh_id, "stucks at", current_edge, "with intended accel", output_accel)
        #    self.edge_time_to_skip=200

        #self.prev_loc=current_loc
        #self.prev_edge=current_edge
        #self.loc_time_to_skip=0
        #self.edge_time_to_skip=0
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


class GippsController(BaseController):
    """Gipps' Model controller.

    For more information on this controller, see:
    Traffic Flow Dynamics written by M.Treiber and A.Kesting
    By courtesy of Springer publisher, http://www.springer.com

    http://www.traffic-flow-dynamics.org/res/SampleChapter11.pdf

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
    acc : float
        max acceleration, in m/s2 (default: 1.5)
    b : float
        comfortable deceleration, in m/s2 (default: -1)
    b_l : float
        comfortable deceleration for leading vehicle , in m/s2 (default: -1)
    s0 : float
        linear jam distance for saftey, in m (default: 2)
    tau : float
        reaction time in s (default: 1)
    noise : float
        std dev of normal perturbation to the acceleration (default: 0)
    fail_safe : str
        type of flow-imposed failsafe the vehicle should posses, defaults
        to no failsafe (None)
    """

    def __init__(self,
                 veh_id,
                 car_following_params=None,
                 v0=30,
                 acc=1.5,
                 b=-1,
                 b_l=-1,
                 s0=2,
                 tau=1,
                 delay=0,
                 noise=0,
                 fail_safe=None):
        """Instantiate a Gipps' controller."""
        BaseController.__init__(
            self,
            veh_id,
            car_following_params,
            delay=delay,
            fail_safe=fail_safe,
            noise=noise
            )

        self.v_desired = v0
        self.acc = acc
        self.b = b
        self.b_l = b_l
        self.s0 = s0
        self.tau = tau

    def get_accel(self, env):
        """See parent class."""
        v = env.k.vehicle.get_speed(self.veh_id)
        h = env.k.vehicle.get_headway(self.veh_id)
        v_l = env.k.vehicle.get_speed(
            env.k.vehicle.get_leader(self.veh_id))

        # get velocity dynamics
        v_acc = v + (2.5 * self.acc * self.tau * (
                1 - (v / self.v_desired)) * np.sqrt(0.025 + (v / self.v_desired)))
        v_safe = (self.tau * self.b) + np.sqrt(((self.tau**2) * (self.b**2)) - (
                self.b * ((2 * (h-self.s0)) - (self.tau * v) - ((v_l**2) / self.b_l))))

        v_next = min(v_acc, v_safe, self.v_desired)

        return (v_next-v)/env.sim_step

class IDMRLController(BaseController):
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
        self.prev_headway=0
        self.prev_T_decide=0
        self.freeze=0
        self.headway_to_create=20
        #self.prev_loc=0
        #self.prev_edge=None 
        #self.loc_time_to_skip=200 
        #self.edge_time_to_skip=200 
        #self.track=False 

    def check_congestion_at_right(self, env): 
        self_veh_x=env.k.vehicle.get_x_by_id(self.veh_id)
        self_veh_vel=env.k.vehicle.get_speed(self.veh_id)
        vel_list=list()
        if self_veh_x>588:
            return False
        buffer_zone=self_veh_vel*0.1
        look_ahead=self_veh_vel*self.headway_to_create
        for other_veh_id in env.k.vehicle.get_ids():
            lane_id=env.k.vehicle.get_lane(other_veh_id)
            other_veh_x=env.k.vehicle.get_x_by_id(other_veh_id)
            #headways=self.k.vehicle.get_lane_headways(veh_id)
            #h=headways[lane_id] 
            if lane_id==0 and self_veh_x< other_veh_x and other_veh_x<588 and other_veh_x <self_veh_x+120: #120
            #if lane_id==0 and self_veh_x< other_veh_x+buffer_zone and other_veh_x<588 and other_veh_x <self_veh_x+look_ahead+buffer_zone:
                other_veh_vel=env.k.vehicle.get_speed(other_veh_id)
                vel_list.append(other_veh_vel) 
        if len(vel_list)==0:
            return False 
        mean_vel=mean(vel_list)
        #if mean_vel<17 and mean_vel>7:
        #if self_veh_vel-mean_vel>0 and self_veh_vel-mean_vel<6: # There is enough speed gain for the vehicle on the right
        #if (self_veh_vel-mean_vel>0 and self_veh_vel-mean_vel<6) or (self_veh_vel/mean_vel>1 and self_veh_vel/mean_vel<1.3): # There is enough speed gain for the vehicle on the right
        #if self_veh_vel/mean_vel>1 and self_veh_vel-mean_vel<2*math.floor(mean_vel/10)+6: # There is enough speed gain for the vehicle on the right
        if (self_veh_vel-mean_vel)>0 and self_veh_vel-mean_vel<8: # There is enough speed gain for the vehicle on the right
       # if abs(self_veh_vel-mean_vel)<8: #and self_veh_vel-mean_vel<8: # There is enough speed gain for the vehicle on the right
            return True
        else:
            return False

    def get_accel(self, env):
        """See parent class."""
        # solve leader issues near junctions using get_lane_leaders()
        # add from Daniel
        env.k.vehicle.update_leader_if_near_junction(self.veh_id, junc_dist_threshold=1000)#150)

        lane_id=env.k.vehicle.get_lane(self.veh_id)
        headways=env.k.vehicle.get_lane_headways(self.veh_id)
        h=headways[lane_id] 
        v = env.k.vehicle.get_speed(self.veh_id)

        #lead_id = env.k.vehicle.get_leader(self.veh_id)
        # Fix the leader to be the leader on the same lane
        lead_ids = env.k.vehicle.get_lane_leaders(self.veh_id)
        lead_id=lead_ids[lane_id]

        # modify T according to the location
        veh_x=env.k.vehicle.get_position(self.veh_id) 
        is_congested=self.check_congestion_at_right(env)
        headway_decrease_sharply=False
        #if self.prev_headway-h>4: 
        #    headway_decrease_sharply=True
        #    self.prev_headway=h
        if lead_id in env.k.vehicle.get_lane_change_human_ids():
            self.freeze=100
        self.freeze-=1
        #if self.freeze<=0 and is_congested and veh_x>200 and veh_x<=522: This achieves a little bit better than human baseline 2934 vs 2912
        #if self.freeze<=0 and is_congested and veh_x>200 and veh_x<=522:
        #    print("veh_id", self.veh_id, "T", self.T)
        #    self.T= (1-(veh_x-100)/322)*10
        #else:
        #    self.T=1
        if self.freeze<=0 and is_congested and veh_x>50 and veh_x<=300 and lead_id not in env.k.vehicle.get_rl_ids():
            #print("veh_id", self.veh_id, "T", self.T)
            #self.T=12#5.5 #(1-(veh_x-100)/322)*10
            self.T=self.headway_to_create#5.5 #(1-(veh_x-100)/322)*10
        else:
            self.T=1



        #h = env.k.vehicle.get_headway(self.veh_id)
        # Fix the heaway to be the headway on the same lane accordingly
        
        # in order to deal with ZeroDivisionError
        if abs(h) < 1e-3:
            h = 1e-3

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

        # 124433730#2-AddedOnRampEdge
        #if self.track:
        #    print("Track: veh_id", self.veh_id, "at", current_edge, "with intended accel", output_accel, "current speed", env.k.vehicle.get_speed(self.veh_id), "current loc", env.k.vehicle.get_x_by_id(self.veh_id))
        #if current_edge =="124433730#2-AddedOnRampEdge":
        #    print("veh_id", self.veh_id, "stucks at", current_edge, "with intended accel", output_accel, "current speed", env.k.vehicle.get_speed(self.veh_id), "current loc", env.k.vehicle.get_x_by_id(self.veh_id))
        #    if env.k.vehicle.get_speed(self.veh_id)==0:
        #        self.track=True

        #if self.prev_loc==current_loc and self.loc_time_to_skip==0:
        #    print("veh_id", self.veh_id, "stops", "with intended accel", output_accel)
        #    self.loc_time_to_skip=200
        #if self.prev_edge==current_edge and self.edge_time_to_skip==0:
        #    print("veh_id", self.veh_id, "stucks at", current_edge, "with intended accel", output_accel)
        #    self.edge_time_to_skip=200

        #self.prev_loc=current_loc
        #self.prev_edge=current_edge
        #self.loc_time_to_skip=0
        #self.edge_time_to_skip=0
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


class GippsController(BaseController):
    """Gipps' Model controller.

    For more information on this controller, see:
    Traffic Flow Dynamics written by M.Treiber and A.Kesting
    By courtesy of Springer publisher, http://www.springer.com

    http://www.traffic-flow-dynamics.org/res/SampleChapter11.pdf

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
    acc : float
        max acceleration, in m/s2 (default: 1.5)
    b : float
        comfortable deceleration, in m/s2 (default: -1)
    b_l : float
        comfortable deceleration for leading vehicle , in m/s2 (default: -1)
    s0 : float
        linear jam distance for saftey, in m (default: 2)
    tau : float
        reaction time in s (default: 1)
    noise : float
        std dev of normal perturbation to the acceleration (default: 0)
    fail_safe : str
        type of flow-imposed failsafe the vehicle should posses, defaults
        to no failsafe (None)
    """

    def __init__(self,
                 veh_id,
                 car_following_params=None,
                 v0=30,
                 acc=1.5,
                 b=-1,
                 b_l=-1,
                 s0=2,
                 tau=1,
                 delay=0,
                 noise=0,
                 fail_safe=None):
        """Instantiate a Gipps' controller."""
        BaseController.__init__(
            self,
            veh_id,
            car_following_params,
            delay=delay,
            fail_safe=fail_safe,
            noise=noise
            )

        self.v_desired = v0
        self.acc = acc
        self.b = b
        self.b_l = b_l
        self.s0 = s0
        self.tau = tau

    def get_accel(self, env):
        """See parent class."""
        v = env.k.vehicle.get_speed(self.veh_id)
        h = env.k.vehicle.get_headway(self.veh_id)
        v_l = env.k.vehicle.get_speed(
            env.k.vehicle.get_leader(self.veh_id))

        # get velocity dynamics
        v_acc = v + (2.5 * self.acc * self.tau * (
                1 - (v / self.v_desired)) * np.sqrt(0.025 + (v / self.v_desired)))
        v_safe = (self.tau * self.b) + np.sqrt(((self.tau**2) * (self.b**2)) - (
                self.b * ((2 * (h-self.s0)) - (self.tau * v) - ((v_l**2) / self.b_l))))

        v_next = min(v_acc, v_safe, self.v_desired)

        return (v_next-v)/env.sim_step
