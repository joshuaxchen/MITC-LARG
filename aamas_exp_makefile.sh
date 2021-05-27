#!/bin/bash
BENCHMARK=./flow/benchmarks
PPO_RUNNER=${BENCHMARK}/rllib/ppo_runner.py	
RUN=python
CPU_NUM=1
LR=5e-5
NUM_ROLLOUTS=20

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}"

echo "************************************************************"
echo "run a centralized experiment on simple merge to train agents" 
echo "with original reward, outflow, average speeds***************" 
echo "************************************************************"

echo "1st exp: train agent with original reward"
${RUN} ${PPO_RUNNER} --benchmark_name merge4_Sim_Arrive_All_RL --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} --memory 2 

#echo "2nd exp: train agent with reward as the number of departing vehicles (outflow)"
#${SETPATH} ${RUN} ${PPO_RUNNER} --benchmark_name merge4_Sim_Arrive --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} --memory 2
#
#echo "3rd exp: train agent with reward as the average speeds of vehicles in the network"
#${SETPATH} ${RUN} ${PPO_RUNNER} --benchmark_name merge4_Sim_AvgVel --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} 

#echo "***********************************************************"
#echo "run a centralized experiment on I696 to train agents with  " 
#echo "outflow, average speeds from scratch***********************" 
#echo "***********************************************************"
#
#echo "1st exp: train with outflow reward in window from scratch"
#${SETPATH} ${RUN} ${PPO_RUNNER} --benchmark_name 1merge_Window_transfer_Arrive --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} 
#
#echo "2nd exp: train with avg speed reward in window from scratch"
#${SETPATH} ${RUN} ${PPO_RUNNER} --benchmark_name 1merge_Window_transfer_AvgVel --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} 
#
#echo "3rd exp: train with outflow reward in the entire network from scratch"
#${SETPATH} ${RUN} ${PPO_RUNNER} --benchmark_name 1merge_horizon2000_warmup0_simstep05_flow2000_merge200_dePart10_Arrive --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} 
#
#
#echo "4th exp: train with avg speed reward in the entire network from scratch"
#${SETPATH} ${RUN} ${PPO_RUNNER} --benchmark_name 1merge_horizon2000_warmup0_simstep05_flow2000_merge200_dePart10_AvgVel --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} 
