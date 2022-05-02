#!/bin/bash

FLOW_DIR=${PWD}/../..
export PYTHONPATH="${PYTHONPATH}:${FLOW_DIR}"
export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8


# Even vehicle placement
MAIN_HUMAN=1
MAIN_RL=0
MERGE=1

python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/i696_multiagent.py \
        --window_size 300 300 \
        --cpu 10 \
        --i696 \
        --exp_folder_mark 'zyl' \
        --handset_inflow $MAIN_HUMAN $MAIN_RL $MERGE



#for AVP in 10 #30 50 80 100
#do
#	for MAIN_INFLOW in 1850 #1650 1850 2000 
#	do
#		let MAIN_RL_INFLOW=MAIN_INFLOW/AVP
#		let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#		echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"
#		python3 ${FLOW_DIR}/examples/rllib/stabilizing_i696.py \
#	done
#done


