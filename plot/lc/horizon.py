import os
from tikz_plot import PlotWriter
from IPython.core.debugger import set_trace

attr_name="outflow"
def obtain_file_names(folder_path):
    for x in os.walk(folder_path):
        if x[0]==folder_path:
            return x[2]
    return None

def parse_file(fname):
    results=dict()
    with open(fname) as file:
        lines=file.readlines()
        for line in lines:
            if line.strip()=="":
                continue
            content=line.split(" ")
            print(content)
            exp_condition=content[0]
            inflow_mean=content[2][:-1]
            inflow_var=content[3][:-1]
            outflow_mean=content[5][:-1]
            outflow_var=content[6][:-1]
            results[exp_condition]=(inflow_mean, inflow_var, outflow_mean, outflow_var)
    return results

def plot_inflow_outflow_against_horizon(data):
    inflow_mean_results=dict()
    outflow_mean_results=dict()
    inflow_var_results=dict()
    outflow_var_results=dict()
    for horizon, summary in data.items():
        for exp_condition, results in summary.items():
            if "human" not in exp_condition:
                continue
            inflow_mean, inflow_var, outflow_mean, outflow_var=results
            if exp_condition not in inflow_mean_results.keys():
                inflow_mean_results[exp_condition]=list()
            if exp_condition not in outflow_mean_results.keys():
                outflow_mean_results[exp_condition]=list()
            if exp_condition not in inflow_var_results.keys():
                inflow_var_results[exp_condition]=list()
            if exp_condition not in outflow_var_results.keys():
                outflow_var_results[exp_condition]=list()
            horizon=int(horizon)
            inflow_mean_results[exp_condition].append((horizon, inflow_mean,0))
            outflow_mean_results[exp_condition].append((horizon, outflow_mean,0))
            inflow_var_results[exp_condition].append((horizon, inflow_var, 0))
            outflow_var_results[exp_condition].append((horizon, outflow_var, 0))

    xlabel="Horizon" 
    inflow_mean_plot=PlotWriter(xlabel, "Mean inflow") 
    outflow_mean_plot=PlotWriter(xlabel, "Mean outflow") 
    inflow_var_plot=PlotWriter(xlabel, "Inflow std") 
    outflow_var_plot=PlotWriter(xlabel, "Outflow std") 
    
    sorted_keys=list(inflow_mean_results.keys())
    sorted_keys.sort()
    for exp_condition in sorted_keys:
        inflow_mean_results[exp_condition].sort()
        inflow_mean_plot.add_plot(exp_condition, inflow_mean_results[exp_condition])
        outflow_mean_results[exp_condition].sort()
        outflow_mean_plot.add_plot(exp_condition, outflow_mean_results[exp_condition])
        inflow_var_results[exp_condition].sort()
        inflow_var_plot.add_plot(exp_condition, inflow_var_results[exp_condition])
        outflow_var_results[exp_condition].sort()
        outflow_var_plot.add_plot(exp_condition, outflow_var_results[exp_condition])

    inflow_mean_plot.write_plot("./fig/inflow_mean.tex", 8)
    outflow_mean_plot.write_plot('./fig/outflow_mean.tex', 8)
    inflow_var_plot.write_plot("./fig/inflow_var.tex", 8)
    outflow_var_plot.write_plot("./fig/outflow_var.tex", 8)
    
            
path_to_log_folder=os.path.join("..","..","exp_shell","evaluate", "log") 
if __name__ == "__main__":
    data=dict()
    file_names=obtain_file_names(path_to_log_folder)
    for fname in file_names:
        horizon=fname.split(".")[0]
        fname=os.path.join(path_to_log_folder, fname)
        data[horizon]=parse_file(fname)
    plot_inflow_outflow_against_horizon(data)
    


