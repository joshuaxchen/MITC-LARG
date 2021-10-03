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
    main_inflow=int(texts[0])
    merge_inflow=int(texts[1])
    avp=int(texts[2])
    randomness=int(texts[3])
    #rl_right_left=int(texts[3])
    #right_human_lane_change=int(texts[4])
    #aggressive=float(texts[5])
    #assertive=float(texts[6])
    #lc_prob=float(texts[7])
    #return left_main_inflow, merge_inflow, avp, rl_right_left, right_human_lane_change, aggressive, lc_prob
    return main_inflow, merge_inflow, avp, randomness

    
def obtain_setting_index(settings, rl_right_left, right_human_lane_change):
    for i in range(0, len(settings)):
        (rl, lc)=settings[i]
        if rl==rl_right_left and lc==right_human_lane_change:
            return i
    return None
    
def plot_against_randomness(summary):
    data=dict()
    for model_key, evaluate in summary.items():
        for eval_label, value in evaluate.items():
            print(eval_label)
            main_inflow, merge_inflow, avp, randomness=read_from_formatted_string(eval_label)

            mean, var=extract_mean_var(value, attr_name)
            if avp==0:
                key="human"
            else:
                key=model_key
            if key not in data.keys():
                data[key]=list()
            data[key].append((randomness, mean, var))

    xlabel="Randomness (percentage)" 
    ylabel=attr_name
    plot=PlotWriter(xlabel, ylabel) 
    plot.add_human=False
    for legend, value in data.items():
        data[legend].sort()
        plot.add_plot(legend, data[legend])
            
    plot.write_plot("random_merge_randomness.tex", 1)

    
        
if __name__ == "__main__":
    # retrive random models and random evaluation
    #random_model_exp_summary=retrieve_special_exp_data(random_aamas_avp_dir) 
    # retrieve special models
    data=dict()
    #for preset_i in ["human", "preset_1_dr_light"]:

    working_dir=os.path.join("..","..","exp_results","random_merge") #"window_size")#"random_merge") 
    for preset_i in ["2000_200_30"]:
    #for preset_i in ["modified_state_three_merge_2000_300_30_random_merge","modified_state_three_merge_2000_200_30_random_merge"]:
    #for preset_i in ["three_merge_2000_200_30_random_merge", "modified_state_three_merge_2000_200_30_random_merge"]:
    #for preset_i in ["2000_200_30_even_merge", "2000_200_30_random_merge"]:
        preset_dir=os.path.join(working_dir, preset_i)
        data_i=retrive_evaluations(preset_dir)
        data[preset_i]=data_i
    
    plot_against_randomness(data)
    #plot_against_assertive(data)

