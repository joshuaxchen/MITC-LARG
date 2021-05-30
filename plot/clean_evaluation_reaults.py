import os

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



working_dir=os.path.join("..","avp_multi_agent")
folder_name_list=obtain_subfolder_names(working_dir)
files_in_each_folder=dict()
summary=dict()
for folder_name in folder_name_list:
    folder_path=os.path.join(working_dir, folder_name)
    files_in_each_folder[folder_name]=obtain_file_names(folder_path)
    summary[folder_name]=dict()
    for file_name in files_in_each_folder[folder_name]:
        if file_name=='summary.txt':
            continue
        fname=os.path.join(folder_path, file_name)
        data=LastNlines(fname, 6, 2)
        summary[folder_name][file_name]=dict()
        for attr_value in data:
            text=attr_value.split(":")
            attr=text[0]
            value=text[1].strip()
            summary[folder_name][file_name][attr]=value
#print(summary)
for folder_name in folder_name_list:
    attr_name='Speed'
    for file_name in files_in_each_folder[folder_name]:
        key=file_name.split("_.")
        print(key[-2:])
        if file_name=='summary.txt':
            continue
        print(file_name,summary[folder_name][file_name]['Speed'])
    print('\n')




