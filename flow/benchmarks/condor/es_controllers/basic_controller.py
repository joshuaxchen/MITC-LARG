from flow.controllers.base_controller import BaseController
class Controller(BaseController):
    def __init__(self,
                 veh_id,
                 car_following_params,
                 slow_speed,
                 stop_distance,
                 start_distance):
        super().__init__(veh_id, car_following_params)
        self.slow_speed = slow_speed
        self.stop_distance = stop_distance
        self.start_distance = start_distance
        
    def get_accel(self, env):
        if env.k.vehicle.get_edge(self.veh_id) != env.env_params.additional_params['merge_edge']:
            return None
        dist = env.k.vehicle.get_position(self.veh_id)
        if dist < self.stop_distance:
            return None
        cur_vel = env.k.vehicle.get_speed(self.veh_id)
        if dist < self.start_distance:
            accel = (self.slow_speed - cur_vel) / 2
        else:
            accel = 1
        return accel

