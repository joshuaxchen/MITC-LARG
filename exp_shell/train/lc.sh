#!/bin/bash

FLOW_DIR=${PWD}/../..
export PYTHONPATH="${PYTHONPATH}:${FLOW_DIR}"
export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8


# Even vehicle placement
MERGE_INFLOW=200


python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/multiagent_lane_change_merge4_Collaborate_lrschedule.py --exp_folder_mark yulin
#python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/multiagent_merge4_Merge4_Collaborate_lrschedule.py
#--exp_folder_mark yulin

#for AVP in 10 #30 50 80 100
#do
#	for MAIN_INFLOW in 1850 #1650 1850 2000 
#	do
#		let MAIN_RL_INFLOW=MAIN_INFLOW/AVP
#		let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#		echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"
#		python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/multiagent_merge4_Merge4_Collaborate_lrschedule.py \
#		--avp ${AVP} \
#		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
#		--exp_folder_mark Even_Avp${AVP}_Main${MAIN_INFLOW}_Merge${MERGE_INFLOW}
#	done
#done


