#!/bin/bash
TRAIN_DIR=~/gitlab/flow_results/linearPPO
#merge4_highway2000_merge200_avp_10
#merge_4_HUMAN_Sim
#linearPPO
#merge4_highway2000_merge200_avp_90
CHCKPOINT=500
#390

python3 flow/visualize/new_rllib_visualizer.py \
$TRAIN_DIR \
$CHCKPOINT \
--render_mode sumo_gui \
#--handset_avp 30 \
--num_rollouts 1 
#--handset_inflow 3000 

