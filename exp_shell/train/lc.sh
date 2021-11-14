#!/bin/bash

FLOW_DIR=${PWD}/../..
export PYTHONPATH="${PYTHONPATH}:${FLOW_DIR}"
export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8

# Even vehicle placement
MERGE_INFLOW=200
RIGHT_MAIN_INFLOW=2000
LEFT_MAIN_INFLOW=1600

AVP_LEFT=0
AVP_RIGHT=30 

let RL_INFLOW_LEFT=LEFT_MAIN_INFLOW*${AVP_LEFT}/100
let HUMAN_INFLOW_LEFT=LEFT_MAIN_INFLOW-RL_INFLOW_LEFT

let RL_INFLOW_RIGHT=RIGHT_MAIN_INFLOW*${AVP_RIGHT}/100
let HUMAN_INFLOW_RIGHT=RIGHT_MAIN_INFLOW-RL_INFLOW_RIGHT

echo ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} 
echo ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}

SPEED_GAIN=0 #0.2 0.4 0.6 0.8 1
ASSERTIVE=1 #0.5 #5 #0.4 0.6 0.8 1
LC_PROB=-1

python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/multiagent_lane_change_merge4_Collaborate_lrschedule.py \
	--exp_folder_mark new_rl_right \
	--lateral_resolution 3.2 \
	--cpu 30 \
	--to_probability \
	--human_inflows ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}\
	--rl_inflows ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} \
	--human_lane_change 1 1 \
	--rl_lane_change 0 0 \
	--merge_inflow ${MERGE_INFLOW} \
	--speed_gain ${SPEED_GAIN} \
	--assertive ${ASSERTIVE} \
	--lc_probability ${LC_PROB} 

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


