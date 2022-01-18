import os
from tikz_plot import PlotWriter
from IPython.core.debugger import set_trace
attr_name="Speed"
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

evaluation_name="even_evaluation"
even_evaluation_aamas_avp_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models")
even_evaluation_random_aamas_avp_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_random")
even_evaluation_aamas_inflows_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_inflows")
even_evaluation_random_aamas_inflows_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_random_inflow")

human_dir=os.path.join("..","..","exp_results", "human_baselines")
even_evaluation_human_inflows_dir=os.path.join("..","..","exp_results", "even_human_baseline")
random_evaluation_human_inflows_dir=os.path.join("..","..","exp_results", "random_human_baseline")

even_evaluation_results_dict={
"avp": even_evaluation_aamas_avp_dir,
"inflow": even_evaluation_aamas_inflows_dir,
"avp_random": even_evaluation_random_aamas_avp_dir,
"inflow_random": even_evaluation_random_aamas_inflows_dir,
}

evaluation_name="random_evaluation"
random_evaluation_aamas_avp_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models")
random_evaluation_random_aamas_avp_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_random")
random_evaluation_aamas_inflows_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_inflows")
random_evaluation_random_aamas_inflows_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_random_inflow")

random_evaluation_results_dict={
"avp": random_evaluation_aamas_avp_dir,
"inflow": random_evaluation_aamas_inflows_dir,
"avp_random": random_evaluation_random_aamas_avp_dir,
"inflow_random": random_evaluation_random_aamas_inflows_dir,
}   

small_inflow_data_dict={
"special_even_models_even_eval": os.path.join("..","..","exp_results", "special_even_models_even_eval_ijcai"),
"special_even_models_random_eval": os.path.join("..","..","exp_results", "special_even_models_random_eval_ijcai"),
"special_random_models_even_eval": os.path.join("..","..","exp_results", "special_random_models_even_eval_ijcai"),
"special_random_models_random_eval": os.path.join("..","..","exp_results", "special_random_models_random_eval_ijcai"),
"human_even": os.path.join("..","..","exp_results","special_human_even_eval_ijcai"),
"human_random": os.path.join("..","..","exp_results","special_human_random_eval_ijcai")
}
def retrieve_exp_data(working_dir):
    exp_folder_name_list=obtain_subfolder_names(working_dir)
    files_in_each_folder=dict()
    model_exp_dict=dict()
    for folder_name in exp_folder_name_list:
        folder_path=os.path.join(working_dir, folder_name)
        files_in_each_folder[folder_name]=obtain_file_names(folder_path)
        model_exp_dict[folder_name]=dict()
        for file_name in files_in_each_folder[folder_name]:
            if file_name=='summary.txt':
                continue
            fname=os.path.join(folder_path, file_name)
            data=LastNlines(fname, 6, 2)
            try:
                EVA_index=fname.index("_EAV")
            except:
                EVA_index=fname.index("_EVA")
            eval_text=fname[EVA_index+1:].split("_")[1]
            eval_label=eval_text.split(".")[0]
            exp_summary=dict()
            for attr_value in data:
                text=attr_value.split(":")
                attr=text[0]
                value=text[1].strip()
                exp_summary[attr]=value
            model_exp_dict[folder_name][eval_label]=exp_summary
    return model_exp_dict

def sort_model_keys(category_summary):
    model_exp_list=list()
    print("category_summary keys:", category_summary.keys())
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
        mean_var_list=e_data[attr_name].split(",")
        mean=float(mean_var_list[0].strip())
        var=float(mean_var_list[1].strip())
        sorted_e_data.append((int(e_key), mean, var)) 
    sorted_e_data.sort()
    return sorted_e_data


def compare_av_placement(summary, human, evaluation_key="even_evalution", inflows_keys=["1650", "1850", "2000"]):
    # extract aamas without random 
    sorted_model_keys=sort_model_keys(summary['avp'])
    eval_inflow=inflows_keys[0]
    star_text="*"
    for inflow in inflows_keys:
        ylabel=attr_name
        avp_plot=PlotWriter("Evaluated AVP", ylabel) 
        inflow_plot=PlotWriter("Evaluated Main Inflow", ylabel) 
        if attr_name=="Speed":
            inflow_plot.set_plot_range(1200, 2000, 5, 21)
            avp_plot.set_plot_range(0, 40, 5, 21)
        elif attr_name=="Outflow":
            inflow_plot.set_plot_range(1200, 2000, 1200, 1850)
            avp_plot.set_plot_range(0, 40, 1500, 1850)


        # add even placement data
        even_label_prefix="even_"
        for model_key in sorted_model_keys:
            if not model_key.startswith(inflow):
                continue

            avp_str=model_key.split("_")[-1]
            avp_aamas_summary=summary['avp']
            sorted_e_data=extract_sorted_data(avp_aamas_summary[model_key])
            legend=even_label_prefix+model_key+":"+eval_inflow+"-"+star_text
            avp_plot.add_plot(legend, sorted_e_data)

            inflow_aamas_summary=summary['inflow']
            sorted_e_data=extract_sorted_data(inflow_aamas_summary[model_key])
            legend=even_label_prefix+model_key+":"+star_text+"-"+avp_str
            inflow_plot.add_plot(legend, sorted_e_data)

        # add random placement data
        random_label_prefix="random_"
        for model_key in sorted_model_keys:
            if not model_key.startswith(inflow):
                continue
            avp_str=model_key.split("_")[-1]
            avp_random_summary=summary['avp_random']
            sorted_e_data=extract_sorted_data(avp_random_summary[model_key])
            legend=random_label_prefix+model_key+":"+eval_inflow+"-"+star_text
            avp_plot.add_plot(legend, sorted_e_data)

            inflow_random_summary=summary['inflow_random']
            sorted_e_data=extract_sorted_data(inflow_random_summary[model_key])
            legend=random_label_prefix+model_key+":"+star_text+"-"+avp_str
            inflow_plot.add_plot(legend, sorted_e_data)

        avp_plot.add_human=True
        inflow_plot.add_human=False
        key_list=list()
        for key, value in human.items():
            key_list.append(int(key)) 
        key_list.sort()
        sorted_e_data=list()
        for e_key in key_list:
            mean_var_list=human[str(e_key)][attr_name].split(",")
            mean=float(mean_var_list[0].strip())
            var=float(mean_var_list[1].strip())
            sorted_e_data.append((int(e_key), mean, var)) 
        if "even" in evaluation_key:
            inflow_plot.set_title("Training: even or random vehicle placement, main inflow 2000, train and evaluate at the same AVP,\\\\ Evaluation: \\textbf{even} vehicle placement, main inflow= [1200, 2000]") 
        else:
            inflow_plot.set_title("Training: even or random vehicle placement, main inflow 2000, train and evaluate at the same AVP,\\\\ Evaluating: \\textbf{random} vehicle placement, main inflow= [1200, 2000]")
        inflow_plot.add_plot("human_baseline", sorted_e_data)

        avp_plot.write_plot("./aamas/"+evaluation_key+"_placement_avp_"+inflow+"_{}.tex".format(attr_name), 5, color_same=True)
        inflow_plot.write_plot("./aamas/"+evaluation_key+"_placement_inflow_"+inflow+"_{}.tex".format(attr_name), 5, color_same=True)

def compare_inflow_training(summary, evaluation_key="even_evalution", inflows_keys=["1650", "1850", "2000"]):
    # extract aamas without random 
    sorted_model_keys=sort_model_keys(summary['avp'])
    ylabel=attr_name
    avp_plot=PlotWriter("Evaluated AVP", ylabel) 
    inflow_plot=PlotWriter("Evaluated Main Inflow", ylabel) 
    avp_plot.add_human=False
    inflow_plot.add_human=False
    if attr_name=="Speed":
        inflow_plot.set_plot_range(1600, 2000, 5, 21)
    elif attr_name=="Outflow":
        inflow_plot.set_plot_range(1600, 2000, 1500, 1850)



    for inflow in inflows_keys:
        # add random placement data
        random_label_prefix="random_"
        for model_key in sorted_model_keys:
            if not model_key.startswith(inflow):
                continue

            avp_random_summary=summary['avp_random']
            sorted_e_data=extract_sorted_data(avp_random_summary[model_key])
            avp_plot.add_plot(random_label_prefix+model_key, sorted_e_data)

            inflow_random_summary=summary['inflow_random']
            sorted_e_data=extract_sorted_data(inflow_random_summary[model_key])
            inflow_plot.add_plot(random_label_prefix+model_key, sorted_e_data)

                    
    avp_plot.write_plot("./aamas/"+evaluation_key+"_inflow_avp_"+inflow+".tex", 5)
    inflow_plot.write_plot("./aamas/"+evaluation_key+"_inflow_inflow_"+inflow+".tex", 5)


def plot_each_inflow_each_category(summary):
    for category, category_summary in summary.items():  
        # sort by model number
        sorted_key_list=sort_model_keys(category_summary)
        xlabel="" 
        ylabel=attr_name
        if category.startswith("avp"):
            xlabel="Evaluated AVP" 
        else:
            xlabel="Evaluated Main Inflow"
        label_prefix=""
        if category.endswith("random"):
            label_prefix="random_"

        plot_1650=PlotWriter(xlabel, ylabel) 
        plot_1850=PlotWriter(xlabel, ylabel) 
        plot_2000=PlotWriter(xlabel, ylabel) 
        for model_key in sorted_key_list:
            if model_key.split("_")[0]=="1650":
                # add each model to plot 
                sorted_e_data=list()
                for e_key, e_data in category_summary[model_key].items():
                    mean_var_list=e_data[attr_name].split(",")
                    mean=float(mean_var_list[0].strip())
                    var=float(mean_var_list[1].strip())
                    sorted_e_data.append((int(e_key), mean, var)) 
                sorted_e_data.sort()
                plot_1650.add_plot(label_prefix+model_key, sorted_e_data)
                #print(model_key, sorted_e_data)
            if model_key.split("_")[0]=="1850":
                # add each model to plot 
                sorted_e_data=list()
                for e_key, e_data in category_summary[model_key].items():
                    mean_var_list=e_data[attr_name].split(",")
                    mean=float(mean_var_list[0].strip())
                    var=float(mean_var_list[1].strip())
                    sorted_e_data.append((int(e_key), mean, var)) 
                sorted_e_data.sort()
                plot_1850.add_plot(label_prefix+model_key, sorted_e_data)
                #print(model_key, sorted_e_data)
            if model_key.split("_")[0]=="2000":
                # add each model to plot 
                sorted_e_data=list()
                for e_key, e_data in category_summary[model_key].items():
                    mean_var_list=e_data[attr_name].split(",")
                    mean=float(mean_var_list[0].strip())
                    var=float(mean_var_list[1].strip())
                    sorted_e_data.append((int(e_key), mean, var)) 
                sorted_e_data.sort()
                plot_2000.add_plot(label_prefix+model_key, sorted_e_data)
                #print(model_key, sorted_e_data)
        plot_1650.write_plot(evaluation_name+"/"+category+"_1650.tex", 1)
        plot_1850.write_plot(evaluation_name+"/"+category+"_1850.tex", 1)
        plot_2000.write_plot(evaluation_name+"/"+category+"_2000.tex", 1)

def plot_each_category(summary):
    for category, category_summary in summary.items():  
        # sort by model number
        sorted_key_list=sort_model_keys(category_summary)
        xlabel="" 
        ylabel=attr_name
        if category.startswith("avp"):
            xlabel="Evaluated AVP" 
        else:
            xlabel="Evaluated Main Inflow"
        label_prefix=""
        if category.endswith("random"):
            label_prefix="random_"

        plot=PlotWriter(xlabel, ylabel) 
        for model_key in sorted_key_list:
            # add each model to plot 
            sorted_e_data=list()
            for e_key, e_data in category_summary[model_key].items():
                print(category, model_key, e_key, e_data)
                mean_var_list=e_data[attr_name].split(",")
                mean=float(mean_var_list[0].strip())
                var=float(mean_var_list[1].strip())
                sorted_e_data.append((int(e_key), mean, var)) 
            sorted_e_data.sort()
            plot.add_plot(label_prefix+model_key, sorted_e_data)
            #print(model_key, sorted_e_data)
        plot.write_plot(evaluation_name+"/"+category+".tex", 1)

def retrieve_special_exp_data(working_dir):
    # print(working_dir)
    exp_folder_name_list=obtain_subfolder_names(working_dir)
    files_in_each_folder=dict()
    model_exp_dict=dict()
    for folder_name in exp_folder_name_list:
        if folder_name.startswith("bk"):
            continue
        folder_path=os.path.join(working_dir, folder_name)
        files_in_each_folder[folder_name]=obtain_file_names(folder_path)
        model_exp_dict[folder_name]=dict()
        for file_name in files_in_each_folder[folder_name]:
            if file_name=='summary.txt':
                continue
            if "_200_" not in file_name:
                continue
            fname=os.path.join(folder_path, file_name)
            data=LastNlines(fname, 6, 2)
            file_name_breakdown=file_name.split("_")
            length=len(file_name_breakdown)
            if length==5:# special models
                try:
                    EVA_index=fname.index("_EAV")
                except:
                    EVA_index=fname.index("_EVA")
                specs_list=fname[EVA_index+1:].split("_")
                inflow_text=specs_list[1]
                avp_text=specs_list[3].split(".")[0]
            elif length==6: # random evaluation
                inflow_text=file_name_breakdown[1] 
                avp_text=file_name_breakdown[-1].split(".")[0]
            eval_label=inflow_text+"_"+avp_text
            exp_summary=dict()
            #print(working_dir, folder_name, file_name)
            for attr_value in data:
                text=attr_value.split(":")
                attr=text[0]
                value=text[1].strip()
                exp_summary[attr]=value
            model_exp_dict[folder_name][eval_label]=exp_summary
    return model_exp_dict


def retrieve_all_data_and_plot():
    even_evaluation_summary=dict()
    for category, working_dir in even_evaluation_results_dict.items():
        model_exp_summary=retrieve_exp_data(working_dir) 
        even_evaluation_summary[category]=model_exp_summary

    random_evaluation_summary=dict()
    for category, working_dir in random_evaluation_results_dict.items():
        model_exp_summary=retrieve_exp_data(working_dir) 
        random_evaluation_summary[category]=model_exp_summary

    # retrieve small inflows
    small_inflows_special_even_models_even_eval=retrieve_special_exp_data(small_inflow_data_dict["special_even_models_even_eval"])
    small_inflows_special_random_models_even_eval=retrieve_special_exp_data(small_inflow_data_dict["special_random_models_even_eval"])

    # merge small inflows to even evaluation across inflows on even model
    for model, eval_dict in even_evaluation_summary['inflow'].items(): # even model
        avp=model.split("_")[-1]
        for flow_avp, dict_value in small_inflows_special_even_models_even_eval[model].items():
            flow_avp_list=flow_avp.split("_")
            small_avp = flow_avp_list[-1]
            flow=flow_avp_list[0]
            if avp!=small_avp:
                continue
            even_evaluation_summary['inflow'][model][flow]=dict_value
    # merge small inflows to even evaluation across inflows on random model
    for model, eval_dict in even_evaluation_summary['inflow_random'].items(): # random model
        avp=model.split("_")[-1]
        for flow_avp, dict_value in small_inflows_special_random_models_even_eval[model].items():
            flow_avp_list=flow_avp.split("_")
            small_avp = flow_avp_list[-1]
            flow=flow_avp_list[0]
            if avp!=small_avp:
                continue
            even_evaluation_summary['inflow_random'][model][flow]=dict_value

    small_inflows_special_even_models_random_eval=retrieve_special_exp_data(small_inflow_data_dict["special_even_models_random_eval"])
    small_inflows_special_random_models_random_eval=retrieve_special_exp_data(small_inflow_data_dict["special_random_models_random_eval"])

    # merge small inflows to random evaluation across inflows on even model
    for model, eval_dict in random_evaluation_summary['inflow'].items(): # even model
        avp=model.split("_")[-1]
        for flow_avp, dict_value in small_inflows_special_even_models_random_eval[model].items():
            flow_avp_list=flow_avp.split("_")
            small_avp = flow_avp_list[-1]
            flow=flow_avp_list[0]
            if avp!=small_avp:
                continue
            random_evaluation_summary['inflow'][model][flow]=dict_value
    # merge small inflows to even evaluation across inflows on random model
    for model, eval_dict in random_evaluation_summary['inflow_random'].items(): # random model
        avp=model.split("_")[-1]
        for flow_avp, dict_value in small_inflows_special_even_models_random_eval[model].items():
            flow_avp_list=flow_avp.split("_")
            small_avp = flow_avp_list[-1]
            flow=flow_avp_list[0]
            if avp!=small_avp:
                continue
            random_evaluation_summary['inflow_random'][model][flow]=dict_value

    # plot against avp and inflow for model 1850
    human=retrieve_exp_data(human_dir)
    even_human=human['even_human_baseline']
    random_human=human['random_human_baseline']

    small_inflows_human_even_eval=retrieve_special_exp_data(small_inflow_data_dict["human_even"])
    small_inflows_human_random_eval=retrieve_special_exp_data(small_inflow_data_dict["human_random"])
    for flow_avp, eval_value in small_inflows_human_even_eval['1650_200_10'].items():
        flow_avp_list=flow_avp.split("_")
        flow=flow_avp_list[0]
        even_human[flow]=eval_value
    for flow_avp, eval_value in small_inflows_human_random_eval['1650_200_10'].items():
        flow_avp_list=flow_avp.split("_")
        flow=flow_avp_list[0]
        random_human[flow]=eval_value
        
        
    #plot_each_category(summary)     
    #plot_each_inflow_each_category(summary)
    compare_av_placement(even_evaluation_summary, even_human, evaluation_key="even_evaluation", inflows_keys=["1850"]) 
    compare_av_placement(random_evaluation_summary, random_human, evaluation_key="random_evaluation", inflows_keys=["1850"])
    #compare_inflow_training(random_evaluation_summary, evaluation_key="random_evaluation", inflows_keys=["1650", "1850", "2000"])
    
def read_inflows(summary, model, key_inflow=None, key_avp=None):
    if model not in summary.keys():
        return None
    result_list=list()
    for eval_key, eval_value in summary[model].items():
        eval_list=eval_key.split("_")
        eval_inflow=int(eval_list[0])
        eval_avp=int(eval_list[-1])
        if key_inflow is not None and key_inflow!=eval_inflow:
            continue
        if key_avp is not None and key_avp!=eval_avp:
            continue
        mean_var_list=eval_value[attr_name].split(",")
        mean=float(mean_var_list[0].strip())
        var=float(mean_var_list[1].strip())
        print(eval_inflow, mean, var)
        #set_trace()
        result_list.append((int(eval_inflow), mean, var))
    try:
        result_list.sort()
    except:
        set_trace()
    return result_list


    # plot against inflow for different models 
if __name__ == "__main__":
    attr_name="Speed"
    retrieve_all_data_and_plot()
    attr_name="Outflow"
    retrieve_all_data_and_plot()


