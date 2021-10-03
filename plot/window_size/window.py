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

working_dir=os.path.join("..","..","exp_results","window_size") 


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
    window_size=int(texts[3])
    #return left_main_inflow, merge_inflow, avp, rl_right_left, right_human_lane_change, aggressive, lc_prob
    return main_inflow, merge_inflow, avp, window_size 

    
   
def plot_against_window(summary):
    data=dict()
    for model_key, evaluate in summary.items():
        human_data=None
        window_sizes=list()
        no_window_data=None
        for eval_label, value in evaluate.items():
            print(eval_label)
            main_inflow, merge_inflow, avp, window_size=read_from_formatted_string(eval_label)
            mean, var=extract_mean_var(value, attr_name)
            if avp==0:
                human_data=(mean, var)
                continue
            if window_size==-1:
                no_window_data=(mean, var)
                continue

            key=model_key
            if window_size==-1:
                key=key+"_no_window"
            if key not in data.keys():
                data[key]=list()
            data[key].append((window_size, mean, var))
            window_sizes.append(window_size)

        window_sizes.sort()
           
        xlabel="Window size" 
        ylabel=attr_name
        plot=PlotWriter(xlabel, ylabel) 
        plot.add_human=False
        for legend, value in data.items():
            data[legend].sort()
            plot.add_plot(legend, data[legend])

        if human_data is not None:
            print("human_data", human_data)
            human=list()
            for window_size in window_sizes:
                human.append((window_size, human_data[0], human_data[1]))    
            plot.add_plot("human", human)

        if no_window_data is not None:
            print("no_window_data", no_window_data)
            no_window=list()
            for window_size in window_sizes:
                no_window.append((window_size, no_window_data[0], no_window_data[1]))    
            plot.add_plot("no_window", no_window)

        plot.write_plot("window.tex", 1)

    
        
if __name__ == "__main__":
    # retrive random models and random evaluation
    #random_model_exp_summary=retrieve_special_exp_data(random_aamas_avp_dir) 
    # retrieve special models
    data=dict()
    #for preset_i in ["human", "preset_1_dr_light"]:
    for preset_i in ["long_merge"]:
        preset_dir=os.path.join(working_dir, preset_i)
        data_i=retrive_evaluations(preset_dir)
        data[preset_i]=data_i
    
    plot_against_window(data)
    #plot_against_assertive(data)

