#!/bin/bash
CKPT_DIR=~/ray_results/flow/merge_4_Sim_Arrive_oldparams/PPO_MergePOEnvArrive-v0_918f4_00001_1_2021-01-08_16-24-19
CKPT=375
MAIN_HUMAN_INFLOW=1800
MAIN_RL_INFLOW=200
MERGE_HUMAN_INFLOW=200

for MAIN_HUMAN_INFLOW in 1800 1575 2025
do
        MAIN_RL_INFLOW = MAIN_HUMAN_INFLOW/9 #200 175 225
        for MERGE_HUMAN_INFLOW in 225 175 200
        do 
            python3 flow/visualize/new_rllib_visualizer.py \
                $CKPT_DIR \
                $CKPT \
                --render_mode no_render \
                --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_HUMAN_INFLOW \
                > merge4_arrive_fixed_${MAIN_HUMAN_INFLOW}_${MAIN_RL_INFLOW}_$MERGE_HUMAN_INFLOW.txt
            
    done
done

