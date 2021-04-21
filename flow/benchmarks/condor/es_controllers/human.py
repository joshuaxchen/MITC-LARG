from flow.controllers.base_controller import BaseController
class Controller(BaseController):
    def __init__(self,
            veh_id,
            car_following_params):
        super().__init__(veh_id, car_following_params)
        
    def get_accel(self, env):
        return None

