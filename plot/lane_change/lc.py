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

working_dir=os.path.join("..","..","exp_results","lane_change_1") 


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

def plot_against_aggressive(summary):
    trained_models=summary.keys
    setting_0="0_0" # rl on the right, with human no lane change
    setting_1="0_1" # rl on the right, with human lane change on the right
    setting_2="1_1" # rl on the left, with human change on the right
    setting_3="1_0" # rl on the left, with no human change on the right
    settings=[setting_0, setting_1, setting_2]
    inflow_desc="2000_200_10"
     
    data=dict()
    for i in range(0, len(settings)):
        setting=settings[i]
        for model_key, evaluate in summary.items():
            model_index=int(model_key[-1])
            print(i, model_index)
            if i !=model_index:
                continue
            for eval_label, value in evaluate.items():
                print(eval_label)
                for assertive in [0.5, 1]:
                    if eval_label.endswith(str(assertive)):
                        eval_label_to_match=inflow_desc+"_"+setting
                        if eval_label_to_match in eval_label:
                            #print(eval_label_to_match, eval_label)
                            aggressive=float(eval_label.split("_")[-2])
                            assertive=float(eval_label.split("_")[-1])
                            mean, var=extract_mean_var(value, attr_name)
                            legend="Setting_%d_%f" % (i, assertive)
                            if legend not in data.keys():
                                data[legend]=[]
                            data[legend].append((aggressive, mean, var))

    xlabel="Aggressiveness" 
    ylabel="Outflow" 
    plot=PlotWriter(xlabel, ylabel) 
    plot.add_human=False
    for legend, value in data.items():
        data[legend].sort()
        plot.add_plot(legend, data[legend])
    
    plot.write_plot("setting_aggressiveness.tex", 1)

def plot_against_assertive(summary):
    trained_models=summary.keys
    setting_0="0_0" # rl on the right, with human no lane change
    setting_1="0_1" # rl on the right, with human lane change on the right
    setting_2="1_1" # rl on the left, with human change on the right
    setting_3="1_0" # rl on the left, with no human change on the right
    settings=[setting_0, setting_1, setting_2]
    data_inflow_desc="2000_200_10"
    human_inflow_desc="2000_200_0"

    data_legends=["RL_right_human_no_lc", "RL_right_human_lc_to_left", "RL_left_human_lc_to_left"]
    human_legends=["Human_no_lc", "Human_lc_to_left", "Human_lc_to_left"]
     
    data=dict()
    human=dict()
    for i in range(0, len(settings)):
        setting=settings[i]
        for model_key, evaluate in summary.items():
            model_index=int(model_key[-1])
            print(i, model_index)
            if i !=model_index:
                continue
            for eval_label, value in evaluate.items():
                print(eval_label)
                for assertive in [0.1, 0.3, 0.5, 0.7, 0.9, 1]:
                    to_add=None
                    prefix=None
                    legends=None
                    if eval_label.startswith(data_inflow_desc):
                        to_add=data 
                        prefix=data_inflow_desc
                        legends=data_legends
                    else:
                        to_add=human
                        prefix=human_inflow_desc
                        legends=human_legends
                    if eval_label.endswith(str(assertive)):
                        eval_label_to_match=prefix+"_"+setting
                        if eval_label_to_match in eval_label:
                            #print(eval_label_to_match, eval_label)
                            aggressive=float(eval_label.split("_")[-2])
                            assertive=float(eval_label.split("_")[-1])
                            mean, var=extract_mean_var(value, attr_name)
                            legend=legends[i]
                            if legend not in to_add.keys():
                                to_add[legend]=[]
                            to_add[legend].append((assertive, mean, var))

    xlabel="Assertative" 
    ylabel=attr_name
    plot=PlotWriter(xlabel, ylabel) 
    plot.add_human=False
    for legend, value in data.items():
        data[legend].sort()
        plot.add_plot(legend, data[legend])
    for legend, value in human.items():
        human[legend].sort()
        plot.add_plot(legend, human[legend])

    plot.write_plot("setting_assertiveness.tex", 1)

 
        
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
    plot_against_assertive(data)

