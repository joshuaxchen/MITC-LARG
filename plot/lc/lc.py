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

working_dir=os.path.join("..","..","exp_results","deterministic_action_random_lane_change") 


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
        eval_label="_".join(file_name_breakdown[1:])
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
    
def plot_against_left_inflow(summary, left_avp_to_plot, right_avp_to_plot, right_main_inflow_to_plot):
    data_with_left_main=dict()
    for model_key, evaluate in summary.items():
        for eval_label, value in evaluate.items():
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left=eval_label.split("_")[0:5]
            if left_avp_to_plot is not None and avp_left!=left_avp_to_plot:
                continue

            if right_avp_to_plot is not None and avp_right!=right_avp_to_plot:
                continue

            if right_main_inflow_to_plot is not None and right_main_inflow!=right_main_inflow_to_plot:
                continue
            print(value)
            if value is None or len(value.keys())==0:
                set_trace()
            mean, var=extract_mean_var(value, attr_name)
            
            left_key=model_key+"_rightAVP"+avp_right+"_leftAVP"+avp_left+"_rightInflow"+right_main_inflow
            if left_key not in data_with_left_main.keys():
                data_with_left_main[left_key]=list()
            data_with_left_main[left_key].append((left_main_inflow, mean, var))
    
    # find human base line
    for model_key, evaluate in summary.items():
        for eval_label, value in evaluate.items():
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left, assertive=eval_label.split("_")

            if right_main_inflow_to_plot is not None and right_main_inflow!=right_main_inflow_to_plot:
                continue
            if avp_right =="0" and avp_left=="0": # human baseline
                mean, var=extract_mean_var(value, attr_name)

                key="human_"+right_main_inflow
                if key not in data_with_left_main.keys():
                    data_with_left_main[key]=list()
                data_with_left_main[key].append((left_main_inflow, mean, var))
        break 

    left_xlabel="LeftMainInflow" 
    ylabel=attr_name
    left_plot=PlotWriter(left_xlabel, ylabel) 
    for legend, value in data_with_left_main.items():
        data_with_left_main[legend].sort()
        left_plot.add_plot(legend, data_with_left_main[legend])
      
    if left_avp_to_plot is None:
        left_avp_to_plot="*"
    if right_avp_to_plot is None:
        right_avp_to_plot="*"
    if right_main_inflow_to_plot is None:   
        right_main_inflow_to_plot="*"

    left_plot.write_plot("left_main_inflow_%s_%s_%s.tex" % (left_avp_to_plot, right_avp_to_plot, right_main_inflow_to_plot), 1)
 
def plot_against_right_inflow(summary, left_avp_to_plot, right_avp_to_plot, left_main_inflow_to_plot):
    data_with_right_main=dict()
    for model_key, evaluate in summary.items():
        for eval_label, value in evaluate.items():
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left=eval_label.split("_")[0:5]
            if left_avp_to_plot is not None and avp_left!=left_avp_to_plot:
                continue

            if right_avp_to_plot is not None and avp_right!=right_avp_to_plot:
                continue

            if left_main_inflow_to_plot is not None and left_main_inflow!=left_main_inflow_to_plot:
                continue

            mean, var=extract_mean_var(value, attr_name)
            right_key=model_key+"_rightAVP"+avp_right+"_leftAVP"+avp_left+"_leftInflow"+left_main_inflow
            if right_key not in data_with_right_main.keys():
                data_with_right_main[right_key]=list()
            data_with_right_main[right_key].append((right_main_inflow, mean, var))

    # find human base line
    for model_key, evaluate in summary.items():
        for eval_label, value in evaluate.items():
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left=eval_label.split("_")[0:5]

            if left_main_inflow_to_plot is not None and left_main_inflow!=left_main_inflow_to_plot:
                continue
            if avp_right =="0" and avp_left=="0": # human baseline
                mean, var=extract_mean_var(value, attr_name)

                key="human_"+left_main_inflow
                if key not in data_with_right_main.keys():
                    data_with_right_main[key]=list()
                data_with_right_main[key].append((right_main_inflow, mean, var))

        break 

    right_xlabel="RightMainInflow" 
    ylabel=attr_name
    right_plot=PlotWriter(right_xlabel, ylabel) 
    for legend, value in data_with_right_main.items():
        data_with_right_main[legend].sort()
        right_plot.add_plot(legend, data_with_right_main[legend])
          
    if left_avp_to_plot is None:
        left_avp_to_plot="*"
    if right_avp_to_plot is None:
        right_avp_to_plot="*"
    if left_main_inflow_to_plot is None:   
        left_main_inflow_to_plot="*"

    right_plot.write_plot("right_main_inflow_%s_%s_%s.tex" % (left_avp_to_plot, right_avp_to_plot, left_main_inflow_to_plot), 1)
  
def plot_against_right_avp(summary, left_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot):
    data_with_right_avp=dict()
    for model_key, evaluate in summary.items():
        for eval_label, value in evaluate.items():
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left=eval_label.split("_")[0:5]
        
            if left_avp_to_plot is not None and avp_left!=left_avp_to_plot: 
                continue           

            if left_main_inflow_to_plot is not None and left_main_inflow!=left_main_inflow_to_plot:
                continue

            if right_main_inflow_to_plot is not None and right_main_inflow!=right_main_inflow_to_plot:
                continue

            mean, var=extract_mean_var(value, attr_name)

            right_key=model_key+"_leftAVP"+avp_left+"_rightInflow"+right_main_inflow+"_leftInflow"+left_main_inflow
            if right_key not in data_with_right_avp.keys():
                data_with_right_avp[right_key]=list()
            data_with_right_avp[right_key].append((avp_right, mean, var))

    
    right_xlabel="RightAVP" 
    ylabel=attr_name
    right_plot=PlotWriter(right_xlabel, ylabel) 
    for legend, value in data_with_right_avp.items():
        if len(data_with_right_avp[legend])<2:
            continue
        data_with_right_avp[legend].sort()
        right_plot.add_plot(legend, data_with_right_avp[legend])
      
    if left_avp_to_plot is None:
        left_avp_to_plot="*"
    if right_main_inflow_to_plot is None:
        right_main_inflow_to_plot="*"
    if left_main_inflow_to_plot is None:   
        left_main_inflow_to_plot="*"


    right_plot.write_plot("avp_right_%s_%s_%s.tex" % (left_avp_to_plot, left_main_inflow_to_plot, left_main_inflow_to_plot), 1)


def plot_against_left_avp(summary, right_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot):
    data_with_left_avp=dict()
    for model_key, evaluate in summary.items():
        for eval_label, value in evaluate.items():
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left, assertive=eval_label.split("_")
        
            if right_avp_to_plot is not None and avp_right!=right_avp_to_plot: 
                continue
        
            if left_main_inflow_to_plot is not None and left_main_inflow!=left_main_inflow_to_plot:
                continue

            if right_main_inflow_to_plot is not None and right_main_inflow!=right_main_inflow_to_plot:
                continue

            left_key=model_key+"_rightAVP"+avp_right+"_rightInflow"+right_main_inflow+"_leftInflow"+left_main_inflow
            mean, var=extract_mean_var(value, attr_name)
            if left_key not in data_with_left_avp.keys():
                data_with_left_avp[left_key]=list()
            data_with_left_avp[left_key].append((avp_left, mean, var))

    
    left_xlabel="LeftAVP" 
    ylabel=attr_name
    left_plot=PlotWriter(left_xlabel, ylabel) 
    for legend, value in data_with_left_avp.items():
        if len(data_with_left_avp)<2:
            continue
        data_with_left_avp[legend].sort()
        left_plot.add_plot(legend, data_with_left_avp[legend])
      
    if right_avp_to_plot is None:
        right_avp_to_plot="*"
    if left_main_inflow_to_plot is None:   
        left_main_inflow_to_plot="*"
    if right_main_inflow_to_plot is None:   
        right_main_inflow_to_plot="*"

    left_plot.write_plot("avp_left_%s_%s_%s.tex"% (right_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot), 1)

        
if __name__ == "__main__":
    # retrive random models and random evaluation
    #random_model_exp_summary=retrieve_special_exp_data(random_aamas_avp_dir) 
    # retrieve special models
    data=dict()
    #for preset_i in ["human", "preset_1_dr_light"]:
    for setting in ["aamas_right", "aamas_left",
    "av_right", "av_left_on_right", "av_left"]:
        setting_dir=os.path.join(working_dir, setting)
        data_i=retrive_evaluations(setting_dir)
        data[setting]=data_i

    human_baselines=dict()
    for setting, eval_data in data.items():
        for eval_label, eval_value in eval_data.items():
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left=eval_label.split("_")[0:5]
            key=left_main_inflow+setting+"-LeftMainInflow"+left_main_inflow
            if avp_right=="0" and avp_left=="0":
                if key not in human_baselines:
                    human_baselines[key]=list()

                mean, var=extract_mean_var(eval_value, attr_name)
                human_baselines[key].append((right_main_inflow, mean, var)) 
    keys=list(human_baselines.keys())
    keys.sort()
    xlabel="Right Main Inflow" 
    ylabel=attr_name
    plot=PlotWriter(xlabel, ylabel) 
    for key in keys:
        value=human_baselines[key]
        value.sort()
        key=key[4:]
        plot.add_plot(key, value)
    plot.write_plot("human_baselines.tex", 1)

    left_avp_to_plot="0" 
    right_avp_to_plot="10" 
    left_main_inflow_to_plot="1600" 
    right_main_inflow_to_plot="2000" 
    plot_against_right_inflow(data, left_avp_to_plot, right_avp_to_plot, left_main_inflow_to_plot)
    plot_against_right_avp(data, left_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot)


    left_avp_to_plot="10" 
    right_avp_to_plot="0" 
    plot_against_left_inflow(data, left_avp_to_plot, right_avp_to_plot, right_main_inflow_to_plot)
    plot_against_left_avp(data, right_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot)

#plot_against_inflow(summary, left_avp_to_plot, right_avp_to_plot, left_main_inflow_to_plot):
    #plot_against_assertive(data)

