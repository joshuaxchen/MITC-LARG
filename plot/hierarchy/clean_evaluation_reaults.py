import os
import re
def obtain_file_names(folder_path):
    for x in os.walk(folder_path):
        if x[0]==folder_path:
            return x[2]
    return None
def obtain_subfolder_names(folder_path):
    for x in os.walk(working_dir):
        if x[0]==working_dir:
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

# Function to read
# last N lines of the file
def obtainLastResult(fname):
    # opening file using with() method
    # so that file get closed
    # after completing work
    with open(fname) as file:
        # loop to read iterate
        # last n lines and print it
        print('reading content from file:', fname)
        lines=file.readlines() 
        matched=False
        line_of_results=list()
        for line in reversed(lines):
            mean_and_var=None
            if line.startswith('Outflow:'):
                #mean_and_var=line[8:]
                mean_and_var=line
                matched=True
            elif line.startswith('Inflow:'):
                #mean_and_var=line[7:]
                mean_and_var=line
                matched=True
            elif line.startswith('Speed:'):
                #mean_and_var=line[6:]
                mean_and_var=line
                matched=True
            elif line.startswith('Reward:'):
                #mean_and_var=line[7:]
                mean_and_var=line
                matched=True
            else:
                if matched:
                    break
                continue 
            line_of_results.append(mean_and_var)
    return line_of_results

working_dir=os.path.join("..","..","exp_results", "aamas")#"hierarchy")#, "main2000-1700_merge200")
folder_name_list=obtain_subfolder_names(working_dir)
files_in_each_folder=dict()
summary=dict()
print(folder_name_list)
for folder_name in folder_name_list:
    folder_path=os.path.join(working_dir, folder_name)
    files_in_each_folder[folder_name]=obtain_file_names(folder_path)
    summary[folder_name]=dict()
    for file_name in files_in_each_folder[folder_name]:
        if file_name=='summary.txt':
            continue
        fname=os.path.join(folder_path, file_name)
        data=obtainLastResult(fname)#, 6, 2)
        summary[folder_name][file_name]=dict()
        print(data)
        for attr_value in data:
            print(attr_value)
            text=attr_value.split(":")
            attr=text[0]
            value=text[1].strip()
            summary[folder_name][file_name][attr]=value
print(summary)
for folder_name in folder_name_list:
    attr_name='Outflow'
    attr_list=[]
    for file_name in files_in_each_folder[folder_name]:
        key=re.split("_",file_name)[-1].split(".")[0]
        if file_name=='summary.txt':
            continue
        values=summary[folder_name][file_name][attr_name].split(",")
        attr_list.append((int(key), values[0].strip(), values[1].strip())) 
    attr_list.sort()
    print(folder_name)
    for item in attr_list:
        print(item[0], item[1], item[2])

    print('\n')



