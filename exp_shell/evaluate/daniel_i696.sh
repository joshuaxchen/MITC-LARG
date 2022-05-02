FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results/i696_random

# merge 200

TRAIN_DIR_i696=${HOME}/ray_results/yulin_stabilizing_i696/PPO_MergePOEnv-v0_9a4a5_00000_0_2022-04-28_12-42-41
# daniel's i696
TRAIN_DIR_i696=${HOME}/ray_results/i696_window_size_300_300/PPO_MultiAgentI696POEnvParameterizedWindowSizeCollaborate-v0_e3194_00000_0_2022-04-29_22-16-12/
# single_lane i696
#TRAIN_DIR_i696=${HOME}/ray_results/i696_window_size_300_300/PPO_MultiAgentI696POEnvParameterizedWindowSizeCollaborate-v0_80a69_00000_0_2022-04-30_00-07-58/
TRAIN_DIR_i696=${HOME}/ray_results/zyl_i696_window_size_300_300/PPO_MultiAgentI696POEnvParameterizedWindowSizeCollaborate-v0_25204_00000_0_2022-05-01_20-13-59/

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

CHCKPOINT=1

MAIN_HUMAN=3000
MAIN_RL=1000
MERGE=1000
python3 $VISUALIZER \
            $TRAIN_DIR_i696 \
            $CHCKPOINT \
            --seed_dir $FLOW_DIR \
            --horizon 4000 \
            --render_mode sumo_gui \
            --i696 \
            --handset_inflow $MAIN_HUMAN $MAIN_RL $MERGE

wait 

source ~/notification_zyl.sh

