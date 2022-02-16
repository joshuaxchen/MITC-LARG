import os, math
from IPython.core.debugger import set_trace
debug=False
class SingleLaneSimpleMerge:
    def __init__(self, cell_length=100, main_cell_num=7, freeflow_speed=20,
    duration_per_time_step=5, critical_density=0.04, jam_density=0.14,
    before_merge_index=5, merge_cell_num=2, waiting_times=1):
        cell_maximum_flow=critical_density*freeflow_speed
        # theoretical maximum throughput in each cell
        self.Q=cell_maximum_flow*duration_per_time_step
        # the maximum amount of vehicles that can remain in each cell
        self.N=cell_length*jam_density
        self.freeflow_speed=freeflow_speed
        self.shockwave_speed=cell_maximum_flow/(jam_density-critical_density)

        self.main_cell_num=main_cell_num
        self.before_merge_index=before_merge_index
        self.merge_cell_num=merge_cell_num
        self.duration_per_time_step=duration_per_time_step

        print("The single-lane simple merge road has been initialized. Please specify the inflow in terms of veh/s. Additionally, the units used in the sytem are veh/s, m/s.")

        # the number of vehicles at each main cell at time t 
        self.main_n_t_table=list()
        self.merge_n_t_table=list()
        main_n_0=[0 for i in range(0, main_cell_num)]
        self.main_n_t_table.append(main_n_0)

        # the number of vehicles at each merge cell at time t 
        self.merge_n_t_table=list()
        merge_n_0=[0 for i in range(0, merge_cell_num)]
        self.merge_n_t_table.append(merge_n_0)

        self.t=0
        self.remaining_waiting=-1
        self.waiting_times=waiting_times
        self.main_inflow_n_t_table=list()
        self.main_inflow_n_t_table.append(main_n_0)


    def step(self, specified_main_inflow, specified_merge_inflow):
        # compute the inflow  
        t=self.t+1 

        # first compute the inflow for the merge cells, who has higher
        # priorities than the main cell 
        merge_n_previous=self.merge_n_t_table[self.t]
        merge_inflows=list()
        for i in range(0, self.merge_cell_num):
            if i==0:
                merge_n_previous_t=specified_merge_inflow*self.duration_per_time_step
            else:
                merge_n_previous_t=merge_n_previous[i-1]
            current_merge_inflow=min(merge_n_previous_t, self.Q, self.shockwave_speed*(self.N-merge_n_previous[i])/self.freeflow_speed )
            merge_inflows.append(current_merge_inflow)

        # then compute the inflow for the main cells
        main_n_previous=self.main_n_t_table[self.t]
        main_inflows=list()
        for i in range(0, self.main_cell_num):
            if i==0:
                main_n_previous_cell_t=specified_main_inflow*self.duration_per_time_step
            else:
                main_n_previous_cell_t=main_n_previous[i-1] # assume all vehicles will transit to the next
            current_main_inflow=min(main_n_previous_cell_t, self.Q, self.shockwave_speed*(self.N-main_n_previous[i])/self.freeflow_speed )
            main_inflows.append(current_main_inflow)

        # set a flag whether there are merging vehicles waiting at the junction 
        waiting_merge_veh=0
        # compute the outflow for each merge cell
        merge_outflows=list() 
        # compute the outflow for each main cell 
        for i in reversed(range(0, self.merge_cell_num)):
            previous_n=merge_n_previous[i]
            outflow=0
            if i==self.merge_cell_num-1: # the last merge cell
                # then this vehicle will move to the next cell 
                (previous_n, waiting_merge_veh)=math.modf(previous_n)# remove the outflow to the 
                outflow=waiting_merge_veh
            else:
                outflow=merge_inflows[i+1]# the outflow should equal to the inflow of the downstream cell
            merge_outflows.append(outflow)
        merge_outflows=list(reversed(merge_outflows)) 
        #print("waiting", waiting_merge_veh)
        # compute the outflow for each main cell 
        # modify the inflow of the main road due to the merge
        if waiting_merge_veh>0 or self.remaining_waiting>0: # there are waiting vehicles waiting
            main_inflows[self.before_merge_index+1]=waiting_merge_veh
        #print("main inflows", main_inflows) 
        self.main_inflow_n_t_table.append(main_inflows)

        main_outflows=list() 
        for i in reversed(range(0, self.main_cell_num)):
            previous_n=main_n_previous[i]
            if i==self.main_cell_num-1:# all vehicles will go out
                outflow=previous_n
            else:# the outflow should equal to the inflow of the downstream cell
                outflow=main_inflows[i+1]
            if i==self.before_merge_index:
                if waiting_merge_veh>0 or self.remaining_waiting>0: # there are waiting vehicles waiting
                    outflow=0

            main_outflows.append(outflow)
        main_outflows=list(reversed(main_outflows)) 
        #print("main_outflows", main_outflows) 

        # update the number of current vehicles at the merge road
        merge_n_t=list()
        for i in range(0, self.merge_cell_num):
            previous_n=merge_n_previous[i]
            inflow=merge_inflows[i]
            outflow=merge_outflows[i]
            merge_n_t.append(previous_n-outflow+inflow)
        self.merge_n_t_table.append(merge_n_t)

        # update the number of current vehicles at the main road
        main_n_t=list()
        for i in range(0, self.main_cell_num):
            previous_n=main_n_previous[i]
            inflow=main_inflows[i]
            outflow=main_outflows[i]
            main_n_t.append(previous_n+inflow-outflow)
        self.main_n_t_table.append(main_n_t)

        if waiting_merge_veh>0:
            self.remaining_waiting=self.waiting_times
        else:
            if self.remaining_waiting>=0:
                self.remaining_waiting-=1
        self.t=t
    def compute_outflow(self):
        outflow=0
        time=0
        for main_n_t in self.main_n_t_table:
           outflow+=main_n_t[-1] 
           time+=self.duration_per_time_step
        avg_outflow=outflow/time
        return avg_outflow

    def compute_inflow(self):
        main_inflow=0
        time=0
        for main_inflow_t in self.main_inflow_n_t_table:
           main_inflow+=main_inflow_t[0] 
           time+=self.duration_per_time_step
        avg_main_inflow=main_inflow/time

        merge_inflow=0
        for merge_n_t in self.merge_n_t_table:
           merge_inflow+=merge_n_t[0] 
        avg_merge_inflow=merge_inflow/time


        return (avg_main_inflow, avg_merge_inflow)

    def simulate(self, main_inflow, merge_inflow, total_time_steps):
        #set_trace()
        if debug:
            print("-------------t=%d--------------" % 0)
            print("main road:", self.main_n_t_table[0])
            print("merge road:", self.merge_n_t_table[0])
        for t in range(1, total_time_steps):
            #set_trace()
            self.step(main_inflow/3600.0, merge_inflow/3600.0)
            if debug:
                print("-------------t=%d--------------" % t)
                print("main road:", self.main_n_t_table[t])
                print("merge road:", self.merge_n_t_table[t])
        avg_outflow=self.compute_outflow() 
        avg_main_inflow, avg_merge_inflow=self.compute_inflow()
        if debug:
            print("outflow (veh/hour):", avg_outflow*3600)
            print("inflow (veh/hour):", avg_main_inflow*3600, avg_merge_inflow*3600)
        return (avg_main_inflow*3600, avg_merge_inflow*3600, avg_outflow*3600)
        #file=open(filename, "w")
        #file.write(content)
        #file.close()

if __name__ == "__main__":
    single_lane_simple_merge=SingleLaneSimpleMerge()
    results=dict()
    for main_inflow in [1400, 1500, 1600, 1700, 1800, 1900, 2000]:
    #for main_inflow in [2000]:
        for merge_inflow in [160, 180, 200]:
        #for merge_inflow in [200]:
            (avg_main_inflow, avg_merge_inflow, avg_outflow)=single_lane_simple_merge.simulate(main_inflow, merge_inflow, 7000)
            results[str(main_inflow)+"-"+str(merge_inflow)]=(avg_main_inflow, avg_merge_inflow, avg_outflow)
            #print(main_inflow, merge_inflow, avg_main_inflow, avg_merge_inflow, avg_outflow)
            print(main_inflow, merge_inflow, avg_outflow)
    #print(results)

    
     


