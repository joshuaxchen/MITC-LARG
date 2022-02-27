import os, math, imageio
from IPython.core.debugger import set_trace
import matplotlib.pyplot as plt

debug = True


class DoubleLaneSimpleMerge:
    def __init__(self, cell_length=100, total_main_len=700,
                 len_before_merge=600, freeflow_speed=21, critical_density=0.04,
                 jam_density=0.14, len_merge=200, waiting_penality_per_merge=1.13, merge_threshold_density=0.0225, lc_rate_per_density_diff=0.04, lc_threshold_density=0.03, lc_slow_down_rate=0.4):
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
        self.merge_threshold_density = merge_threshold_density
        self.lc_threshold_density=lc_threshold_density
        self.jam_density=jam_density
        self.lc_slow_down_rate=lc_slow_down_rate

        self.main_cell_num = main_cell_num
        self.before_merge_index = before_merge_index
        self.merge_cell_num = len_merge // cell_length
        self.duration_per_time_step = duration_per_time_step

        # print("The single-lane simple merge road has been initialized. Please specify the inflow in terms of veh/s. Additionally, the units used in the sytem are veh/s, m/s.")

        # the number of vehicles at each main cell at time t
        self.right_main_n_t_table = list()
        self.left_main_n_t_table = list()
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
        self.right_main_inflow_n_t_table = list()
        self.right_main_inflow_n_t_table.append(main_n_0)
        self.left_main_inflow_n_t_table = list()
        self.left_main_inflow_n_t_table.append(main_n_0)

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

    def compute_lane_change(self, right_main_n_previous, left_main_n_previous):
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
        return lc_from_right_to_left

    def compute_inflow_from_upstream(self, main_or_merge_previous,
    specified_inflow, num_of_cells, out_due_to_lc, before_merge_index=None,
    waiting_merge_veh=None):
        # first compute the inflow for the merge cells, who has higher
        # priorities than the main cell
        inflows = list()
        for i in range(0, num_of_cells):
            merge_n_previous_cell_t = 0
            if i == 0:# inflow at the beginning
                previous_cell_t = specified_inflow * self.duration_per_time_step
            elif i-1==before_merge_index and waiting_merge_veh is not None: # inflow before merge
                previous_cell_t= waiting_merge_veh + main_or_merge_previous[i - 1] - max(out_due_to_lc[i-1],0)
            else:
                previous_cell_t = main_or_merge_previous[i - 1] - max(out_due_to_lc[i-1],0)
            current_cell_t = main_or_merge_previous[i]
            # current_cell_merge_inflow=min(merge_n_previous_cell_t, self.Q, self.get_inflow_according_to_cell_model(merge_n_current_cell_t, self.N, self.Q, self.shockwave_speed, self.freeflow_speed))
            current_cell_inflow = self.get_inflow_according_to_cell_model(previous_cell_t, current_cell_t, self.N, self.Q, self.shockwave_speed, self.freeflow_speed)
            inflows.append(current_cell_inflow)
        return inflows

    def compute_outflow_from_downstream(self, main_or_merge_previous, inflows,
    num_of_cells, out_due_to_lc, waiting_merge_veh=None, before_merge_index=None, outflow_of_last_cell=None):
        outflows=list()
        for i in reversed(range(0, num_of_cells)):
            previous_n = main_or_merge_previous[i]
            if i == num_of_cells - 1:  # all vehicles will go out
                if outflow_of_last_cell is not None:
                    outflow=outflow_of_last_cell - out_due_to_lc[i]
                else:
                    outflow = previous_n - out_due_to_lc[i]
            elif i == before_merge_index and waiting_merge_veh is not None:
                outflow = max(0, inflows[i + 1] - waiting_merge_veh)
            else:
                outflow = inflows[i + 1]  # inflow from downstream
            outflows.append(outflow)
        outflows = list(reversed(outflows))
        if debug:
            print("outflows", outflows)
        return outflows

    def step(self, specified_left_main_inflow, specified_right_main_inflow, specified_merge_inflow):
        # compute the inflow
        t = self.t + 1

        right_main_n_previous = self.right_main_n_t_table[self.t]
        left_main_n_previous = self.left_main_n_t_table[self.t]
        # compute the amount of vehicles changing from right to left
        # (positive), or from left to right (negative) 
        lc_from_right_to_left=self.compute_lane_change(right_main_n_previous, left_main_n_previous)
        #lc_from_right_to_left=[0 for i in range(self.main_cell_num)]
        if debug:
            print("left_main_n_previous", left_main_n_previous)
            print("right_main_n_previous", right_main_n_previous)
            print("lc_from_right_to_left", lc_from_right_to_left)

        # first compute the inflow for the merge cells, who has higher
        # priorities than the main cell
        merge_n_previous = self.merge_n_t_table[self.t]
        merge_inflows = self.compute_inflow_from_upstream(merge_n_previous, specified_merge_inflow, self.merge_cell_num, [0]*self.merge_cell_num)

        # set a flag whether there are merging vehicles waiting at the junction
        waiting_merge_veh = 0
        # compute the outflow for each **merge** cell
        merge_outflows = self.compute_outflow_from_downstream(merge_n_previous, merge_inflows, self.merge_cell_num, [0]*self.merge_cell_num)
        # compute the outflow at the last cell 
        last_merge_index=self.merge_cell_num - 1
        veh_at_last_merge_cell=merge_n_previous[last_merge_index]
        (remaining_n, waiting_merge_veh) = math.modf(veh_at_last_merge_cell)
        merge_outflows[last_merge_index]=waiting_merge_veh

        assert waiting_merge_veh >= 0, "waiting should not be negative %f" % waiting_merge_veh
        # if waiting_merge_veh>=1:
        #    set_trace()

        # then compute the *right* inflow for the main cells
        right_main_inflows = self.compute_inflow_from_upstream(right_main_n_previous,
                                                               specified_right_main_inflow, self.main_cell_num, lc_from_right_to_left, before_merge_index=self.before_merge_index, waiting_merge_veh=waiting_merge_veh)
        
        # then compute the *left* inflow for the main cells
        out_from_left_lane_due_to_lc=[-1*lc for lc in lc_from_right_to_left]
        left_main_inflows = self.compute_inflow_from_upstream(left_main_n_previous, specified_left_main_inflow, self.main_cell_num, out_from_left_lane_due_to_lc)
        # Here, we ****simplify the problem **** by assuming that the lane changing
        # vehicle will not change the density of the vehicles in the target
        # cell 

        #i=0
        #left_main_inflow_with_lc=list()
        #for num_of_veh_change_from_right_to_left in lc_from_right_to_left:
        #    left_main_inflow_with_lc.append(left_main_inflows[i]+num_of_veh_change_from_right_to_left)
        #    i+=1  

        #left_main_inflows=left_main_inflow_with_lc

        """
        ***********************************
        ***********************************
        ***********************************
        """
        # modify the inflow of the main road due to the merge
        if t == 7:
            # set_trace()
            pass
        # if there are waiting vehicles waiting at the junction
        threshold = self.cell_length * self.merge_threshold_density
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

        # TODO: modify the inflow of the main road due to lane change
        # assume tha the lane change vehicles will slow down the average speed
        # of the vehicle
        outflow_of_last_cell_left_lane=None
        outflow_of_last_cell_right_lane=None
        for i in range(self.main_cell_num):
            lc=lc_from_right_to_left[i]
            if lc==0:
                continue
            inflows=left_main_inflows
            outflow_of_last_cell=None
            if lc>0: # from right to left, then re-compute the inflow of the left lane
                current_cell_capacity=left_main_n_previous[i]
            else:# otherwise, re-compute the inflow of the right lane
                current_cell_capacity = right_main_n_previous[i]
                inflows=right_main_inflows
                lc=-lc
            current_cell_density=current_cell_capacity/self.cell_length
            increased_density=lc/self.cell_length
            if current_cell_density<0:
                print("")
                pass
            #print("increased_density", increased_density)
            #print("current cell density", current_cell_density)
            if debug:
                print("sum density", current_cell_density+increased_density, "increased density", increased_density)
            if current_cell_density+increased_density>=self.lc_threshold_density: # get a slow down in the left lane
                # reduce the outflow of the current cell, i.e., reduce the inflow of the next cell
                # The decreased outflow is proportional to the amount of increased density
                decrease_rate = self.lc_slow_down_rate #- min(increased_density*500, 0.3)
                #max_lc=self.lc_rate_per_density_diff*self.jam_density*self.cell_length
                #decrease_rate=min(math.exp(-lc/max_lc)*self.lc_slow_down_rate,1)
                #print(i, "lc=", lc, math.exp(1-lc/max_lc)*self.lc_slow_down_rate, decrease_rate)
                if i<self.main_cell_num-1:
                    #set_trace()
                    inflow_at_next_cell=inflows[i+1]
                    #inflow_at_next_cell=inflow_at_next_cell*(1-self.lc_slow_down_rate*increased_density/(self.jam_density-self.critical_density))
                    inflow_at_next_cell=inflow_at_next_cell*decrease_rate
                    inflows[i+1]=inflow_at_next_cell
                else: # decrease the outflow of the last cell
                    #outflow_of_last_cell=current_cell_capacity*(1-self.lc_slow_down_rate*increased_density/(self.jam_density-self.critical_density))
                    outflow_of_last_cell = current_cell_capacity *decrease_rate
            if lc>0:
                outflow_of_last_cell_left_lane=outflow_of_last_cell
            else:
                outflow_of_last_cell_right_lane=outflow_of_last_cell

        if debug:
            print("main inflows", right_main_inflows)
        self.right_main_inflow_n_t_table.append(right_main_inflows)

        # compute the outflow for each **right main*** cell
        right_main_outflows =self.compute_outflow_from_downstream(right_main_n_previous, right_main_inflows, self.main_cell_num, lc_from_right_to_left, waiting_merge_veh=waiting_merge_veh, before_merge_index=self.before_merge_index, outflow_of_last_cell=outflow_of_last_cell_right_lane)

        # compute the outflow for each **left main*** cell
        out_from_left_lane_due_to_lc=[-1*lc for lc in lc_from_right_to_left]
        left_main_outflows =self.compute_outflow_from_downstream(left_main_n_previous, left_main_inflows, self.main_cell_num, out_from_left_lane_due_to_lc, outflow_of_last_cell=outflow_of_last_cell_left_lane)
        self.left_main_inflow_n_t_table.append(left_main_inflows)
        
        # update the number of current vehicles at the merge road
        merge_n_t = list()
        for i in range(0, self.merge_cell_num):
            previous_n = merge_n_previous[i]
            inflow = merge_inflows[i]
            outflow = merge_outflows[i]
            merge_n_t.append(max(previous_n - outflow + inflow,0))
        self.merge_n_t_table.append(merge_n_t)

        # update the number of current vehicles at the ***right*** main road
        right_main_n_t = list()
        for i in range(0, self.main_cell_num):
            previous_n = right_main_n_previous[i]
            inflow = right_main_inflows[i]
            outflow = right_main_outflows[i]
            lc=-1*lc_from_right_to_left[i]
            right_main_n_t.append(max(previous_n + inflow - outflow + lc,0))
        self.right_main_n_t_table.append(right_main_n_t)
        
        # update the number of current vehicles at the ***left*** main road
        left_main_n_t = list()
        for i in range(0, self.main_cell_num):
            previous_n = left_main_n_previous[i]
            inflow = left_main_inflows[i]
            outflow = left_main_outflows[i]
            lc=lc_from_right_to_left[i]
            if previous_n + inflow - outflow + lc<0:
                set_trace()
            left_main_n_t.append(max(previous_n + inflow - outflow + lc,0)) # max to deal with numeric issues
        self.left_main_n_t_table.append(left_main_n_t)
        
        # update the waiting vehicle and remaining waiting penality
        if waiting_merge_veh > 0:
            self.remaining_waiting = self.waiting_penality_per_merge
        else:
            if self.remaining_waiting > 0:
                self.remaining_waiting -= 1
        self.t = t

    def compute_inflow(self):
        main_inflow = 0
        time = 0
        for right_main_inflow_t in self.right_main_inflow_n_t_table:
            main_inflow += right_main_inflow_t[0]
            time += self.duration_per_time_step
        avg_right_main_inflow = main_inflow / time

        main_inflow = 0
        time = 0
        for left_main_inflow_t in self.left_main_n_t_table:
            main_inflow += left_main_inflow_t[0]
            time += self.duration_per_time_step
        avg_left_main_inflow = main_inflow / time

        merge_inflow = 0
        for merge_n_t in self.merge_n_t_table:
            merge_inflow += merge_n_t[0]
        avg_merge_inflow = merge_inflow / time

        return (avg_left_main_inflow, avg_right_main_inflow, avg_merge_inflow)

    def compute_outflow(self):
        outflow = 0
        time = 0
        for right_main_n_t in self.right_main_n_t_table:
            outflow += right_main_n_t[-1]
            time += self.duration_per_time_step
        avg_right_outflow = outflow / time

        outflow=0
        time = 0
        for left_main_n_t in self.left_main_n_t_table:
            outflow += left_main_n_t[-1]
            time += self.duration_per_time_step
        avg_left_outflow = outflow / time
        return avg_left_outflow, avg_right_outflow

    def simulate(self, left_main_inflow, right_main_inflow, merge_inflow, total_time_steps):
        # set_trace()
        if debug:
            print("-------------t=%d--------------" % 0)
            print("left main road:", self.left_main_n_t_table[0])
            print("right main road:", self.right_main_n_t_table[0])
            print("merge road:", self.merge_n_t_table[0])
        for t in range(1, total_time_steps):
            # set_trace()
            temp = merge_inflow / 3600.0
            #if t >= total_time_steps / 2:
            #    temp = 0
            self.step(left_main_inflow / 3600.0, right_main_inflow / 3600.0, temp)
            if debug:
                print("-------------t=%d--------------" % t)
                print("left main road:", self.left_main_n_t_table[t])
                print("right main road:", self.right_main_n_t_table[t])
                print("merge road:", self.merge_n_t_table[t])
        avg_left_outflow, avg_right_outflow= self.compute_outflow()
        avg_left_main_inflow, avg_right_main_inflow, avg_merge_inflow = self.compute_inflow()
        if debug:
            print("left outflow (veh/hour):", avg_left_outflow * 3600)
            print("right outflow (veh/hour):", avg_right_outflow * 3600)
            print("left inflow (veh/hour):", avg_left_main_inflow* 3600)
            print("right inflow (veh/hour):", avg_right_main_inflow * 3600)
            print("merge inflow (veh/hour):",  avg_merge_inflow * 3600)
        return (avg_left_main_inflow* 3600, avg_right_main_inflow* 3600, avg_merge_inflow * 3600,avg_left_outflow* 3600, avg_right_outflow* 3600)
        # file=open(filename, "w")
        # file.write(content)
        # file.close()

    def make_gif(self, left_inflow, right_inflow, merge_inflow, avg_left_outflow, avg_right_outflow, duration=0.3):
        # plot the main_n_t
        x = [i for i in range(0, self.main_cell_num)]
        t = 0
        filenames = []
        for right_main_n_t in self.right_main_n_t_table:
            left_main_n_t=self.left_main_n_t_table[t]

            figure, axis = plt.subplots(1, 2, figsize=(20,8))
            #plt.tight_layout(pad=30)
            plt.suptitle(f'Left MainInflow {left_inflow} veh/hour, Right MainInflow {right_inflow} veh/hour, Merge Inflow {merge_inflow} veh/hour\n\n Left MainOutflow {avg_left_outflow:.2f} veh/hour, Right MainOutflow {avg_left_outflow:.2f} veh/hour')
            plot_for_left_road=axis[0]
            plot_for_right_road=axis[1]

            # right main road
            inflows = self.right_main_inflow_n_t_table[t]
            old_capacity = list()
            # print("len of main_n_t", len(main_n_t))
            # print("len of main_inflow_n_t", len(inflows))
            for i in range(len(right_main_n_t)):
                old_capacity.append(right_main_n_t[i] - inflows[i])
            plot_for_right_road.bar(x, old_capacity)
            plot_for_right_road.bar(x, inflows, bottom=old_capacity, color='g')
            # merge road
            plot_for_right_road.bar(self.main_cell_num + 1, self.merge_n_t_table[t])

            # print(main_n_t)
            plot_for_right_road.set_xlim(0, self.main_cell_num + 2)
            plot_for_right_road.set_ylim(0, self.N)
            plot_for_right_road.title.set_text('Right Lane Cells')


            # left main road
            inflows = self.left_main_inflow_n_t_table[t]
            old_capacity = list()
            # print("len of main_n_t", len(main_n_t))
            # print("len of main_inflow_n_t", len(inflows))
            for i in range(len(left_main_n_t)):
                old_capacity.append(left_main_n_t[i] - inflows[i])
            plot_for_left_road.bar(x, old_capacity)
            plot_for_left_road.bar(x, inflows, bottom=old_capacity, color='g')
            plot_for_left_road.title.set_text('Left Lane Cells')
            # merge road

            # print(main_n_t)
            plot_for_left_road.set_xlim(0, self.main_cell_num + 1)
            plot_for_left_road.set_ylim(0, self.N)

            plt.sca(axis[0])
            plt.xticks(range(self.main_cell_num+1),range(self.main_cell_num+1))
            plt.sca(axis[1])
            plt.xticks(range(self.main_cell_num+2),range(self.main_cell_num+2))
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
    for right_main_inflow in [1800]:
        for left_main_inflow in [1500]:
            for merge_inflow in [200]:
                single_lane_simple_merge = DoubleLaneSimpleMerge()

                (avg_left_main_inflow, avg_right_main_inflow, avg_merge_inflow,
                 avg_left_outflow, avg_right_outflow) = single_lane_simple_merge.simulate(left_main_inflow,
                                                                                          right_main_inflow,
                                                                                          merge_inflow,
                                                                                          math.ceil(1000 / duration))
                results[str(left_main_inflow) +"-"+str(right_main_inflow) + "-" + str(merge_inflow)] =(avg_left_outflow, avg_right_outflow)
                # print(main_inflow, merge_inflow, avg_main_inflow, avg_merge_inflow, avg_outflow)
                print(str(left_main_inflow) +"-"+str(right_main_inflow) + "-" + str(merge_inflow), avg_left_outflow, avg_right_outflow, avg_left_outflow + avg_right_outflow)
                if debug:
                    single_lane_simple_merge.make_gif(left_main_inflow, right_main_inflow, merge_inflow, avg_left_outflow, avg_right_outflow)
    # print(results)





