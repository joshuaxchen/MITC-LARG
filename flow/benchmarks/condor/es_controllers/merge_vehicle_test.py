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
            merge_vehs = env.k.vehicle.get_ids_by_edge("bottom")
            center_x = env.k.network.total_edgestarts_dict["center"]
            merge_dists = [env.k.vehicle.get_position(veh) for veh in merge_vehs]
            len_bottom = env.k.network.edge_length("bottom")
            position = env.k.network.total_edgestarts_dict["bottom"]
            if len(merge_dists)>0:
                position = max(merge_dists)
            merge_distance = (len_bottom - position)
            veh_x = env.k.vehicle.get_x_by_id(self.veh_id)
            distance = veh_x = center_x
            if distance - merge_distance > self.target_headway:
                self.reached_goal = True

        if self.reached_goal:
            return 1
        else:
            cur_vel = env.k.vehicle.get_speed(self.veh_id)
            return (8-cur_vel)

