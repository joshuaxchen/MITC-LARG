#!/bin/bash
TRAIN_DIR=~/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/aamas_full
TRAIN_DIR1=~/ray_results/yulin_countbetween_hierarchy_eta1_0.9_eta2_0.1/countbetween_hierarchy_aamas
TRAIN_DIR1=~/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/hierarchy_based_on_aamas_full
TRAIN_DIR1=~/ray_results/yulin_densityahead_hierarchy_eta1_0.9_eta2_0.1/aamas_density_hierarchy_avp10
#TRAIN_DIR=~/gitlab/flow_results/new_adaptive_headway_penality_avp10_main2000_merge200_maxheadway50
#count_ahead_normalized_multiagent_main2000_merge200_avp10
#new_adaptive_headway_penality_avp10_main2000_merge200_maxheadway50
#new_adaptive_headway_avp10_main2000_merge200_maxheadway50
#$merge4_highway2000_merge200_avp_10
#new_adaptive_headway_avp10_main2000_merge200_maxheadway50
#new_adaptive_headway_avp90_main2000_merge200_maxheadway50
#new_adaptive_headway_count_ahead_avp10_main2000_merge200_maxheadway50
#adaptive_headway_count_ahead_main2000_merge200_avp10_maxheadway50
#adaptive_headway_penality_main2000_merge200_avp10_maxheadway50
#merge4_highway2000_merge200_avp_90 
#TRAIN_DIR=~/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Hierarchy-v0_8659f_00000_0_2021-06-22_21-55-53

#yulin_adaptive_headway_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4AdaptiveHeadway-v0_4383e_00000_0_2021-06-11_19-15-16
#~/gitlab/flow_results/PPO_MultiAgentHighwayPOEnvMerge4AdaptiveHeadway-v0_4383e_00000_0_2021-06-11_19-15-16
#merge4_highway2000_merge200_avp_10
#merge_4_HUMAN_Sim
#linearPPO
#merge4_highway2000_merge200_avp_90
CHCKPOINT=500
#390

<<<<<<< HEAD
HUMAN_DIR=/home/users/flow_user/ray_results/yulin_merge_4_HUMAN_Sim/PPO_MergePOEnv-v0_baf56_00000_0_2021-05-26_02-05-19 

#PYTHONPATH=. python3 ./flow/visualize/new_rllib_visualizer.py \
#$TRAIN_DIR \
#$CHCKPOINT \
#--num_rollouts 1 \
#--render_mode sumo_gui \
#--handset_avp 90 

PYTHONPATH=. python3 ./flow/visualize/new_rllib_visualizer.py \
$HUMAN_DIR \
1 \
=======
PYTHONPATH=. python3 flow/visualize/new_rllib_visualizer.py \
$TRAIN_DIR \
$CHCKPOINT \
--render_mode sumo_gui \
>>>>>>> 38776bac8c1608ea867ab0c7474ff9c91d7ecbf4
--num_rollouts 1 \
--render_mode sumo_gui \
--handset_inflow 1485 165 200
#--handset_avp 60 
#--render_mode no_render
#--policy_dir $TRAIN_DIR \

