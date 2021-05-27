from flow.envs.multiagent.highway import MultiAgentHighwayPOEnv

class MultiAgentHighwayPOEnvDistanceMergeInfoMOR(MultiAgentHighwayPOEnv):
    @property
    def observation_space(self):
        return Box(low=-1, high=1, shape=(7, ), dtype=np.float32)

    def get_state(self):
        """See class definition."""
        obs = {}

        # normalizing constants
        max_speed = self.k.network.max_speed()
        max_length = self.k.network.length()
        for rl_id in self.k.vehicle.get_rl_ids():
            this_speed = self.k.vehicle.get_speed(rl_id)
            lead_id = self.k.vehicle.get_leader(rl_id)
            follower = self.k.vehicle.get_follower(rl_id)

            if lead_id in ["", None]:
                # in case leader is not visible
                lead_speed = max_speed
                lead_head = max_length
            else:
                lead_speed = self.k.vehicle.get_speed(lead_id)
                lead_head = self.k.vehicle.get_headway(rl_id)

            if follower in ["", None]:
                # in case follower is not visible
                follow_speed = 0
                follow_head = max_length
            else:
                follow_speed = self.k.vehicle.get_speed(follower)
                follow_head = self.k.vehicle.get_headway(follower)
            
            veh_x = self.k.vehicle.get_x_by_id(rl_id)
            merge_edge = None
            merge_edge_pos = float('inf')
            for e in self.env_params.additional_params['merging_edges']:
                p = self.k.network.total_edgestarts_dict[e]
                if p < edge_pos and p > veh_x:
                    merge_edge_pos = p
                    merge_edge = e
            merge_distance = 1
            if merge_edge is not None:
                len_merge = self.k.network.edge_length("merge_edge")
                merge_vehs = self.k.vehicle.get_ids_by_edge(merge_edge)
                merge_dists = [self.k.vehicle.get_position(veh) for veh in merge_vehs]
                if len(merge_dists) > 0:
                    merge_pos = max(merge_dists)
                    merge_distance = (len_merge - merge_pos)/len_merge

            edge = self.k.vehicle.get_edge(rl_id)
            length = self.k.network.edge_length(edge)
            pos = self.k.vehicle.get_position(rl_id)
            distance = (length - pos)/(length)
            else:
                pass #FIXME implement

            observation = np.array([
                this_speed / max_speed,
                (lead_speed - this_speed) / max_speed,
                lead_head / max_length,
                (this_speed - follow_speed) / max_speed,
                follow_head / max_length,
                np.clip(distance,-1,1),
                np.clip(merge_distance,-1,1),

            ])

            obs.update({rl_id: observation})

        return obs
