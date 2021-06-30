#!/bin/bash

# Set up environment avariables like PATH, SUMO_HOME
source ~/.bashrc
echo "set up environment variable"

# Activate conda environment
conda activate flow_test
echo "activate flow_test"

#######################################################
' 
Please do not change the command below. 
First obtain the number of cpus from input (condor sub)
Stop exitence ray process to avoid confliction
Create rollout workers
Start ray and initiate rollout workers
' 
# START HERE
MACHINE_PROC=$1
echo "request number of cpus: $MACHINE_PROC"
NPROC="$((MACHINE_PROC-1))"
echo "number of workers: $NPROC" 
ray stop
echo "start ray" 
ray start --head --node-ip-address=127.0.0.1 --redis-password="mitc_flow" --port 6379 --num-cpus $MACHINE_PROC
# END HERE
#######################################################

# Obtain path to MITC directory relative to condor_jobs
FLOW_DIR=${PWD}/..
export PYTHONPATH="${PYTHONPATH}:${FLOW_DIR}"
export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8


# Even vehicle placement
MERGE_INFLOW=200

for AVP in 10 #30 50 80 100
do
	for MAIN_INFLOW in 1850 #1650 1850 2000 
	do
		let MAIN_RL_INFLOW=MAIN_INFLOW/AVP
		let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
		echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"
		python3 ${FLOW_DIR}/examples/rllib/multiagent_exps/condor_multiagent_merge4_Merge4_Collaborate_lrschedule.py \
		--avp ${AVP} \
		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
		--exp_folder_mark Even_Avp${AVP}_Main${MAIN_INFLOW}_Merge${MERGE_INFLOW}
	done
done

#######################################################
' 
Please do not change below. 
Stop ray
'
ray stop
echo "stop ray" 
#######################################################


