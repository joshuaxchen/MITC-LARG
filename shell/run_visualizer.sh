#!/bin/bash
#CKPT_DIR=~/ray_results/flow/merge_4_Sim_Arrive_oldparams/PPO_MergePOEnvArrive-v0_918f4_00001_1_2021-01-08_16-24-19
CKPT_DIR=~/ray_results/flow/merge_4_Sim_Arrive_oldparams/PPO_MergePOEnvArrive-v0_314b0_00000_0_2021-04-24_20-26-00
#CKPT_DIR=~/ray_results/flow/merge_4_Sim_Arrive_reset_inflow_oldparams/PPO_MergePOEnvArrive-v0_aff88_00000_0_2021-04-18_17-59-10/
#CKPT_DIR=~/ray_results/flow/merge_4_Sim_Arrive_reset_inflow_oldparams/PPO_MergePOEnvArrive-v0_b4d2b_00002_2_2021-04-20_04-46-34
#CKPT=375
CKPT=500
MAIN_HUMAN_INFLOW=1800
MAIN_RL_INFLOW=200
MERGE_HUMAN_INFLOW=200

for MAIN_HUMAN_INFLOW in 1575
do
    for MAIN_RL_INFLOW in 175
    do
        for MERGE_HUMAN_INFLOW in 200
        do 
            python3 flow/visualize/new_rllib_visualizer.py \
                $CKPT_DIR \
                $CKPT \
                --render_mode no_render \
                --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_HUMAN_INFLOW \
                > merge4_arrive_fixed_rollout40_${MAIN_HUMAN_INFLOW}_${MAIN_RL_INFLOW}_$MERGE_HUMAN_INFLOW.txt
        done
    done
done

