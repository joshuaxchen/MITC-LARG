import os
import sys
import datetime

def check_existing_trained_progress(exp_tag, alg_run):
    # jobs in condor tend to be preempted by condor sheduler and then resumed.
    # when resumed, we should restore from existing progress instead of
    # starting from the beginning.
    exp_parent_path=os.path.join("~","ray_results", exp_tag)  
    exp_parent_path=os.path.expanduser(exp_parent_path)
    #print(exp_parent_path)
    if os.path.isdir(exp_parent_path):
        root_dir_file_list=os.walk(exp_parent_path)
        i=0
        latest_checkpoint_folder=None
        latest_time=None
        latest_checkpoint_num=-1
        for (root, child_folders, file_list) in root_dir_file_list:
            divided_path_list=root.split("/")
            #print(divided_path_list[-1])
            if not divided_path_list[-1].startswith(alg_run):
                continue
            folder_name_list=root.split("_")
            day=folder_name_list[-2]
            time=folder_name_list[-1]
            folder_date=datetime.datetime.strptime(day+'_'+time, '%Y-%m-%d_%H-%M-%S')
            #print(folder_date)
            for checkpoint_dir in child_folders:
                if not checkpoint_dir.startswith('checkpoint'):
                    continue
                checkpoint_num=int(checkpoint_dir.split("_")[1])
                #print(latest_time)
                if latest_time is None or latest_time<folder_date or (latest_time==folder_date and latest_checkpoint_num<checkpoint_num):
                    latest_time=folder_date
                    latest_checkpoint_num=checkpoint_num
                    latest_checkpoint_folder=os.path.join(root, checkpoint_dir)
        return latest_checkpoint_folder
    return None
    

exp_tag="yulin_multiagent_Even_Avp100_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1"
alg_run="PPO"
checkpoint_to_restore=check_existing_trained_progress(exp_tag, alg_run)
print(checkpoint_to_restore)
