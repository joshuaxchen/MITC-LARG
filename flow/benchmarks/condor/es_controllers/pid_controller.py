from flow.controllers.base_controller import BaseController

class Controller(BaseController):
    def __init__(self,
            veh_id,
            car_following_params,
            target,
            p,
            i,
            d):
        super().__init__(veh_id, car_following_params)
        self.target = target
        self.p = p
        self.i = i
        self.d = d
        self._int = 0
        self._last = 0

    def get_accel(self, env):
        measure = env.k.vehicle.get_headway(self.veh_id)/env.k.vehicle.get_speed(self.veh_id)
        diff = (self.target - measure)
        self._int += diff
        deriv = (diff-self._last)
        self._last = diff
        accel = max(self.p,0)*diff + max(self.i,0)*self._int + max(self.d,0)*deriv
        return accel

