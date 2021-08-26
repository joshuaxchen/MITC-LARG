import os
from tikz_plot import PlotWriter
attr_name="Inflow"
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

special_random_evaluation_name="special_models_random"
special_even_evaluation_name="special_models_even"
special_evaluation_name="special_models"
special_random_models_dir=os.path.join("..","..","exp_results", special_random_evaluation_name) 
special_even_models_dir=os.path.join("..","..","exp_results", special_even_evaluation_name) 

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
        if folder_name.startswith("bk"):
            continue
        folder_path=os.path.join(working_dir, folder_name)
        files_in_each_folder[folder_name]=obtain_file_names(folder_path)
        model_exp_dict[folder_name]=dict()
        for file_name in files_in_each_folder[folder_name]:
            if file_name=='summary.txt':
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
                specs_list=fname[EVA_index+1:].split(".")
                eval_main_merge_avp_text=specs_list[0]
                main_merge_avp_text="_".join(eval_main_merge_avp_text.split("_")[1:])
            elif length==6: # random evaluation
                inflow_text=file_name_breakdown[1] 
                merge_text=file_name_breakdown[2] 
                avp_text=file_name_breakdown[-1].split(".")[0]
                main_merge_avp_text=inflow_text+"_"+merge_text+"_"+avp_text
            eval_label=main_merge_avp_text
            exp_summary=dict()
            print(working_dir, folder_name, file_name)
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
        folder_path=os.path.join(working_dir, folder_name)
        files_in_each_folder[folder_name]=obtain_file_names(folder_path)
        model_exp_dict[folder_name]=dict()
        for file_name in files_in_each_folder[folder_name]:
            if file_name=='summary.txt':
                continue
            fname=os.path.join(folder_path, file_name)
            exp_summary=retrive_flow_data(fname, attr_name)
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

def compare_av_placement(summary, best_models, extra_data):
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
        avp_plot.write_plot(evaluation_name+"/placement_avp_"+str(inflow)+".tex",5)
        inflow_plot.write_plot(evaluation_name+"/placement_inflow_"+str(inflow)+".tex",5)

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

def plot_special_model_flow(summary):
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
        for avp in [1, 5, 10, 16, 20, 25, 30, 40]:
            for eval_label, eval_value in evaluate.items(): 
                legend_label=model_key+"_"+str(avp)
                if eval_label.split("_")[-1]==str(avp):
                    if avp==5:
                        pass
                    if legend_label not in data_map.keys():
                        data_map[legend_label]=list()       
                    #print("flow",model_key, eval_label)

                    eval_flow_merge_avp_list=eval_label.split("_")    
                    mean_var_list=eval_value[attr_name].split(",")
                    mean=float(mean_var_list[0].strip())
                    var=float(mean_var_list[1].strip())
                    data_map[legend_label].append((int(eval_flow_merge_avp_list[0]), mean, var))
    xlabel="Evaluated Main InFlow" 
    ylabel="Outflow" 
    plot=PlotWriter(xlabel, ylabel) 
    #print(data_map.keys())
    for model_key in avp30_models+avp80_models:            
        #if model_key.startswith("1650_200_30") or model_key.startswith("1850_200_80"):
        #    continue
        for avp in [1, 5, 10, 16, 20, 25, 30, 40]:
            legend_label=model_key+"_"+str(avp)
            data_map[legend_label].sort()
            legend_label1=legend_label
            if "random" in special_random_evaluation_name:
                legend_label1="random_"+legend_label1
            plot.add_plot(legend_label1, data_map[legend_label])
    plot.write_plot(special_random_evaluation_name+"/"+"flow.tex",8)

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
    ylabel="Outflow" 
    plot=PlotWriter(xlabel, ylabel) 
    for model_key in avp30_models+avp80_models:            
        #if model_key.startswith("1650_200_30") or model_key.startswith("1850_200_80"):
            #continue
        for flow in eval_flows:
            legend_label=model_key+"_"+str(flow)
            data_map[legend_label].sort()
            legend_label1=legend_label
            if "random" in special_random_evaluation_name:
                legend_label1="random_"+legend_label1
            plot.add_plot(legend_label1, data_map[legend_label])
    plot.write_plot(special_random_evaluation_name+"/"+"avp.tex",len(eval_flows))

def retrieve_all_data_and_plot(extra_data):
    summary=dict()
    for category, working_dir in results_dict.items():
        model_exp_summary=retrieve_exp_data(working_dir) 
        summary[category]=model_exp_summary 
        plot_each_category(summary)     
    plot_each_inflow_each_category(summary)
    best_models=["1650_200_30", "1850_200_30", "2000_200_30"]
    compare_av_placement(summary, best_models, extra_data)

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
    ylabel="Outflow" 
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

def plot_against_merge_inflow(special_random_summary, special_even_summary):
    best_models=["2000_200_30"]#["1650_200_30", "1850_200_30", "2000_200_30"]
    # extract aamas without random 
    i=0
    avp30_models=list()
    for key in special_random_summary.keys():
        flow_merge_avp_list=key.split("_")    
        if flow_merge_avp_list[2]=="30":
            avp30_models.append(key)
    avp30_models.sort()

    # plot evaluation under each flow        
    random_data_map=dict()
    even_data_map=dict()
    summary=special_random_summary
    for model_key, evaluate in summary.items():
        # main inflow is fixed to be 2000
        eval_main_inflow=2000
        for eval_label, eval_value in evaluate.items(): 
            if str(eval_main_inflow) not in eval_label:
                continue
            # assuming 2000_merge_avp
            print(eval_label)
            params=eval_label.split("_")
            avp_text=params[2]
            legend_label=model_key+"_"+avp_text

            mean_var_list=eval_value[attr_name].split(",")
            mean=float(mean_var_list[0].strip())
            var=float(mean_var_list[1].strip())
            if legend_label not in random_data_map.keys():
                random_data_map[legend_label]=list()
            random_data_map[legend_label].append((int(params[1]), mean, var))
    if attr_name=="Outflow":
        human_data=[
            (180, 1606.68, 12.35),
            (190, 1566.75, 15.40),
            (200, 1560.42, 14.02 ),
            (210, 1513.08, 12.53),
            (220, 1501.52, 10.96),
            (230, 1459.91, 18.49),
            (240, 1442.81, 9.35),
            (250, 1444.36, 11.60),
            (260, 1397.66, 14.40),
            (270, 1358.32, 10.68 ),
            (280, 1349.45, 10.89),
            (290, 1304.93, 14.67),
            (300, 1244.99, 11.79),
            (310, 1253.92, 10.22),
            (320, 1256.51, 11.12),
            (330, 1245.96, 12.84),
            (340, 1190.77, 16.95),
            (350, 1145.12, 16.60),
            (360, 1106.86, 14.18),
            (370, 1087.40, 17.10),
            (380, 1060.09, 17.02),
            (390, 1027.08, 17.67),
            (400, 990.29, 22.90),
            (500, 973.03, 13.39),
            (600, 852.90, 20.77),
            (700, 813.10, 16.86),
            (800, 846.00, 5.98),
            (900, 915.88, 5.56),
            (1000,1003.79, 5.12)
        ]
    elif attr_name=="Speed":
        human_data=[
            (180, 7.78, 0.19),
            (190,  7.41, 0.15),
            (200, 7.32, 0.15),
            (250, 6.25, 0.11),
            (300, 4.98, 0.11),
            (350, 4.30, 0.10),
            (400, 3.53, 0.11),
            (500, 3.17, 0.06),
            (600, 2.53, 0.07),
            (700, 2.17, 0.06),
            (800, 2.05, 0.05),
            (900, 2.02, 0.03),
            (1000, 2.09, 0.03),
        ]
    elif attr_name=="Inflow":
        human_data=[
            (180, 1766.56, 12.22),
            (190, 1728.80, 14.58),
            (200, 1728.86, 13.63),
            (250, 1625.12, 11.72),
            (300, 1443.82, 11.36),
            (350, 1356.37, 16.61),
            (400, 1215.97, 22.31),
            (500, 1205.54, 12.55),
            (600, 1104.65, 20.01),
            (700, 1078.13, 16.30),
            (800, 1116.97, 6.00),
            (900, 1187.82, 5.61),
            (1000, 1279.87, 4.71),
        ]
        
    summary=special_even_summary
    for model_key, evaluate in summary.items():
        # main inflow is fixed to be 2000
        eval_main_inflow=2000
        for eval_label, eval_value in evaluate.items(): 
            if str(eval_main_inflow) not in eval_label:
                continue
            # assuming 2000_merge_avp
            #print(eval_label)
            params=eval_label.split("_")
            avp_text=params[2]
            legend_label=model_key+"_"+avp_text

            mean_var_list=eval_value[attr_name].split(",")
            mean=float(mean_var_list[0].strip())
            var=float(mean_var_list[1].strip())
            if legend_label not in even_data_map.keys():
                even_data_map[legend_label]=list()
            even_data_map[legend_label].append((int(params[1]), mean, var))

        #print(data_map.keys())

    xlabel="Evaluated Merge InFlow" 
    ylabel=attr_name
    total_plot=PlotWriter(xlabel, ylabel) 


    for model_key in avp30_models:            
        if random_human_only:
            if "1650_200" in model_key or "1850_200" in model_key:
                continue
        xlabel="Evaluated Merge InFlow" 
        ylabel=attr_name
        plot=PlotWriter(xlabel, ylabel) 

        for avp in [1, 5, 10, 16, 20, 30, 40]:
            legend_label=model_key+"_"+str(avp)

            random_data_map[legend_label].sort()
            legend_label1="random_"+legend_label
            plot.add_plot(legend_label1, random_data_map[legend_label])
            total_plot.add_plot(legend_label1, random_data_map[legend_label])

        #for avp in [1, 5, 10, 16, 20, 30, 40]:
        #    legend_label=model_key+"_"+str(avp)

        #    even_data_map[legend_label].sort()
        #    legend_label2=legend_label
        #    plot.add_plot(legend_label2, even_data_map[legend_label])
        #    total_plot.add_plot(legend_label2, even_data_map[legend_label])
        
        plot.add_human=False
        plot.add_plot("human_baseline", human_data)
        plot.write_plot(special_random_evaluation_name+"/"+"merge_"+model_key+".tex",7)

    total_plot.add_human=False
    total_plot.add_plot("human_baseline", human_data)
    total_plot.write_plot(special_random_evaluation_name+"/"+"merge_total_2000.tex",7)

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
    ylabel="Outflow" 
    plot=PlotWriter(xlabel, ylabel) 
    for model_key in avp30_models+avp80_models:            
        #if model_key.startswith("1650_200_30") or model_key.startswith("1850_200_80"):
            #continue
        for flow in eval_flows:
            legend_label=model_key+"_"+str(flow)
            data_map[legend_label].sort()
            legend_label1=legend_label
            if "random" in special_random_evaluation_name:
                legend_label1="random_"+legend_label1
            plot.add_plot(legend_label1, data_map[legend_label])
        plot.write_plot(special_random_evaluation_name+"/"+"merge.tex",len(eval_flows))

        compare_av_placement(summary, best_models, extra_data)

if __name__ == "__main__":
    # retrive random models and random evaluation
    #random_model_exp_summary=retrieve_special_exp_data(random_aamas_avp_dir) 
    # retrieve special models
    special_random_summary=retrieve_special_exp_data(special_random_models_dir)
    special_even_summary=retrieve_special_exp_data(special_even_models_dir)
    # data to add 2000_200_30
    # add to the special models
    plot_against_merge_inflow(special_random_summary, special_even_summary)



