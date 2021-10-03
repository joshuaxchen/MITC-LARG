import os
from tikz_plot import PlotWriter
attr_name="Outflow"
random_human_only=True

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


special_random_evaluation_name="randomness_maininflow"
special_random_models_dir=os.path.join("..","..","exp_results", special_random_evaluation_name) 

evaluation_name="random_evaluation"
aamas_avp_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models")
random_aamas_avp_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_random")
aamas_inflows_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_inflows")
random_aamas_inflows_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_random_inflow")

results_dict={
"avp": aamas_avp_dir,
"inflow": aamas_inflows_dir,
"avp_random": random_aamas_avp_dir,
"inflow_random": random_aamas_inflows_dir,
}

eval_flows=[1600, 1700, 1800, 1900, 2000, 2100, 2200, 2250, 2300, 2400, 2500, 2600]

def retrieve_special_exp_data(working_dir):
    # print(working_dir)
    exp_folder_name_list=obtain_subfolder_names(working_dir)
    files_in_each_folder=dict()
    model_exp_dict=dict()
    for folder_name in exp_folder_name_list:
        if "bk" not in folder_name:
            continue
        folder_path=os.path.join(working_dir, folder_name)
        files_in_each_folder[folder_name]=obtain_file_names(folder_path)
        model_exp_dict[folder_name]=dict()
        for file_name in files_in_each_folder[folder_name]:
            if file_name=='summary.txt':
                continue
            fname=os.path.join(folder_path, file_name)
            data=LastNlines(fname, 6, 2)
            specs_list=fname.split("_")[1:]
            eval_label="_".join(specs_list)
            eval_label=eval_label.split(".")[0]
            exp_summary=dict()
            print(working_dir, folder_name, file_name, eval_label)
            exit(0)
            for attr_value in data:
                text=attr_value.split(":")
                attr=text[0]
                value=text[1].strip()
                exp_summary[attr]=value
            model_exp_dict[folder_name][eval_label]=exp_summary
    return model_exp_dict

   
def retrieve_exp_data(working_dir):
    exp_folder_name_list=obtain_subfolder_names(working_dir)
    files_in_each_folder=dict()
    model_exp_dict=dict()
    for folder_name in exp_folder_name_list:
        if "bk" not in folder_name:
            continue
        folder_path=os.path.join(working_dir, folder_name)
        files_in_each_folder[folder_name]=obtain_file_names(folder_path)
        model_exp_dict[folder_name]=dict()
        for file_name in files_in_each_folder[folder_name]:
            if ".txt" not in file_name:
                continue
            if file_name=='summary.txt':
                continue
            fname=os.path.join(folder_path, file_name)
            exp_summary=retrive_flow_data(fname, attr_name)
            try:
                EVA_index=file_name.index("EAVL")
            except:
                EVA_index=file_name.index("_EVA")
            eval_text=file_name.split(".")[0][EVA_index+1:].split("_")[1:]
            eval_label="_".join(eval_text)
            print(eval_label)
            model_exp_dict[folder_name][eval_label]=exp_summary
    return model_exp_dict

def retrive_flow_data(fname, attr_name):
    data=LastNlines(fname, 6, 2)
    exp_summary=dict()
    for attr_value in data:
        text=attr_value.split(":")
        attr=text[0]
        value=text[1].strip()
        exp_summary[attr]=value
    return exp_summary

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

def find_best_training_avp_against_randomness(summary):
    data_map=dict()
    for model_key, model_data in summary.items():
        trained_labels=model_key.split("_")
        trained_avp=trained_labels[2]
        for eval_label, eval_value in model_data.items():
            print(eval_label)
            labels=eval_label.split("_")
            flow_str=labels[0]
            avp_str=labels[2]
            randomness_str=labels[-1]
            legend_label=model_key[3:]+"_"+avp_str
            if legend_label not in data_map.keys():
                data_map[legend_label]=list()
            mean_var_list=eval_value[attr_name].split(",")
            mean=float(mean_var_list[0].strip())
            var=float(mean_var_list[1].strip())
            data_map[legend_label].append((int(randomness_str), mean, var))
    
    xlabel="Evaluated randomness" 
    ylabel=attr_name #"Outflow" 
    plot=PlotWriter(xlabel, ylabel) 
    #print(data_map.keys())
    legend_prefix="random_"
    for legend_label, data in data_map.items(): 
    #for model_key, model_data in summary.items():
        #for flow in [1600, 1700, 1800, 1900, 2000]:
        data.sort()
        legend_label1=legend_prefix+legend_label
        plot.add_plot(legend_label1, data)
    plot.write_plot("./aamas/"+"maininflow_randomness.tex",5)

 
if __name__ == "__main__":
    # retrive random models and random evaluation
    #random_model_exp_summary=retrieve_special_exp_data(random_aamas_avp_dir) 
    # retrieve special models
    special_random_summary=retrieve_exp_data(special_random_models_dir)
    #model_key="2000_200_30"
    #plot_special_model_flow(model_key, special_random_summary[model_key])
    find_best_training_avp_against_randomness(special_random_summary)

    #special_even_summary=retrieve_special_exp_data(special_even_models_dir)

    #plot_special_model_av(special_random_summary)
    #plot_special_model_flow(special_random_summary)
    ## data to add 2000_200_30
    ## add to the special models
    #for model_key, model_value in random_model_exp_summary.items():
    #    if model_key not in special_random_summary.keys():
    #        special_random_summary[model_key]=model_value 
    #        print("added", model_key)
    #extra_data_random_eval=special_random_summary


    ## print(extra_data)
    #retrieve_all_data_and_plot(extra_data_random_eval, "random_eval")
    ##retrieve_all_data_and_plot(special_even_summary, "even_eval")
    #plot_special_random_even_models(special_random_summary, special_even_summary)


