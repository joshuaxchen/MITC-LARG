# Flow

[Flow](https://flow-project.github.io/) is a computational framework for deep RL and control experiments for traffic microsimulation.

# Important parameters for training and visualization

--handset_inflow MAIN_HUMAN_INFLOW MAIN_RL_INFLOW MERGE_INFLOW: handset_inflow takes three paramters as input to specify the main human inflow, main rl inflow, and merge inflow in a simple merge scenario. (used for both training and evalution)

--exp_folder_make "prefix of the folder name with the trained model": exp_folder_name is used to specify the prefix of the foldername of the trained model under ray_results.  (used for both training and evalution)

--cpu NUMBER_OF_CPU_TO_USE: Specify the number of cpus to be used.  (used for training)

--agent_action_policy_dir "path_to_your_trained_model": This is used to specify the policy for the AVs.  (used for evalution)

--seed_dir "path_to_the_folder_of_the_random_seed": This is used to specify the path to the random seed. (used for evaluation)

--lateral_resolution 3.2: This is a default parameter used for multi-lane scenario to specify the lateral_resolution. (used for evaluation)

--render_mode [sumo_gui|no_render]: This is to specify whether you want to visualize the results in sumo or not. (used for evaluation) 

--rl_inflows RL_INFLOW_RIGHT RL_INFLOW_LEFT: It takes two parameters as input to specify the right rl inflow, and left rl inflow. (used for evaluation in a 2-lane scenario)

--human_lane_change [0/1] [0/1]: It takes two integers as input to specify whether there is lane change (1) or not (0) for human driven vehicles in the right and left lane respectively. (used for both training and evaluation) 

--rl_lane_change [0/1] [0/1]: It takes two integers as input to specify whether there is lane change (1) or not (0) for AVs in the right and left lane respectively. (used for both training and evaluation) 

--merge_inflow MERGE_INFLOW: It specifies the inflow of the merge lane, assuming that they are all human driven vehicles. (used for both evaluation) 

--speed_gain [0, 1]: This is a parameter used by sumo lane change model to specify the speed gain for each vehicle, the willingness of the vehicle to change lanes to gain speed. (used for evaluation) 

--to_probability: This is a flag, and it is used to set the inflows in the main highway to be randomly placed. It does not change the merge inflow placement. (used for both training and evaluation) 

--horizon HORIOZN: This is used to specify the horizon of the experiments, in terms of time steps. (used for evaluation) 

--assertive ASSERTIVE: This is a parameter used by sumo lane change model to specify the assertiveness (willingness to accept lower front and rear gaps on the target lane). (used for both traning and evaluation) 

--run_random_seed seed_index: This is used to run the experiment of a specific random seed (out of 100). (used for evaluation) 

--print_vehicles_per_time_step_in_file "path_to_log_file": This is used to record the number of vehicles remainning in the network for the first/specified experiment/random seed. (used for evaluation) 

--print_metric_per_time_step_in_file "path_to_log_file": This is used to record the inflow, outflow measured at every time step in the first/specified experiment/random seed. (used for evaluation) 

--print_inflow_outflow_var_in_file "path_to_log_file": This is used to record the mean, variance of the inflow/outflow at the last 1000 time steps. (used for evaluation) 

--lc_probability LC_PROB: This is deprecated. It was used to manually push the human driven vehicles to change lane with some probability. (used for evaluation) 

--i696: This flag is set to indicate that the inflows is added to the i696 network, where the edges have different names than simple merge and there are three merging ramps sharing the same merge inflow. (used for evaluation) 

--highway_len LENGTH: The total length of the highway. This is used for multiple on ramps.

--on_ramps RAMP_1_LOCATION RAMP_2_LOCATION: The x coordinate of the first and the second on ramp.

# Example Shell
1. [Traning an AAMAS model (under even placement, add flag --to_probability for random placement)](https://github.com/yulinzhang/MITC-LARGE/blob/yulin_develop/exp_shell/train/random_placement_aamas_models.sh)
2. [Evaluating an AAMAS model](https://github.com/yulinzhang/MITC-LARGE/blob/yulin_develop/exp_shell/evaluate/particular_random_model.sh)
3. [Evaluating on multiple merging ramps](https://github.com/yulinzhang/MITC-LARGE/blob/yulin_develop/exp_shell/evaluate/mor.sh)
4. Evaluating on multi-lane scenario: [visualization](https://github.com/yulinzhang/MITC-LARGE/blob/yulin_develop/exp_shell/evaluate/lanechange_gui.sh) and [evaluation](https://github.com/yulinzhang/MITC-LARGE/blob/yulin_develop/exp_shell/evaluate/deterministic_aamas_lc.sh)

