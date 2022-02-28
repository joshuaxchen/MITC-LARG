import os
from tikz_plot import PlotWriter
from IPython.core.debugger import set_trace

attr_name="Outflow"
def obtain_file_names(folder_path):
    for x in os.walk(folder_path):
        if x[0]==folder_path:
            return x[2]
    return None
def obtain_subfolder_names(folder_path):
    for x in os.walk(folder_path):
        if x[0]==folder_path:
            return x[1]
    return None

# Python implementation to
# read last N lines of a file

# Function to read
# last N lines of the file
def LastNlines(fname, num_of_lines, ignore_last_m_lines):
    # opening file using with() method
    # so that file get closed
    # after completing work
    with open(fname) as file:
            # loop to read iterate
            # last n lines and print it
            last_lines=file.readlines() [-num_of_lines:]
            return last_lines[:-ignore_last_m_lines]
    return None

working_dir=os.path.join("..","exp_results","lc_human_14000") 

def retrive_evaluations_from_ctm(fname):
    results=dict()
    with open(fname) as file:
        lines=file.readlines()
        for line in lines:
            if line.strip()=="":
                continue 

            items=line.split(" ")
            input_spec=items[0].split("-")
            left_main=input_spec[0]
            right_main=input_spec[1]
            merge=input_spec[2]
            outflow=items[-1]
            results[f"{left_main}-{right_main}"]=outflow
    return results
            

def retrive_evaluations(working_dir):
    files=obtain_file_names(working_dir)
    print("working_dir", working_dir)
    model_exp_dict=dict()
    for file_name in files:
        if file_name=='summary.txt' or '.txt' not in file_name :
            continue
        fname=os.path.join(working_dir, file_name)
        data=LastNlines(fname, 6, 2)
        file_name_breakdown=file_name.split(".txt")[0].split("_")
        eval_label=file_name_breakdown[3]+"-"+file_name_breakdown[2]
        #eval_label=main_merge_avp_rlrightleft_righthumanlc_aggressive_text
        exp_summary=dict()
        print(working_dir, file_name)
        for attr_value in data:
            text=attr_value.split(":")
            print(text)
            attr=text[0]
            value=text[1].strip()
            exp_summary[attr]=value
        model_exp_dict[eval_label]=exp_summary
    return model_exp_dict

def extract_mean_var(e_data, attr_name):
    mean_var_list=e_data[attr_name].split(",")
    mean=float(mean_var_list[0].strip())
    var=float(mean_var_list[1].strip())
    return (mean, var)

def read_from_formatted_string(input_str):
    texts=input_str.split("_")
    left_main_inflow=int(texts[0])
    merge_inflow=int(texts[1])
    avp=int(texts[2])
    rl_right_left=int(texts[3])
    right_human_lane_change=int(texts[4])
    aggressive=float(texts[5])
    assertive=float(texts[6])
    lc_prob=float(texts[7])
    #return left_main_inflow, merge_inflow, avp, rl_right_left, right_human_lane_change, aggressive, lc_prob
    return left_main_inflow, avp, rl_right_left, right_human_lane_change, rl_right_left, assertive, lc_prob

rl_configs=["rl_right", "rl_left"]
lc_configs=["nlc","lc"]
def obtain_config(rl_right_left, right_human_lane_change):
    rl_config=rl_configs[rl_right_left]
    lc_config=lc_configs[right_human_lane_change]
    return rl_config, lc_config
     
def obtain_setting_index(settings, rl_right_left, right_human_lane_change):
    for i in range(0, len(settings)):
        (rl, lc)=settings[i]
        if rl==rl_right_left and lc==right_human_lane_change:
            return i
    return None
    
def plot_human_data(sumo_data, ctm_data):
    keys=set(sumo_data.keys())
    keys=keys.intersection(set(ctm_data.keys()))
    keys=list(keys)
    keys.sort()
    print("keys", keys) 
    print("ctm keys", ctm_data.keys()) 
    sumo_fixed_right_flow_dict=dict()
    ctm_fixed_right_flow_dict=dict()
    sumo_data_to_plot=list()
    ctm_data_to_plot=list()
    for left_right_flow in keys:
        sumo_outflow_mean=sumo_data[left_right_flow][attr_name].split(",")[0] 
        sumo_outflow_var=sumo_data[left_right_flow][attr_name].split(",")[1] 
        ctm_outflow=ctm_data[left_right_flow]  
        inflows=left_right_flow.split("-")
        if inflows[1] not in sumo_fixed_right_flow_dict:
            sumo_fixed_right_flow_dict[inflows[1]]=list()
        if inflows[1] not in ctm_fixed_right_flow_dict:
            ctm_fixed_right_flow_dict[inflows[1]]=list()
        left_main_inflow=inflows[0]
        right_main_inflow=inflows[1]
        sumo_fixed_right_flow_dict[right_main_inflow].append((left_main_inflow, sumo_outflow_mean, sumo_outflow_var))
        ctm_fixed_right_flow_dict[right_main_inflow].append((left_main_inflow, ctm_outflow.strip(), 0))
    print("sumo_fixed_right_flow_dict", sumo_fixed_right_flow_dict.keys()) 
    left_inflow_plot=PlotWriter("Left MainInflow", "Outflow") 

    for right_inflow in sumo_fixed_right_flow_dict.keys():
        #print(left_right_flow)
        inflows=left_right_flow.split("-")
        #print(inflows)
        sumo_fixed_right_flow_dict[right_inflow].sort()
        ctm_fixed_right_flow_dict[right_inflow].sort()
        left_inflow_plot.add_plot("sumo_RightInflow"+right_inflow, sumo_fixed_right_flow_dict[right_inflow])
        #left_inflow_plot.add_plot("ctm_RightInflow"+inflows[1],
        #ctm_fixed_right_flow_dict[inflows[1]])

    for right_inflow in ctm_fixed_right_flow_dict.keys():
        #print(left_right_flow)
        inflows=left_right_flow.split("-")
        #print(inflows)
        sumo_fixed_right_flow_dict[right_inflow].sort()
        ctm_fixed_right_flow_dict[right_inflow].sort()
        left_inflow_plot.add_plot("ctm_RightInflow"+right_inflow, ctm_fixed_right_flow_dict[right_inflow])
        #left_inflow_plot.add_plot("ctm_RightInflow"+inflows[1],
        #ctm_fixed_right_flow_dict[inflows[1]])


    left_inflow_plot.write_plot("./plot/human_leftinflow.tex", len(ctm_fixed_right_flow_dict.keys()))
   
        
if __name__ == "__main__":
    # retrive random models and random evaluation
    #random_model_exp_summary=retrieve_special_exp_data(random_aamas_avp_dir) 
    # retrieve special models
    #for preset_i in ["human", "preset_1_dr_light"]:
    sumo_data=retrive_evaluations(working_dir)
    ctm_data=retrive_evaluations_from_ctm("./ctm_results.txt")
    plot_human_data(sumo_data, ctm_data)

    
