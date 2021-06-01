from flow.controllers.base_controller import BaseController
class Controller(BaseController):
    def __init__(self,
                 veh_id,
                 car_following_params,
                 slow_speed,
                 target_headway):
        super().__init__(veh_id, car_following_params)
        self.slow_speed = slow_speed
        self.target_headway = target_headway
        
    def get_accel(self, env):
        cur_vel = env.k.vehicle.get_speed(self.veh_id)
        headway = env.k.vehicle.get_headway(self.veh_id)
        if headway < self.target_headway:
            accel = (self.slow_speed - cur_vel) / 2
        else:
            accel = 1
        return accel

