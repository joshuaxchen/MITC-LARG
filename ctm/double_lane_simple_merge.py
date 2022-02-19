import os, math, imageio
from IPython.core.debugger import set_trace
import matplotlib.pyplot as plt

debug = True


class DoubleLaneSimpleMerge:
    def __init__(self, cell_length=100, total_main_len=700,
                 len_before_merge=600, freeflow_speed=21, critical_density=0.04,
                 jam_density=0.14, len_merge=200, waiting_penality_per_merge=1.13, threshold_density=0.0225, lc_rate_per_density_diff=0.5):
        main_cell_num = total_main_len // cell_length
        before_merge_index = len_before_merge // cell_length - 1
        duration_per_time_step = cell_length * 1.0 / freeflow_speed
        cell_maximum_flow = critical_density * freeflow_speed
        # theoretical maximum throughput in each cell
        self.Q = cell_maximum_flow * duration_per_time_step
        # the maximum amount of vehicles that can remain in each cell
        self.N = cell_length * jam_density
        self.freeflow_speed = freeflow_speed
        self.shockwave_speed = cell_maximum_flow / (jam_density - critical_density)

        self.cell_length = cell_length
        self.critical_density = critical_density
        self.threshold_density = threshold_density

        self.main_cell_num = main_cell_num
        self.before_merge_index = before_merge_index
        self.merge_cell_num = len_merge // cell_length
        self.duration_per_time_step = duration_per_time_step

        # print("The single-lane simple merge road has been initialized. Please specify the inflow in terms of veh/s. Additionally, the units used in the sytem are veh/s, m/s.")

        # the number of vehicles at each main cell at time t
        self.right_main_n_t_table = list()
        self.merge_n_t_table = list()
        main_n_0 = [0 for i in range(0, main_cell_num)]
        self.right_main_n_t_table.append(main_n_0)
        self.left_main_n_t_table.append(main_n_0)

        # the number of vehicles at each merge cell at time t
        self.merge_n_t_table = list()
        merge_n_0 = [0 for i in range(0, self.merge_cell_num)]
        self.merge_n_t_table.append(merge_n_0)

        self.t = 0
        # The remaining waiting time steps caused by the merging vehicles
        self.remaining_waiting = -1
        # The time caused by the merging vehicles
        self.waiting_penality_per_merge = waiting_penality_per_merge
        self.main_inflow_n_t_table = list()
        self.main_inflow_n_t_table.append(main_n_0)

        self.lc_rate_per_density_diff=lc_rate_per_density_diff
        # create a counter for the merging road
        # each time the merging vehicle will increase a penality on the main
        # road, if the penelty exceeds some threshold, then we block the
        # outflow of its upstream cell.
        # self.penality_to_block=0

    def get_inflow_according_to_cell_model(self, upstream_cell_capacity, current_veh, maximum_capacity, maximum_flow,
                                           shockwave_speed, freeflow_speed):
        # assume tha
        return min(upstream_cell_capacity, maximum_flow,
                   shockwave_speed * (maximum_capacity - current_veh) / freeflow_speed)

    def step(self, specified_main_inflow, specified_merge_inflow):
        # compute the inflow
        t = self.t + 1

        right_main_n_previous = self.right_main_n_t_table[self.t]
        left_main_n_previous = self.left_main_n_t_table[self.t]
        lc_from_right_to_left=list()
        # first compute the number of vehicles changing from right to left, or vice versa
        for i in range(0, self.main_cell_num):
            # check the density difference
            right_main_n_current_cell_t= right_main_n_previous[i]
            left_main_n_current_cell_t= left_main_n_previous[i]
            density_diff = (right_main_n_current_cell_t - left_main_n_current_cell_t) / self.cell_length
            # this can be negative
            num_of_veh_change_from_right_to_left = density_diff * self.lc_rate_per_density_diff * self.cell_length
            lc_from_right_to_left.append(num_of_veh_change_from_right_to_left)

        # first compute the inflow for the merge cells, who has higher
        # priorities than the main cell
        merge_n_previous = self.merge_n_t_table[self.t]
        merge_inflows = list()
        for i in range(0, self.merge_cell_num):
            merge_n_previous_cell_t = 0
            if i == 0:
                merge_n_previous_cell_t = specified_merge_inflow * self.duration_per_time_step
            else:
                merge_n_previous_cell_t = merge_n_previous[i - 1]
            merge_n_current_cell_t = merge_n_previous[i]
            # current_cell_merge_inflow=min(merge_n_previous_cell_t, self.Q, self.get_inflow_according_to_cell_model(merge_n_current_cell_t, self.N, self.Q, self.shockwave_speed, self.freeflow_speed))
            current_cell_merge_inflow = self.get_inflow_according_to_cell_model(merge_n_previous_cell_t,
                                                                                merge_n_current_cell_t, self.N, self.Q,
                                                                                self.shockwave_speed,
                                                                                self.freeflow_speed)
            merge_inflows.append(current_cell_merge_inflow)

        # set a flag whether there are merging vehicles waiting at the junction
        waiting_merge_veh = 0
        # compute the outflow for each **merge** cell
        merge_outflows = list()
        # compute the outflow for each main cell
        for i in reversed(range(0, self.merge_cell_num)):
            previous_n = merge_n_previous[i]
            outflow = 0
            if i == self.merge_cell_num - 1:  # the last merge cell
                # then this vehicle will move to the next cell
                # take the integer part of the merging inflow and take a note on the remaining part
                (previous_n, waiting_merge_veh) = math.modf(previous_n)
                outflow = waiting_merge_veh
            else:
                outflow = merge_inflows[i + 1]  # the outflow should equal to the inflow of the downstream cell
            merge_outflows.append(outflow)
        merge_outflows = list(reversed(merge_outflows))
        # print("waiting", waiting_merge_veh)

        assert waiting_merge_veh >= 0, "waiting should not be negative %f" % waiting_merge_veh
        # if waiting_merge_veh>=1:
        #    set_trace()

        # then compute the *right* inflow for the main cells
        right_main_inflows = list()
        for i in range(0, self.main_cell_num):
            right_main_n_previous_cell_t = 0
            if i == 0:  # the first cell has inflow maximum
                right_main_n_previous_cell_t = specified_main_inflow * self.duration_per_time_step
            elif i == self.before_merge_index + 1:  # after merge
                right_main_n_previous_cell_t = waiting_merge_veh + right_main_n_previous[i - 1]
            else:
                right_main_n_previous_cell_t = right_main_n_previous[i - 1]  # assume all vehicles will transit to the next
            right_main_n_current_cell_t = right_main_n_previous[i]
            current_cell_main_inflow = self.get_inflow_according_to_cell_model(right_main_n_previous_cell_t,
                                                                               right_main_n_current_cell_t, self.N,
                                                                               self.Q,
                                                                               self.shockwave_speed,
                                                                               self.freeflow_speed)
            right_main_inflows.append(current_cell_main_inflow)

        # then compute the *left* inflow for the main cells
        left_main_inflows = list()
        for i in range(0, self.main_cell_num):
            right_main_n_previous_cell_t = 0
            if i == 0:  # the first cell has inflow maximum
                left_main_n_previous_cell_t = specified_main_inflow * self.duration_per_time_step
            else:
                left_main_n_previous_cell_t = left_main_n_previous[i - 1]  # assume all vehicles will transit to the next
            left_main_n_current_cell_t = left_main_n_previous[i]
            current_cell_main_inflow = self.get_inflow_according_to_cell_model(left_main_n_previous_cell_t,
                                                                               left_main_n_current_cell_t, self.N,
                                                                               self.Q,
                                                                               self.shockwave_speed,
                                                                               self.freeflow_speed)

            current_cell_main_inflow+=num_of_veh_change_from_right_to_left
            left_main_inflows.append(current_cell_main_inflow)

        """
        ***********************************
        ***********************************
        ***********************************
        ***********************************
        """
        # compute the outflow for each **right main*** cell
        # modify the inflow of the main road due to the merge
        if t == 7:
            # set_trace()
            pass
        # if there are waiting vehicles waiting at the junction
        threshold = self.cell_length * self.threshold_density
        if waiting_merge_veh > 0:
            # if the number of vehicles is more than critical density
            if right_main_n_previous[self.before_merge_index] >= threshold:
                right_main_inflows[self.before_merge_index + 1] = waiting_merge_veh
            # otherwise, use the default one from upstream

        elif self.remaining_waiting > 0:  # no waiting vehicle, but been blocked by previous time steps
            if right_main_n_previous[self.before_merge_index] >= threshold:
                if self.remaining_waiting >= 1:
                    right_main_inflows[self.before_merge_index + 1] = waiting_merge_veh
                elif 0 < self.remaining_waiting and self.remaining_waiting < 1:  # 0<self.remaining_waiting<1
                    right_main_inflows[self.before_merge_index + 1] = right_main_inflows[self.before_merge_index + 1] * (
                                1 - self.remaining_waiting)
                else:
                    right_main_inflows[self.before_merge_index + 1] = 0

        if debug:
            print("main inflows", right_main_inflows)
        self.main_inflow_n_t_table.append(right_main_inflows)

        right_main_outflows = list()
        # print("main_cell_num", self.main_cell_num)
        # print("before_merge_index", self.before_merge_index)
        for i in reversed(range(0, self.main_cell_num)):
            previous_n = right_main_n_previous[i]
            if i == self.main_cell_num - 1:  # all vehicles will go out
                outflow = previous_n
            elif i == self.before_merge_index:
                outflow = max(0, right_main_inflows[i + 1] - waiting_merge_veh)
            else:
                outflow = right_main_inflows[i + 1]  # inflow from downstream
            right_main_outflows.append(outflow)
        right_main_outflows = list(reversed(right_main_outflows))
        if debug:
            print("main_outflows", right_main_outflows)

            # update the number of current vehicles at the merge road
        merge_n_t = list()
        for i in range(0, self.merge_cell_num):
            previous_n = merge_n_previous[i]
            inflow = merge_inflows[i]
            outflow = merge_outflows[i]
            merge_n_t.append(previous_n - outflow + inflow)
        self.merge_n_t_table.append(merge_n_t)

        # update the number of current vehicles at the main road
        right_main_n_t = list()
        for i in range(0, self.main_cell_num):
            previous_n = right_main_n_previous[i]
            inflow = right_main_inflows[i]
            outflow = right_main_outflows[i]
            right_main_n_t.append(previous_n + inflow - outflow)
        self.right_main_n_t_table.append(right_main_n_t)

        if waiting_merge_veh > 0:
            self.remaining_waiting = self.waiting_penality_per_merge
        else:
            if self.remaining_waiting > 0:
                self.remaining_waiting -= 1
        self.t = t

    def compute_inflow(self):
        main_inflow = 0
        time = 0
        for main_inflow_t in self.main_inflow_n_t_table:
            main_inflow += main_inflow_t[0]
            time += self.duration_per_time_step
        avg_main_inflow = main_inflow / time

        merge_inflow = 0
        for merge_n_t in self.merge_n_t_table:
            merge_inflow += merge_n_t[0]
        avg_merge_inflow = merge_inflow / time

        return (avg_main_inflow, avg_merge_inflow)

    def compute_outflow(self):
        outflow = 0
        time = 0
        for main_n_t in self.right_main_n_t_table:
            outflow += main_n_t[-1]
            time += self.duration_per_time_step
        avg_outflow = outflow / time
        return avg_outflow

    def simulate(self, main_inflow, merge_inflow, total_time_steps):
        # set_trace()
        if debug:
            print("-------------t=%d--------------" % 0)
            print("main road:", self.right_main_n_t_table[0])
            print("merge road:", self.merge_n_t_table[0])
        for t in range(1, total_time_steps):
            # set_trace()
            temp = merge_inflow / 3600.0
            if t >= total_time_steps / 2:
                temp = 0
            self.step(main_inflow / 3600.0, temp)
            if debug:
                print("-------------t=%d--------------" % t)
                print("main road:", self.right_main_n_t_table[t])
                print("merge road:", self.merge_n_t_table[t])
        avg_outflow = self.compute_outflow()
        avg_main_inflow, avg_merge_inflow = self.compute_inflow()
        if debug:
            print("outflow (veh/hour):", avg_outflow * 3600)
            print("inflow (veh/hour):", avg_main_inflow * 3600, avg_merge_inflow * 3600)
        return (avg_main_inflow * 3600, avg_merge_inflow * 3600, avg_outflow * 3600)
        # file=open(filename, "w")
        # file.write(content)
        # file.close()

    def make_gif(self, duration=0.3):
        # plot the main_n_t
        x = [i for i in range(0, self.main_cell_num)]
        t = 0
        filenames = []
        for main_n_t in self.right_main_n_t_table:
            # main road
            inflows = self.main_inflow_n_t_table[t]
            old_capacity = list()
            # print("len of main_n_t", len(main_n_t))
            # print("len of main_inflow_n_t", len(inflows))
            for i in range(len(main_n_t)):
                old_capacity.append(main_n_t[i] - inflows[i])
            plt.bar(x, old_capacity)
            plt.bar(x, inflows, bottom=old_capacity, color='g')
            # merge road
            plt.bar(self.main_cell_num + 1, self.merge_n_t_table[t])

            # print(main_n_t)
            plt.xlim(0, self.main_cell_num + 2)
            plt.ylim(0, self.N)
            filename = f'./figures/{t}.png'
            filenames.append(filename)
            plt.savefig(filename)
            plt.close()
            t += 1

        with imageio.get_writer('./figures/mygif.gif', mode='I', duration=duration) as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)
        for filename in set(filenames):
            os.remove(filename)


if __name__ == "__main__":
    results = dict()
    duration = 100 / 21.0
    # for merge_inflow in [160, 180, 200]:
    #    for main_inflow in [1400, 1500, 1600, 1700, 1800, 1900, 2000]:
    for main_inflow in [1800]:
        for merge_inflow in [200]:
            single_lane_simple_merge = SingleLaneSimpleMerge()
            (avg_main_inflow, avg_merge_inflow,
             avg_outflow) = single_lane_simple_merge.simulate(main_inflow,
                                                              merge_inflow, math.ceil(1000 / duration))
            results[str(main_inflow) + "-" + str(merge_inflow)] = (avg_main_inflow, avg_merge_inflow, avg_outflow)
            # print(main_inflow, merge_inflow, avg_main_inflow, avg_merge_inflow, avg_outflow)
            print(main_inflow, merge_inflow, avg_outflow)
            if debug:
                single_lane_simple_merge.make_gif()
    # print(results)





