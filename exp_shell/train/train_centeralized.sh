#!/bin/bash
BENCHMARK=../flow/benchmarks
PPO_RUNNER=${BENCHMARK}/rllib/ppo_runner.py	
RUN=python
CPU_NUM=11
LR=5e-5
NUM_ROLLOUTS=20

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../"

echo "************************************************************"
echo "run a centralized experiment on simple merge to train agents" 
echo "with original reward, outflow, average speeds***************" 
echo "************************************************************"

echo "1st exp: train agent with original reward"
${RUN} ${PPO_RUNNER} --benchmark_name merge4_adaptive_headway --num_cpus ${CPU_NUM} --lr ${LR} --num_rollouts ${NUM_ROLLOUTS} 

