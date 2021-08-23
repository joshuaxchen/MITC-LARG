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

special_random_evaluation_name="special_models_random"
special_even_evaluation_name="special_models_even"
special_evaluation_name="special_models"
special_random_models_dir=os.path.join("..","..","exp_results", special_random_evaluation_name) 
special_even_models_dir=os.path.join("..","..","exp_results", special_even_evaluation_name) 

working_dir=os.path.join("..","..","exp_results","lane_change") 

eval_flows=[1600, 1700, 1800, 1900, 2000, 2100, 2200, 2250, 2300, 2400, 2500, 2600]

def retrive_evaluations(working_dir):
    print(working_dir)
    files=obtain_file_names(working_dir)
    model_exp_dict=dict()
    for file_name in files:
        if file_name=='summary.txt' or '.txt' not in file_name :
            continue
        fname=os.path.join(working_dir, file_name)
        data=LastNlines(fname, 6, 2)
        file_name_breakdown=file_name.split(".")[0].split("_")
        main_merge_avp_rlrightleft_righthumanlc_aggressive_text="_".join(file_name_breakdown[1:])
        eval_label=main_merge_avp_rlrightleft_righthumanlc_aggressive_text
        exp_summary=dict()
        print(working_dir, file_name)
        for attr_value in data:
            text=attr_value.split(":")
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

def sort_model_keys(category_summary):
    model_exp_list=list()
    #print("category_summary keys:", category_summary.keys())
    for model_key, model_eval_value in category_summary.items():
        model_int_label_list=list()
        for label in model_key.split("_"):
            model_int_label_list.append(int(label))
        model_exp_list.append((model_int_label_list[0], \
                model_int_label_list[1], model_int_label_list[2], \
                model_eval_value))
    model_exp_list.sort() 
    # add each model to plot 
    sorted_key_list=list()
    for k1, k2, k3, m in model_exp_list:
        model_key="%d_%d_%d" % (k1, k2, k3)
        sorted_key_list.append(model_key) 
    return sorted_key_list

def extract_sorted_data(model_data):
    sorted_e_data=list()
    for e_key, e_data in model_data.items():
        (mean, var)=extract_mean_var(e_data, attr_name)
        sorted_e_data.append((int(e_key), mean, var)) 
    sorted_e_data.sort()
    return sorted_e_data

def plot_against_aggressive(summary):
    trained_models=summary.keys
    setting_0="0_0" # rl on the right, with human no lane change
    setting_1="0_1" # rl on the right, with human lane change on the right
    setting_2="1_1" # rl on the left, with human change on the right
    setting_3="1_0" # rl on the left, with no human change on the right
    settings=[setting_0, setting_1, setting_2]
    inflow_desc="2000_200_10"
     
    data=[[], [], []]
    for setting in settings:
        for model_key, evaluate in summary.items():
            for eval_label, value in evaluate.items():
                setting_index=int(setting[-1])
                eval_label_to_match=inflow_desc+"_"+setting
                if eval_label_to_match in eval_label:
                    aggressive=float(eval_label.split("_")[-1])
                    mean, var=extract_mean_var(value, attr_name)
                    data[setting_index].append((aggressive, mean, var))

    xlabel="Aggressiveness" 
    ylabel="Outflow" 
    plot=PlotWriter(xlabel, ylabel) 

    for i in range(0, len(data)):
        data[i].sort()
        plot.add_plot("Setting_%d" % i, data[i])
    
    plot.write_plot("setting_aggressiveness.tex", 1)

  
        
if __name__ == "__main__":
    # retrive random models and random evaluation
    #random_model_exp_summary=retrieve_special_exp_data(random_aamas_avp_dir) 
    # retrieve special models
    data=dict()
    for i in [0,1,2]:
        preset_i="preset_%d" % i
        preset_dir=os.path.join(working_dir, preset_i)
        data_i=retrive_evaluations(preset_dir)
        data[preset_i]=data_i

    plot_against_aggressive(data)


