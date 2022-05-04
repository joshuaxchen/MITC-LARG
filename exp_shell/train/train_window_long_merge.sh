#!/bin/bash

TRAIN_DIR=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_740c0_00000_0_2021-07-04_14-31-39
MARK='2000_200_30'

TRAIN_DIR_6=${HOME}/ray_results/multiagent_normalized_time_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateNormalizedToTime-v0_92974_00000_0_2021-10-24_15-25-47

FLOW_DIR=${PWD}/../..
export PYTHONPATH="${PYTHONPATH}:${FLOW_DIR}"
export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8


MERGE_INFLOW=200
MAIN_INFLOW=2000
AVP=30 #200 400 600 800 # 200 400 600 800 # 200 400 600 800
let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"

WINDOW_RIGHT=100
WINDOW_ABOVE=200

for WINDOW_LEFT in 622 #500 600 700 
do 
	#python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/window_size_long_merge_4_multiagent_i696_1merge_Window_Full_ZeroShot_Transfer.py \
	python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/window_size_single_lane_controller.py \
	--exp_folder_mark zyl \
	--cpu 10 \
	--to_probability \
	--window_size ${WINDOW_LEFT} ${WINDOW_RIGHT} ${WINDOW_ABOVE}
	#--restore ${TRAIN_DIR}/checkpoint_500/checkpoint-500 \
	#--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW 
	#--to_probability 
done



