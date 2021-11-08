import os
from tikz_plot import PlotWriter
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

working_dir=os.path.join("..","..","exp_results","lane_change") 


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
    
def plot_against_inflow(summary):
    data_with_right_main=dict()
    data_with_left_main=dict()
    for model_key, evaluate in summary.items():
        for eval_label, value in evaluate.items():
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left, assertive=eval_label.split("_")
            mean, var=extract_mean_var(value, attr_name)
            right_key=model_key+"_"+avp_right+"_"+avp_left+"_"+left_main_inflow
            if right_key not in data_with_right_main.keys():
                data_with_right_main[right_key]=list()
            data_with_right_main[right_key].append((right_main_inflow, mean, var))

            left_key=model_key+"_"+avp_right+"_"+avp_left+"_"+right_main_inflow
            if left_key not in data_with_left_main.keys():
                data_with_left_main[left_key]=list()
            data_with_left_main[left_key].append((left_main_inflow, mean, var))
    
    right_xlabel="RightMainInflow" 
    left_xlabel="LeftMainInflow" 
    ylabel=attr_name
    right_plot=PlotWriter(right_xlabel, ylabel) 
    left_plot=PlotWriter(left_xlabel, ylabel) 
    for legend, value in data_with_right_main.items():
        data_with_right_main[legend].sort()
        right_plot.add_plot(legend, data_with_right_main[legend])
    for legend, value in data_with_left_main.items():
        data_with_left_main[legend].sort()
        left_plot.add_plot(legend, data_with_left_main[legend])
      
   
    right_plot.write_plot("inflow_right.tex", 1)
    left_plot.write_plot("inflow_left.tex", 1)

def plot_against_avp(summary):
    data_with_right_avp=dict()
    data_with_left_avp=dict()
    for model_key, evaluate in summary.items():
        for eval_label, value in evaluate.items():
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left, assertive=eval_label.split("_")
            mean, var=extract_mean_var(value, attr_name)
            right_key=model_key+"_"+avp_right+"_"+avp_left+"_"+left_main_inflow
            if right_key not in data_with_right_avp.keys():
                data_with_right_avp[right_key]=list()
            data_with_right_avp[right_key].append((right_main_inflow, mean, var))

            left_key=model_key+"_"+avp_right+"_"+avp_left+"_"+right_main_inflow
            if left_key not in data_with_left_avp.keys():
                data_with_left_avp[left_key]=list()
            data_with_left_avp[left_key].append((left_main_inflow, mean, var))
    
    right_xlabel="RightAVP" 
    left_xlabel="LeftAVP" 
    ylabel=attr_name
    right_plot=PlotWriter(right_xlabel, ylabel) 
    left_plot=PlotWriter(left_xlabel, ylabel) 
    for legend, value in data_with_right_avp.items():
        data_with_right_avp[legend].sort()
        right_plot.add_plot(legend, data_with_right_avp[legend])
    for legend, value in data_with_left_avp.items():
        data_with_left_avp[legend].sort()
        left_plot.add_plot(legend, data_with_left_avp[legend])
      
   
    right_plot.write_plot("avp_right.tex", 1)
    left_plot.write_plot("avp_left.tex", 1)

   
def plot_against_aggressive(summary):
    trained_models=summary.keys
    
    setting_0="0_0" # rl on the right, with human no lane change
    setting_1="0_1" # rl on the right, with human lane change on the right
    setting_2="1_1" # rl on the left, with human change on the right
    setting_3="1_0" # rl on the left, with no human change on the right
    settings=[(0,0), (0,1), (1,1)]
    inflow_desc="2000_200_10"

    human=dict()
    preset_1=dict()
    preset_2=dict()
    for model_key, evaluate in summary.items():
        model_index=model_key[-1]
        data=None
        if "human" in model_key:
            data=human
        elif "1" in model_key:
            data=preset_1
        elif "2" in model_key:
            data=preset_2

        for eval_label, value in evaluate.items():
            left_main_inflow, avp, rl_right_left, right_human_lane_change, rl_right_left, assertive, lc_prob=read_from_formatted_string(eval_label)
            if "human" in model_key and avp!=0:
                continue
            if "human" not in model_key and avp!=10:
                continue
                
            eval_setting_index=obtain_setting_index(settings, rl_right_left, right_human_lane_change)

            mean, var=extract_mean_var(value, attr_name)
            key="L%d_%d_%d" % (left_main_inflow, rl_right_left, right_human_lane_change)
            if key not in data.keys():
                data[key]=list()
            data[key].append((lc_prob, mean, var))
    i=1
    for data in [preset_1, preset_2]:
        xlabel="LC-prob" 
        ylabel=attr_name
        plot=PlotWriter(xlabel, ylabel) 
        plot.add_human=False
        for legend, value in data.items():
            data[legend].sort()
            plot.add_plot(legend, data[legend])
        for legend, value in human.items():
            human[legend].sort()
            plot.add_plot("human_"+legend, human[legend])
        
        plot.write_plot("setting_aggressiveness_%s.tex" % i, 6)
        i+=1

        
if __name__ == "__main__":
    # retrive random models and random evaluation
    #random_model_exp_summary=retrieve_special_exp_data(random_aamas_avp_dir) 
    # retrieve special models
    data=dict()
    #for preset_i in ["human", "preset_1_dr_light"]:
    for setting in ["aamas_right", "aamas_left", "av_right", "av_left"]:
        setting_dir=os.path.join(working_dir, setting)
        data_i=retrive_evaluations(setting_dir)
        data[setting]=data_i

    human_baselines=dict()
    for setting, eval_data in data.items():
        for eval_label, eval_value in eval_data.items():
            labels=eval_label.split("_") 
            right_avp=int(labels[2])
            left_avp=int(labels[3])
            main_inflow=int(labels[0])
            if right_avp==0 and left_avp==0:
                if setting not in human_baselines:
                    human_baselines[setting]=list()

                mean, var=extract_mean_var(eval_value, attr_name)
                human_baselines[setting].append((main_inflow, mean, var)) 

    plot_against_inflow(data)
    plot_against_avp(data)

    #plot_against_assertive(data)

