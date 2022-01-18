from tools.tikz_plot import PlotWriter
from IPython.core.debugger import set_trace
main_road_length=700
merge_road_length=200
cell_length=100
num_of_cells_in_main=main_road_length/cell_length
num_of_cells_in_merge=merge_road_length/cell_length
merge_roads=["inflow_merge", "bottom"] # 7 (inflow_merge), 8 (bottom)
main_roads=["inflow_highway", "left", "center"] # cell index: 0 (inflow_highway), 1-5 (left), 6 (center)



def profile_speed_density(vehicle_kernel):
    veh_ids=vehicle_kernel.get_ids()
    vehicle_per_cell=dict()
    for veh_id in veh_ids:
        # check whether it is in the main road or the merge road
        edge=vehicle_kernel.get_edge(veh_id)
        cell_index=-1
        if edge in merge_roads:
            # the vehicle is in the merge road
            cell_index=7
            if edge =="bottom":
                cell_index=8
        elif edge in main_roads:
            cell_index=0
            if edge =="left":
                cell_index=1
                pos=vehicle_kernel.get_position(veh_id)
                #set_trace()
                cell_index+=int(pos//100)
            elif edge =="center":
                cell_index=6
        elif ":" in edge:
            pass
        else:
            raise ValueError('the edge of the vehicle %s is not in main or merge road with edge %s' % (veh_id, edge))
        # add the vehicle to the cell 
        if cell_index not in vehicle_per_cell.keys():
           vehicle_per_cell[cell_index]=list()
        vehicle_per_cell[cell_index].append(veh_id)
    # compute the density and average speed for each cell    
    density_flow_per_cell=dict()
    for cell_index, veh_list in vehicle_per_cell.items():
        avg_speed=0
        num_of_veh=len(veh_list)
        for veh_id in veh_list:
            avg_speed+= vehicle_kernel.get_speed(veh_id)
        avg_speed=avg_speed/num_of_veh
        density=num_of_veh/cell_length # veh/m
        flow=avg_speed*density # veh/s
        density_flow_per_cell[cell_index]=(density, flow)
    return density_flow_per_cell
        
def draw_fundamental_diagrams(file_name, density_flow_per_cell):
    for cell_index, density_flow_list in density_flow_per_cell.items():
        xlabel="density"
        ylabel="flow"
        plot=PlotWriter(xlabel, ylabel)  
        density_flow_list.sort()
        plot.add_plot("data", density_flow_list)
        plot.write_plot(file_name+"_cell"+str(cell_index)+".tex")
        
