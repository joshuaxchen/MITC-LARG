#!/bin/bash
TRAIN_DIR=/home/yulin/Desktop/PPO_MergePOEnvArrive-v0_e9efd_00000_0_2021-05-17_08-00-54
CHCKPOINT=500

python3 flow/visualize/new_rllib_visualizer.py \
$TRAIN_DIR \
$CHCKPOINT \
--render_mode sumo_gui \
--max_rollouts 1 
#--handset_inflow 3000 

