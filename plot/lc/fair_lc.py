import os
from tikz_plot import PlotWriter
from IPython.core.debugger import set_trace

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

working_dir=os.path.join("..","..","exp_results","dec_08_assemble") 


def retrive_evaluations(working_dir):
    files=obtain_file_names(working_dir)
    print("working_dir", working_dir)
    model_exp_dict=dict()
    for file_name in files:
        if file_name=='summary.txt' or '.txt' not in file_name :
            continue
        fname=os.path.join(working_dir, file_name)
        data=LastNlines(fname, 6, 2)
        file_name_breakdown=file_name.split(".txt")[0].split("_")
        prefix=""
        if "human" in file_name:
            prefix="human_"    
            eval_label="_".join(file_name_breakdown[2:])
        else:
            eval_label="_".join(file_name_breakdown[1:])
        eval_label=prefix+eval_label
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
    
def plot_against_left_inflow(summary, left_avp_to_plot, right_avp_to_plot, right_main_inflow_to_plot):
    for model_key, evaluate in summary.items():
        data_with_left_main=dict()
        for eval_label, value in evaluate.items():
            prefix=""
            if "human_" in eval_label:
                eval_label="_".join(eval_label.split("_")[1:])
                prefix="human_"

            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left=eval_label.split("_")[0:5]
            #if left_avp_to_plot is not None and avp_left!=left_avp_to_plot:
            #    continue

            #if right_avp_to_plot is not None and avp_right!=right_avp_to_plot:
            #    continue

            #if right_main_inflow_to_plot is not None and right_main_inflow!=right_main_inflow_to_plot:
            #    continue
            print(value)
            if value is None or len(value.keys())==0:
                #set_trace()
                pass
            mean, var=extract_mean_var(value, attr_name)
            
            left_key=prefix+model_key+"_rightAVP"+avp_right+"_leftAVP"+avp_left+"_rightInflow"+right_main_inflow
            if left_key not in data_with_left_main.keys():
                data_with_left_main[left_key]=list()
            data_with_left_main[left_key].append((left_main_inflow, mean, var))
    
        sorted_keys=list(data_with_left_main.keys())
        sorted_keys.sort()
        left_xlabel="LeftMainInflow" 
        ylabel=attr_name
        left_plot=PlotWriter(left_xlabel, ylabel) 
        for legend in sorted_keys:
            data_with_left_main[legend].sort()
            left_plot.add_plot(legend, data_with_left_main[legend])
          
        if left_avp_to_plot is None:
            left_avp_to_plot="*"
        if right_avp_to_plot is None:
            right_avp_to_plot="*"
        if right_main_inflow_to_plot is None:   
            right_main_inflow_to_plot="*"

        left_plot.write_plot("./fig/"+model_key+"_left_main_inflow_%s_%s_%s.tex" % (left_avp_to_plot, right_avp_to_plot, right_main_inflow_to_plot), every_n_per_color=4, line_shape_group_size=4)
 
def plot_against_right_inflow(summary, left_avp_to_plot, right_avp_to_plot, left_main_inflow_to_plot):
    for model_key, evaluate in summary.items():
        data_with_right_main=dict()
        for eval_label, value in evaluate.items():
            prefix=""
            print(eval_label)
            if "human_" in eval_label:
                eval_label="_".join(eval_label.split("_")[1:])
                prefix="human_"

            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left=eval_label.split("_")[0:5]
            #if left_avp_to_plot is not None and avp_left!=left_avp_to_plot:
            #    continue

            #if right_avp_to_plot is not None and avp_right!=right_avp_to_plot:
            #    continue

            if left_main_inflow_to_plot is not None and left_main_inflow!=left_main_inflow_to_plot:
                continue

            mean, var=extract_mean_var(value, attr_name)
            right_key=prefix+model_key+"_rightAVP"+avp_right+"_leftAVP"+avp_left+"_leftInflow"+left_main_inflow
            if right_key not in data_with_right_main.keys():
                data_with_right_main[right_key]=list()
            data_with_right_main[right_key].append((right_main_inflow, mean, var))

        sorted_keys=list(data_with_right_main.keys())
        sorted_keys.sort()

        right_xlabel="RightMainInflow" 
        ylabel=attr_name
        right_plot=PlotWriter(right_xlabel, ylabel) 
        for legend in sorted_keys:
            data_with_right_main[legend].sort()
            right_plot.add_plot(legend, data_with_right_main[legend])
              
        #set_trace()
        if left_avp_to_plot is None:
            left_avp_to_plot="*"
        if right_avp_to_plot is None:
            right_avp_to_plot="*"
        if left_main_inflow_to_plot is None:   
            left_main_inflow_to_plot="*"

        right_plot.write_plot("./fig/"+model_key+"_right_main_inflow_%s_%s_%s.tex" % (left_avp_to_plot, right_avp_to_plot, left_main_inflow_to_plot), every_n_per_color=4, line_shape_group_size=4)
      
def plot_against_right_avp(summary, left_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot):
    for model_key, evaluate in summary.items():
        data_with_right_avp=dict()
        for eval_label, value in evaluate.items():
            prefix=""
            if "human_" in eval_label:
                eval_label="_".join(eval_label.split("_")[1:])
                prefix="human_"
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left=eval_label.split("_")[0:5]
            #if left_avp_to_plot is not None and avp_left!=left_avp_to_plot: 
            #    continue           

            if left_main_inflow_to_plot is not None and left_main_inflow!=left_main_inflow_to_plot:
                continue

            #if right_main_inflow_to_plot is not None and right_main_inflow!=right_main_inflow_to_plot:
            #    continue

            mean, var=extract_mean_var(value, attr_name)

            right_key=prefix+model_key+"_leftAVP"+avp_left+"_rightInflow"+right_main_inflow+"_leftInflow"+left_main_inflow
            if right_key not in data_with_right_avp.keys():
                data_with_right_avp[right_key]=list()
            data_with_right_avp[right_key].append((avp_right, mean, var))
        

        sorted_keys=list(data_with_right_avp.keys())
        sorted_keys.sort()
        right_xlabel="RightAVP" 
        ylabel=attr_name
        right_plot=PlotWriter(right_xlabel, ylabel) 
        for legend in sorted_keys:
            if len(data_with_right_avp[legend])<2:
                continue
            data_with_right_avp[legend].sort()
            right_plot.add_plot(legend, data_with_right_avp[legend])
          
        if left_avp_to_plot is None:
            left_avp_to_plot="*"
        if right_main_inflow_to_plot is None:
            right_main_inflow_to_plot="*"
        if left_main_inflow_to_plot is None:   
            left_main_inflow_to_plot="*"


        right_plot.write_plot("./fig/"+model_key+"_avp_right_%s_%s_%s.tex" % (left_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot),  every_n_per_color=4, line_shape_group_size=4)


def plot_against_left_avp(summary, right_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot):
    for model_key, evaluate in summary.items():
        data_with_left_avp=dict()
        for eval_label, value in evaluate.items():
            prefix=""
            if "human_" in eval_label:
                eval_label="_".join(eval_label.split("_")[1:])
                prefix="human_"
            right_main_inflow, left_main_inflow, merge_inflow, avp_right, avp_left=eval_label.split("_")[0:5]
        
            #if right_avp_to_plot is not None and avp_right!=right_avp_to_plot: 
            #    continue
        
            if left_main_inflow_to_plot is not None and left_main_inflow!=left_main_inflow_to_plot:
                continue

            #if right_main_inflow_to_plot is not None and right_main_inflow!=right_main_inflow_to_plot:
            #    continue

            
            left_key=prefix+model_key+"_rightAVP"+avp_right+"_rightInflow"+right_main_inflow+"_leftInflow"+left_main_inflow
            mean, var=extract_mean_var(value, attr_name)
            if left_key not in data_with_left_avp.keys():
                data_with_left_avp[left_key]=list()
            data_with_left_avp[left_key].append((avp_left, mean, var))

        sorted_keys=list(data_with_left_avp.keys())
        sorted_keys.sort()

        left_xlabel="LeftAVP" 
        ylabel=attr_name
        left_plot=PlotWriter(left_xlabel, ylabel) 
        for legend in sorted_keys:
            if len(data_with_left_avp[legend])<2:
                continue
            data_with_left_avp[legend].sort()
            left_plot.add_plot(legend, data_with_left_avp[legend])
          
        if right_avp_to_plot is None:
            right_avp_to_plot="*"
        if left_main_inflow_to_plot is None:   
            left_main_inflow_to_plot="*"
        if right_main_inflow_to_plot is None:   
            right_main_inflow_to_plot="*"

        left_plot.write_plot("./fig/"+model_key+"_avp_left_%s_%s_%s.tex"% (right_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot),  every_n_per_color=4, line_shape_group_size=4)

        
if __name__ == "__main__":
    # retrive random models and random evaluation
    #random_model_exp_summary=retrieve_special_exp_data(random_aamas_avp_dir) 
    # retrieve special models
    data=dict()
    #for preset_i in ["human", "preset_1_dr_light"]:
    #for setting in ["aamas_right_1", "aamas_left_1", "aamas_both"]:
    for setting in ["aamas_right", "aamas_left"]:
    #for setting in ["aamas_right"]:
        setting_dir=os.path.join(working_dir, setting)
        data_i=retrive_evaluations(setting_dir)
        data[setting]=data_i
    #set_trace()
    left_avp_to_plot="0" 
    right_avp_to_plot="10" 
    left_main_inflow_to_plot="1600" 
    right_main_inflow_to_plot="2000" 
    plot_against_right_inflow(data, left_avp_to_plot, right_avp_to_plot, left_main_inflow_to_plot)
    plot_against_right_avp(data, left_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot)


    left_avp_to_plot="10" 
    right_avp_to_plot="0" 
    left_main_inflow_to_plot="1000" 
    right_main_inflow_to_plot="1600" 
    plot_against_left_inflow(data, left_avp_to_plot, right_avp_to_plot, right_main_inflow_to_plot)
    plot_against_left_avp(data, right_avp_to_plot, left_main_inflow_to_plot, right_main_inflow_to_plot)

#plot_against_inflow(summary, left_avp_to_plot, right_avp_to_plot, left_main_inflow_to_plot):
    #plot_against_assertive(data)

