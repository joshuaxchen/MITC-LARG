import os
from tikz_plot import PlotWriter
from scipy.stats import ttest_ind

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

def read_exp_results(fname):
    results = []
    var=None
    mean=None
    with open(fname, 'r') as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            if l == 'Outflows (veh/hr):\n':
               results.append(float(lines[i+1][1:-2]))
            s='{}: '.format(attr_name)
            if s in l:
                sep_index=l.index(s)
                mean_var_list=l[sep_index+len(s):].split(",")
                var=float(mean_var_list[1])
                mean=float(mean_var_list[0])
    return {attr_name:(results, mean, var)}
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

special_random_evaluation_name="special_models_random_2"
special_even_evaluation_name="special_models_even"
special_evaluation_name="special_models"
special_random_models_dir=os.path.join("..","..","exp_results", special_random_evaluation_name) 
special_even_models_dir=os.path.join("..","..","exp_results", special_even_evaluation_name) 

evaluation_name="random_evaluation"
aamas_avp_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models")
random_aamas_avp_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_random")
aamas_inflows_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_inflows")
random_aamas_inflows_dir=os.path.join("..","..","exp_results", evaluation_name, "aamas_models_random_inflow")

human_dir=os.path.join("..","..","exp_results", "human_baselines")

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
            #data=LastNlines(fname, 6, 2)
            data=read_exp_results(fname)
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
            print(working_dir, folder_name, file_name)
            #for attr_value in data:
            #    text=attr_value.split(":")
            #    attr=text[0]
            #    value=text[1].strip()
            #    exp_summary[attr]=value
            exp_summary=data
            model_exp_dict[folder_name][eval_label]=exp_summary
    return model_exp_dict

   
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
            #exp_summary=retrive_flow_data(fname, attr_name)
            exp_summary=read_exp_results(fname)
            try:
                EVA_index=fname.index("_EAV")
            except:
                EVA_index=fname.index("_EVA")
            eval_text=fname[EVA_index+1:].split("_")[1]
            eval_label=eval_text.split(".")[0]

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

def compare_av_placement_in_random_evaluation(summary, best_models, extra_data,
eval_key):
    # extract aamas without random 
    sorted_model_keys=sort_model_keys(summary['avp'])
    inflows_keys=[1650, 1850, 2000]
    for inflow in inflows_keys:
        ylabel=attr_name
        avp_plot=PlotWriter("Evaluated AVP", ylabel) 
        inflow_plot=PlotWriter("Evaluated Main Inflow", ylabel) 
        
        for model_key in sorted_model_keys:
            if not model_key.startswith(str(inflow)):
                continue

            avp_aamas_summary=summary['avp']
            sorted_e_data=extract_sorted_data(avp_aamas_summary[model_key])
            avp_plot.add_plot(model_key, sorted_e_data)
        
            inflow_aamas_summary=summary['inflow']
            sorted_e_data=extract_sorted_data(inflow_aamas_summary[model_key])
            inflow_plot.add_plot(model_key, sorted_e_data)

        random_label_prefix="random_"
        for model_key in sorted_model_keys:
            if not model_key.startswith(str(inflow)):
                continue

            avp_random_summary=summary['avp_random']
            sorted_e_data=extract_sorted_data(avp_random_summary[model_key])
            avp_plot.add_plot(random_label_prefix+model_key, sorted_e_data)

            inflow_random_summary=summary['inflow_random']
            sorted_e_data=extract_sorted_data(inflow_random_summary[model_key])
            inflow_plot.add_plot(random_label_prefix+model_key, sorted_e_data)

        # add extra_data to avp plot
        best_models=[]
        if extra_data is not None:
            for model_key, model_value in extra_data.items():
                if str(inflow) in model_key or model_key not in best_models:
                    continue
                sorted_e_data=list()
                for eval_key, eval_value in model_value.items():
                    # print(eval_key, inflow)
                    if str(inflow) in eval_key:
                        # print("matched")
                        (mean, var)=extract_mean_var(eval_value, attr_name)
                        sorted_e_data.append((int(eval_key.split("_")[1]), mean, var))
                sorted_e_data.sort()
                # print("sorted_e_data", sorted_e_data)
                avp_plot.add_plot("random_"+model_key, sorted_e_data)
           
        # add extra_data to flow plot
        avp_plot.write_plot(evaluation_name+"/%s_avp_" % eval_key+str(inflow)+".tex",5)
        inflow_plot.write_plot(evaluation_name+"/%s_inflow_"% eval_key+str(inflow)+".tex",5)

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
        plot_1650.write_plot(evaluation_name+"/"+category+"_1650.tex",len(eval_flows))
        plot_1850.write_plot(evaluation_name+"/"+category+"_1850.tex",len(eval_flows))
        plot_2000.write_plot(evaluation_name+"/"+category+"_2000.tex",len(eval_flows))

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
                #print(category, model_key, e_key, e_data)
                mean_var_list=e_data[attr_name].split(",")
                mean=float(mean_var_list[0].strip())
                var=float(mean_var_list[1].strip())
                sorted_e_data.append((int(e_key), mean, var)) 
            sorted_e_data.sort()
            plot.add_plot(label_prefix+model_key, sorted_e_data)
            #print(model_key, sorted_e_data)
        plot.write_plot(evaluation_name+"/"+category+".tex", len(eval_flows))

def plot_special_model_flow(model_key, model_data):
     # extract aamas without random 
    # plot evaluation under each flow        
    data_map=dict()
    for avp in [1, 5, 10, 16, 20, 25, 30, 40]:
        for eval_label, eval_value in model_data.items(): 
            legend_label=model_key+"_"+str(avp)
            if eval_label.split("_")[-1]==str(avp):
                if legend_label not in data_map.keys():
                    data_map[legend_label]=list()       
                #print("flow",model_key, eval_label)

                eval_flow_merge_avp_list=eval_label.split("_")    
                mean_var_list=eval_value[attr_name].split(",")
                mean=float(mean_var_list[0].strip())
                var=float(mean_var_list[1].strip())
                data_map[legend_label].append((int(eval_flow_merge_avp_list[0]), mean, var))

    xlabel="Evaluated Main InFlow" 
    ylabel=attr_name #"Outflow" 
    plot=PlotWriter(xlabel, ylabel) 
    #print(data_map.keys())
    for avp in [1, 5, 10, 16, 20, 25, 30, 40]:
        legend_label=model_key+"_"+str(avp)
        data_map[legend_label].sort()
        legend_label1=legend_label
        plot.add_plot(legend_label1, data_map[legend_label])
    plot.write_plot("./aamas/"+"flow.tex",8)

def plot_special_model_av(summary):
    # extract aamas without random 
    avp30_models=list()
    avp80_models=list()
    for key in summary.keys():
        flow_merge_avp_list=key.split("_")    
        if flow_merge_avp_list[2]=="30":
            avp30_models.append(key)
        elif flow_merge_avp_list[2]=="80":
            avp80_models.append(key)
    avp30_models.sort()
    avp80_models.sort()
    # plot evaluation under each flow        
    data_map=dict()
    for model_key, evaluate in summary.items():
        flow_merge_avp_list=key.split("_")    
        for eval_label, eval_value in evaluate.items(): 
            for flow in eval_flows:
                legend_label=model_key+"_"+str(flow)
                if eval_label.startswith(str(flow)):
                    if legend_label not in data_map.keys():
                        data_map[legend_label]=list()       
                    print(model_key, eval_label)
                    eval_flow_merge_avp_list=eval_label.split("_")    
                    mean_var_list=eval_value[attr_name].split(",")
                    mean=float(mean_var_list[0].strip())
                    var=float(mean_var_list[1].strip())
                    data_map[legend_label].append((int(eval_flow_merge_avp_list[1]), mean, var))
    xlabel="Evaluated AVP" 
    ylabel=attr_name #"Outflow" 
    plot=PlotWriter(xlabel, ylabel) 
    for model_key in avp30_models+avp80_models:            
        if random_human_only:
            if model_key.startswith("1650_200") or model_key.startswith("1850_200"):
                continue
        for flow in eval_flows:
            legend_label=model_key+"_"+str(flow)
            data_map[legend_label].sort()
            legend_label1=legend_label
            if "random" in special_random_evaluation_name:
                legend_label1="random_"+legend_label1
            plot.add_plot(legend_label1, data_map[legend_label])
    plot.write_plot(special_random_evaluation_name+"/"+"avp.tex",len(eval_flows))

def retrieve_all_data_and_plot(extra_data, eval_key):
    summary=dict()
    for category, working_dir in results_dict.items():
        model_exp_summary=retrieve_exp_data(working_dir) 
        summary[category]=model_exp_summary 
        plot_each_category(summary)     
    plot_each_inflow_each_category(summary)
    best_models=["1650_200_30", "1850_200_30", "2000_200_30"]
    compare_av_placement_in_random_evaluation(summary, best_models, extra_data,
    eval_key)

def plot_special_random_even_models(random_data, even_data):
    random_models=list()
    for key in random_data.keys():
        flow_merge_avp_list=key.split("_")    
        random_models.append(key)
    even_models=list()
    for key in even_data.keys():
        flow_merge_avp_list=key.split("_")    
        even_models.append(key)
    random_models.sort()
    even_models.sort()

    # plot evaluation under each flow        
    data_map=dict()
    # add random data
    for model_key, evaluate in random_data.items():
        for eval_label, eval_value in evaluate.items(): 
            for flow in eval_flows:
                legend_label="r_"+model_key+"_"+str(flow)
                #print("check", model_key, eval_label)
                if eval_label.startswith(str(flow)):
                    if legend_label not in data_map.keys():
                        data_map[legend_label]=list()       
                    #print(model_key, eval_label)
                    eval_flow_merge_avp_list=eval_label.split("_")    
                    mean_var_list=eval_value[attr_name].split(",")
                    mean=float(mean_var_list[0].strip())
                    var=float(mean_var_list[1].strip())
                    data_map[legend_label].append((int(eval_flow_merge_avp_list[1]), mean, var))
    for model_key, evaluate in even_data.items():
        for eval_label, eval_value in evaluate.items(): 
            for flow in eval_flows:
                legend_label=model_key+"_"+str(flow)
                if eval_label.startswith(str(flow)):
                    if legend_label not in data_map.keys():
                        data_map[legend_label]=list()       
                    #print(model_key, eval_label)
                    eval_flow_merge_avp_list=eval_label.split("_")    
                    if attr_name not in eval_value:
                        print("exception:",model_key, eval_label)
                        continue
                    mean_var_list=eval_value[attr_name].split(",")
                    mean=float(mean_var_list[0].strip())
                    var=float(mean_var_list[1].strip())
                    data_map[legend_label].append((int(eval_flow_merge_avp_list[1]), mean, var))

    xlabel="Evaluated AVP" 
    ylabel=attr_name
    plot=PlotWriter(xlabel, ylabel) 
    for model_key in random_models:            
    # first order the model
        for flow in eval_flows:
        # second order the flow
            legend_label="r_"+model_key+"_"+str(flow)
            if  legend_label not in data_map.keys():
                print("not in", legend_label)
                continue
            data_map[legend_label].sort()
            # third, order the avp
            plot.add_plot(legend_label, data_map[legend_label])
    for model_key in even_models:            
    # first order the model
        for flow in eval_flows:
        # second order the flow
            legend_label=model_key+"_"+str(flow)
            if legend_label not in data_map.keys():
                continue
            data_map[legend_label].sort()
            # third, order the avp
            plot.add_plot(legend_label, data_map[legend_label])
    plot.write_plot(special_evaluation_name+"/"+"avp.tex",len(eval_flows))

    # used for paper 
    # plot random against even under inflow 1800
def find_best_training_avp_against_flow_p_value(summary, human):
    # only evaluted at avp 10
    selected_model_key="2000_200_30"
    selected_evaluated_data=summary[selected_model_key]
    data_map=dict()
    keys=list()
    for eval_label, eval_value in selected_evaluated_data.items():
        labels=eval_label.split("_")
        flow_str=labels[0]
        flow=int(flow_str)
        if flow>2000:
            continue
        avp_str=labels[1]
        avp=int(avp_str)
        keys.append(avp)
        legend_label=avp_str
        if legend_label not in data_map.keys():
            data_map[legend_label]=list()
        results, mean, var= eval_value[attr_name]
        #mean_var_list=eval_value[attr_name].split(",")
        human_data, human_mean, human_var=human[flow_str][attr_name]
        pvalue=ttest_ind(results, human_data).pvalue
        #mean=float(mean_var_list[0].strip())
        #var=float(mean_var_list[1].strip())
        flow=int(flow_str)
        #data_map[legend_label].append((flow, mean, var))
        data_map[legend_label].append((flow, pvalue, 0))
    keys=list(set(keys))
    keys.sort()
    #key_list=human.keys()
    #key_list.sort()
    #sorted_e_data=list()
    #for e_key in key_list:
    #    labels=e_key.split("_")
    #    flow_str=labels[0]
    #    flow=int(flow_str)
    #    mean_var_list=human[e_key][attr_name].split(",")
    #    mean=float(mean_var_list[0].strip())
    #    var=float(mean_var_list[1].strip())
    #    sorted_e_data.append((flow, mean, var)) 

    xlabel="Evaluated main inflow" 
    ylabel=attr_name #"Outflow" 
    plot=PlotWriter(xlabel, "P-value") 
    #plot.set_title('Training inflow=random {}, Training AVP=[0,100\\%],\\\\ Evaluating AVP=30\\%, Evaluating inflow=random [1600,2000]'.format(main_inflow)) 

    for legend_value in [1,2,3,4,5]: 
        legend_label=str(legend_value)
        data=data_map[legend_label]
        data.sort()
        legend_label1="AVP{}".format(legend_label)
        plot.add_plot(legend_label1, data)
    #plot.add_plot("human_baseline", sorted_e_data)
    plot.write_plot("./aamas/"+"sensitivity_avp.tex",6, color_same=False)

    # used for paper 
    # plot random against even under inflow 1800
def find_best_training_avp_against_avp(summary, human):
    # only evaluted at avp 10
    evaluted_inflow="1800"
    data_map=dict()
    for model_key, model_data in summary.items():
        trained_labels=model_key.split("_")
        trained_avp=trained_labels[2]
        for eval_label, eval_value in model_data.items():
            labels=eval_label.split("_")
            flow_str=labels[0]
            avp_str=labels[1]
            if flow_str!=str(evaluted_inflow):
                continue
            legend_label=model_key+"_"+flow_str
            if legend_label not in data_map.keys():
                data_map[legend_label]=list()
            mean_var_list=eval_value[attr_name].split(",")
            mean=float(mean_var_list[0].strip())
            var=float(mean_var_list[1].strip())
            avp=int(labels[-1])
            data_map[legend_label].append((avp, mean, var))
    
    #print(data_map.keys())
    keys=data_map.keys()
    keys.sort()
    #keys.remove("1650_200_100")
    #keys.remove("1850_200_100")
    #keys.remove("2000_200_100")
    #index1=keys.index("1650_200_80")
    #keys.insert(index1+1, "1650_200_100")
    #index2=keys.index("1850_200_80")
    #keys.insert(index2+1, "1850_200_100")
    #index3=keys.index("2000_200_80")
    #keys.insert(index3+1, "2000_200_100")
    legend_prefix="random_"

    for main_inflow in ["1650", "1850", "2000"]:
        xlabel="Evaluated AVP" 
        ylabel=attr_name #"Outflow" 
        plot=PlotWriter(xlabel, ylabel) 
        plot.set_title('Training inflow=random {}, Training AVP=[0,100\\%],\\\\ Evaluating AVP=[0,40\\%], Evaluating inflow=random 1800'.format(main_inflow)) 
        for legend_label in keys: 
            if main_inflow in legend_label:
                data=data_map[legend_label]
                data.sort()
                legend_label1=legend_prefix+legend_label
                plot.add_plot(legend_label1, data)

        mean_var_list=human[main_inflow][attr_name].split(",")
        mean=float(mean_var_list[0].strip())
        var=float(mean_var_list[1].strip())
        human_data=[(0, mean, var), (40, mean, var)]
        plot.add_plot("human_baseline", human_data)
        plot.write_plot("./aamas/"+"best_avp_vs_avp_%s.tex" % main_inflow,5, color_same=False)

def find_best_training_avp_against_flow(summary, human):
    # only evaluted at avp 10
    selected_model_key="2000_200_30"
    selected_evaluated_data=summary[selected_model_key]
    data_map=dict()
    keys=list()
    for eval_label, eval_value in selected_evaluated_data.items():
        labels=eval_label.split("_")
        flow_str=labels[0]
        flow=int(flow_str)
        if flow>2000:
            continue
        avp_str=labels[1]
        avp=int(avp_str)
        keys.append(avp)
        legend_label=avp_str
        if legend_label not in data_map.keys():
            data_map[legend_label]=list()
        results, mean, var= eval_value[attr_name]
        #mean_var_list=eval_value[attr_name].split(",")
        human_data, human_mean, human_var=human[flow_str][attr_name]
        pvalue=ttest_ind(results, human_data).pvalue
        #mean=float(mean_var_list[0].strip())
        #var=float(mean_var_list[1].strip())
        flow=int(flow_str)
        data_map[legend_label].append((flow, mean, var))
        #data_map[legend_label].append((flow, pvalue, 0))
    keys=list(set(keys))
    keys.sort()
    key_list=human.keys()
    key_list.sort()
    human_sorted_e_data=list()
    for e_key in key_list:
        labels=e_key.split("_")
        flow_str=labels[0]
        flow=int(flow_str)
        _, mean, var=human[e_key][attr_name]
        #mean=float(mean_var_list[0].strip())
        #var=float(mean_var_list[1].strip())
        human_sorted_e_data.append((flow, mean, var)) 

    xlabel="Evaluated main inflow" 
    ylabel=attr_name #"Outflow" 
    plot=PlotWriter(xlabel, "P-value") 
    plot.set_plot_range(1600, 2000, 1500, 1850)
    #plot.set_title('Training inflow=random {}, Training AVP=[0,100\\%],\\\\ Evaluating AVP=30\\%, Evaluating inflow=random [1600,2000]'.format(main_inflow)) 

    for legend_value in [1,2,3,4,5]: 
        legend_label=str(legend_value)
        data=data_map[legend_label]
        data.sort()
        legend_label1="AVP{}".format(legend_label)
        plot.add_plot(legend_label1, data)
    plot.add_plot("human_baseline", human_sorted_e_data)
    plot.write_plot("./aamas/"+"sensitivity_avp.tex",6, color_same=False)

    # used for paper 
    # plot random against even under inflow 1800
def find_best_training_avp_against_avp(summary, human):
    # only evaluted at avp 10
    evaluted_inflow="1800"
    data_map=dict()
    for model_key, model_data in summary.items():
        trained_labels=model_key.split("_")
        trained_avp=trained_labels[2]
        for eval_label, eval_value in model_data.items():
            labels=eval_label.split("_")
            flow_str=labels[0]
            avp_str=labels[1]
            if flow_str!=str(evaluted_inflow):
                continue
            legend_label=model_key+"_"+flow_str
            if legend_label not in data_map.keys():
                data_map[legend_label]=list()
            mean_var_list=eval_value[attr_name].split(",")
            mean=float(mean_var_list[0].strip())
            var=float(mean_var_list[1].strip())
            avp=int(labels[-1])
            data_map[legend_label].append((avp, mean, var))
    
    #print(data_map.keys())
    keys=data_map.keys()
    keys.sort()
    #keys.remove("1650_200_100")
    #keys.remove("1850_200_100")
    #keys.remove("2000_200_100")
    #index1=keys.index("1650_200_80")
    #keys.insert(index1+1, "1650_200_100")
    #index2=keys.index("1850_200_80")
    #keys.insert(index2+1, "1850_200_100")
    #index3=keys.index("2000_200_80")
    #keys.insert(index3+1, "2000_200_100")
    legend_prefix="random_"

    for main_inflow in ["1650", "1850", "2000"]:
        xlabel="Evaluated AVP" 
        ylabel=attr_name #"Outflow" 
        plot=PlotWriter(xlabel, ylabel) 
        plot.set_title('Training inflow=random {}, Training AVP=[0,100\\%],\\\\ Evaluating AVP=[0,40\\%], Evaluating inflow=random 1800'.format(main_inflow)) 
        for legend_label in keys: 
            if main_inflow in legend_label:
                data=data_map[legend_label]
                data.sort()
                legend_label1=legend_prefix+legend_label
                plot.add_plot(legend_label1, data)

        mean_var_list=human[main_inflow][attr_name].split(",")
        mean=float(mean_var_list[0].strip())
        var=float(mean_var_list[1].strip())
        human_data=[(0, mean, var), (40, mean, var)]
        plot.add_plot("human_baseline", human_data)
        plot.write_plot("./aamas/"+"best_avp_vs_avp_%s.tex" % main_inflow,5, color_same=False)




 
if __name__ == "__main__":
    # retrive random models and random evaluation
    #random_model_exp_summary=retrieve_special_exp_data(random_aamas_avp_dir) 
    # retrieve special models
    special_random_summary=retrieve_special_exp_data(special_random_models_dir)
    #model_key="2000_200_30"
    #plot_special_model_flow(model_key, special_random_summary[model_key])
    human=retrieve_exp_data(human_dir)
    random_human=human['random_human_baseline']
    find_best_training_avp_against_flow(special_random_summary, random_human)

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


