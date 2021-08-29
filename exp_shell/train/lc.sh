#!/bin/bash

FLOW_DIR=${PWD}/../..
export PYTHONPATH="${PYTHONPATH}:${FLOW_DIR}"
export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8


# Even vehicle placement
MERGE_INFLOW=200

RIGHT_MAIN_INFLOW=2000

RIGHT_MAIN_INFLOW=2000  # 1800 #1900 2000 2100 2200 # 1800 1900 2000 2100 2200 #1800 1900 #
LEFT_MAIN_INFLOW=2000  # 1800 #1900 2000 2100 2200 # 1800 1900 2000 2100 2200 #1800 1900 #
AVP=10 #200 400 600 800 # 200 400 600 800 # 200 400 600 800
let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW

RL_RIGHT_LEFT=1
if ((RL_RIGHT_LEFT == 0)); then # rl on the right
	RL_INFLOW_LEFT=0
	let RL_INFLOW_RIGHT=RIGHT_MAIN_INFLOW*${AVP}/100
else # otherwise, rl vehicles on the left
	let RL_INFLOW_LEFT=LEFT_MAIN_INFLOW*${AVP}/100
	RL_INFLOW_RIGHT=0
fi
let HUMAN_INFLOW_LEFT=LEFT_MAIN_INFLOW-RL_INFLOW_LEFT
let HUMAN_INFLOW_RIGHT=RIGHT_MAIN_INFLOW-RL_INFLOW_RIGHT
echo ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} 
echo ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}

RIGHT_HUMAN_LANE_CHANGE=1
AGGRESSIVE=1 #0.2 0.4 0.6 0.8 1
ASSERTIVE=1 #0.5 #5 #0.4 0.6 0.8 1
LC_PROB=0.6
python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/multiagent_lane_change_merge4_Collaborate_lrschedule.py \
	--exp_folder_mark yulin_rl_left \
	--lateral_resolution 3.2 \
	--cpu 20 \
	--to_probability \
	--human_inflows ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}\
	--rl_inflows ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} \
	--human_lane_change ${RIGHT_HUMAN_LANE_CHANGE} 0 \
	--rl_lane_change 0 0 \
	--merge_inflow ${MERGE_INFLOW} \
	--aggressive ${AGGRESSIVE} \
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


