import os
from tikz_plot import PlotWriter
import collections
from IPython.core.debugger import set_trace

attr_name="Speed"


data_dict={
"special_even_models_even_eval": os.path.join("..","..","exp_results", "special_even_models_even_eval_ijcai"),
"special_even_models_random_eval": os.path.join("..","..","exp_results", "special_even_models_random_eval_ijcai"),
"special_random_models_even_eval": os.path.join("..","..","exp_results", "special_random_models_even_eval_ijcai"),
"special_random_models_random_eval": os.path.join("..","..","exp_results", "special_random_models_random_eval_ijcai"),
"human_even": os.path.join("..","..","exp_results","special_human_even_eval_ijcai"),
"human_random": os.path.join("..","..","exp_results","special_human_random_eval_ijcai")
}


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

def read_inflows(summary, model, key_inflow=None, key_avp=None):
    if model not in summary.keys():
        return None
    result_list=list()
    result_list.append((0,0,0))
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
        #print(str(eval_inflow)+ "\t"+str(mean)+"\t"+str(var))
        #set_trace()
        result_list.append((int(eval_inflow), mean, var))
    try:
        result_list.sort()
    except:
        set_trace()
    return result_list


if __name__ == "__main__":
    special_even_models_even_eval=retrieve_special_exp_data(data_dict["special_even_models_even_eval"])
    fig1_key=["2000-200-10", "2000-200-30", "2000-200-50", "2000-200-80", "2000-200-100"]
    #set_trace()
    print("even evaluation")
    for model_key in fig1_key:
        avp=int(model_key.split("-")[-1])
        model_key=model_key.replace("-","_")
        print("even_"+model_key)
        even_list=read_inflows(special_even_models_even_eval, model_key, key_avp=avp)
        for even_data in even_list:
            print(str(even_data[0])+ "\t"+str(even_data[1])+"\t"+str(even_data[2]))
        print("-----------------------")
    
    special_random_models_even_eval=retrieve_special_exp_data(data_dict["special_random_models_even_eval"])
    for model_key in fig1_key:
        avp=int(model_key.split("-")[-1])
        model_key=model_key.replace("-","_")
        print("random_"+model_key)
        even_list=read_inflows(special_even_models_even_eval, model_key, key_avp=avp)
        for even_data in even_list:
            print(str(even_data[0])+ "\t"+str(even_data[1])+"\t"+str(even_data[2]))
        print("-----------------------")
    print("****************************")
    special_even_models_random_eval=retrieve_special_exp_data(data_dict["special_even_models_random_eval"])
    fig1_key=["2000-200-10", "2000-200-30", "2000-200-50", "2000-200-80", "2000-200-100"]
    #set_trace()
    print("random evaluation")
    for model_key in fig1_key:
        avp=int(model_key.split("-")[-1])
        model_key=model_key.replace("-","_")
        print("even_"+model_key)
        even_list=read_inflows(special_even_models_even_eval, model_key, key_avp=avp)
        for even_data in even_list:
            print(str(even_data[0])+ "\t"+str(even_data[1])+"\t"+str(even_data[2]))
        print("-----------------------")
    
    special_random_models_random_eval=retrieve_special_exp_data(data_dict["special_random_models_random_eval"])
    for model_key in fig1_key:
        avp=int(model_key.split("-")[-1])
        model_key=model_key.replace("-","_")
        print("random_"+model_key)
        even_list=read_inflows(special_even_models_even_eval, model_key, key_avp=avp)
        for even_data in even_list:
            print(str(even_data[0])+ "\t"+str(even_data[1])+"\t"+str(even_data[2]))
        print("-----------------------")
    
