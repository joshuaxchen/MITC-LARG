from flow.controllers.base_controller import BaseController
class Controller(BaseController):
    def __init__(self,
                 veh_id,
                 car_following_params,
                 target_headway):
        super().__init__(veh_id, car_following_params)
        self.target_headway = target_headway
        self.reached_goal = False
        
    def get_accel(self, env):
        if not self.reached_goal:
            headway = env.k.vehicle.get_headway(self.veh_id)
            if headway >= self.target_headway:
                self.reached_goal = True

        if self.reached_goal:
            return 1
        else:
            return -1

