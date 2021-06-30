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


for AVP in 10 
do
    python3 ~/flow/MITC/examples/rllib/multiagent_exps/condor_multiagent_merge4_Collaborate_lrschedule.py --avp ${AVP}
done


#######################################################
' 
Please do not change below. 
Stop ray
'
ray stop
echo "stop ray" 
#######################################################


