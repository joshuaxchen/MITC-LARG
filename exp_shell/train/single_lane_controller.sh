#!/bin/bash

FLOW_DIR=${PWD}/../..
export PYTHONPATH="${PYTHONPATH}:${FLOW_DIR}"
export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8

MAIN_INFLOW=2000
# Merge vehicle placement
MERGE_INFLOW=200


for AVP in 30
do
	let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
	let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
	echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"


	python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/single_lane_controller.py \
		--exp_folder_mark single_lane_controller_horizon_2000_penality0.8_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP} \
		--cpu 48 \
		--to_probability \
		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
		--horizon 2000 \
		--num_training_iterations 250 \
		--eta1 0.9
done 
wait
source ~/notification_zyl.sh

#inflow_type=0
#python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/multiagent_lane_change_merge4_Collaborate_lrschedule.py \
#	--exp_folder_mark yulin${inflow_type} \
#	--lateral_resolution 3.2 \
#	--cpu 30 \
#	--to_probability \
#	--preset_inflow ${inflow_type} &
#
#inflow_type=1
#python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/multiagent_lane_change_merge4_Collaborate_lrschedule.py \
#	--exp_folder_mark yulin${inflow_type} \
#	--lateral_resolution 3.2 \
#	--cpu 30 \
#	--to_probability \
#	--preset_inflow ${inflow_type}


