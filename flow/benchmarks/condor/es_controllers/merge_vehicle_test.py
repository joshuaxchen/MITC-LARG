from flow.controllers.base_controller import BaseController
class Controller(BaseController):
    def __init__(self,
                 veh_id,
                 car_following_params,
                 target_headway,
                 threshold):
        super().__init__(veh_id, car_following_params)
        self.target_headway = target_headway
        self.threshold = threshold
        
    def get_accel(self, env):
        merge_vehs = env.k.vehicle.get_ids_by_edge("bottom")
        center_x = env.k.network.total_edgestarts_dict["center"]
        merge_dists = [(env.k.vehicle.get_position(veh), veh) for veh in merge_vehs]
        len_bottom = env.k.network.edge_length("bottom")
        position = env.k.network.total_edgestarts_dict["bottom"]
        merge_veh = None
        if len(merge_dists)>0:
            position, merge_veh = max(merge_dists, key=lambda y:y[0])
        if merge_veh is None:
            return 1
        merge_distance = (len_bottom - position)
        merge_vel = env.k.vehicle.get_speed(merge_veh)
        if merge_vel == 0:
            return 1
        merge_time = merge_distance/merge_vel
        veh_x = env.k.vehicle.get_x_by_id(self.veh_id)
        distance = veh_x = center_x
        if distance > center_x:
            return 1
        veh_vel = env.k.vehicle.get_speed(self.veh_id)
        if (veh_vel == 0):
            return 1
        time_to_intersection = (center_x - distance)/veh_vel
        if (merge_time - time_to_intersection) > self.threshold:
            return 1
        target_vel = (center_x - distance)/(merge_time+self.target_headway)
        return (target_vel-veh_vel)


