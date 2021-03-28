#!/bin/bash
BENCHMARK=./flow/benchmarks
PPO_RUNNER=${BENCHMARK}/rllib/ppo_runner.py	
RUN=python
CPU_NUM=1
LR=5e-5
NUM_ROLLOUTS=2

echo "*******************************************************************************"
echo "run a centralized experiment to train agents with original reward, number of departed vehicles, average speeds" 
echo "*******************************************************************************"

echo "1st exp: train agent with original reward"
${RUN} ${PPO_RUNNER} --benchmark_name merge4_Sim --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} 

echo "2nd exp: train agent with reward as the number of departing vehicles"
${RUN} ${PPO_RUNNER} --benchmark_name merge4_Sim_Arrive --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} 

echo "3rd exp: train agent with reward as the average speeds of vehicles in the network"
${RUN} ${PPO_RUNNER} --benchmark_name merge4_Sim_AvgVel --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} 

#python rllib/ppo_runner.py --benchmark_name merge4_Sim --num_cpus number_of_cores --lr 5e-5 --num_rollouts 20

