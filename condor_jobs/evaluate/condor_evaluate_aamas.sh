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

TRAIN_DIR_1=~/ray_results/yulin_multiagent_Even_Avp100_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_8a7f3_00000_0_2021-07-01_16-08-53
VISUALIZER="${FLOW_DIR}/flow/visualize/condor_rllib_visualizer.py"
EXP_FOLDER="${FLOW_DIR}/exp_results"

CHCKPOINT=500

# Even vehicle placement
MERGE_INFLOW=200

for AVP in 10 #20 30 40 50 60 70 80 90 100
do
	python3 $VISUALIZER $TRAIN_DIR_1 $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/aamas/2000_200/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt 
done

wait 

#######################################################
' 
Please do not change below. 
Stop ray
'
ray stop
echo "stop ray" 
#######################################################


