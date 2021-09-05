import os
from tikz_plot import PlotWriter
attr_name="Inflow"
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

working_dir=os.path.join("..","..","exp_results","lane_change_5") 


def retrive_evaluations(working_dir):
    files=obtain_file_names(working_dir)
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
    data=dict()
    for model_key, evaluate in summary.items():
        for eval_label, value in evaluate.items():
            print(eval_label)
            left_main_inflow, avp, rl_right_left, right_human_lane_change, rl_right_left, assertive, lc_prob=read_from_formatted_string(eval_label)
            rl_config, lc_config=obtain_config(rl_right_left, right_human_lane_change)                
            legend=rl_config+"_"+lc_config

            mean, var=extract_mean_var(value, attr_name)
            key=model_key+"_"+legend+"_%.1f" % (assertive)
            if key not in data.keys():
                data[key]=list()
            data[key].append((left_main_inflow, mean, var))

        xlabel="Left-Inflow" 
        ylabel=attr_name
        right_plot=PlotWriter(xlabel, ylabel) 
        left_plot=PlotWriter(xlabel, ylabel) 
        right_plot.add_human=False
        left_plot.add_human=False
        for legend, value in data.items():
            data[legend].sort()
            if "right" in legend:
                right_plot.add_plot(legend, data[legend])
            else:
                left_plot.add_plot(legend, data[legend])
                
       
        right_plot.write_plot("%s_inflow_right.tex" % model_key, 1)
        left_plot.write_plot("%s_inflow_left.tex" % model_key, 1)

  
    
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
    for preset_i in ["human"]:
        preset_dir=os.path.join(working_dir, preset_i)
        data_i=retrive_evaluations(preset_dir)
        data[preset_i]=data_i
    
    plot_against_inflow(data)
    #plot_against_assertive(data)

