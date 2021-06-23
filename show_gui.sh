#!/bin/bash
TRAIN_DIR=~/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Hierarchy-v0_8659f_00000_0_2021-06-22_21-55-53

#yulin_adaptive_headway_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4AdaptiveHeadway-v0_4383e_00000_0_2021-06-11_19-15-16
#~/gitlab/flow_results/PPO_MultiAgentHighwayPOEnvMerge4AdaptiveHeadway-v0_4383e_00000_0_2021-06-11_19-15-16
#merge4_highway2000_merge200_avp_10
#merge_4_HUMAN_Sim
#linearPPO
#merge4_highway2000_merge200_avp_90
CHCKPOINT=500
#390

PYTHONPATH=. python3 ./flow/visualize/new_rllib_visualizer.py \
$TRAIN_DIR \
$CHCKPOINT \
--num_rollouts 1 \
--render_mode no_render
#--handset_avp 30 \
#--handset_inflow 3000 
#--render_mode sumo_gui 

