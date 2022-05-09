FLOW_DIR=${PWD}/../..
#VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
VISUALIZER=$FLOW_DIR/flow/visualize/parallized_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results/

POLICY_DIR=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_740c0_00000_0_2021-07-04_14-31-39
MARK='2000_200_30'

TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_cbf62_00000_0_2021-09-12_15-41-25


TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_157ce_00000_0_2021-09-12_21-55-42


TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_a3705_00000_0_2021-09-13_10-09-49

# window left and right
TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_1d079_00000_0_2021-09-13_15-13-51

# fix length
TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_db37f_00000_0_2021-09-13_19-15-24

# simple merge
TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_e2773_00000_0_2021-09-13_19-29-55

# simple merge - even merge inflow
TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_42633_00000_0_2021-09-21_11-09-11
CHCKPOINT=501

# long simple merge - even merge inflow - horizon=3000
TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_real_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_cab41_00000_0_2021-09-21_20-52-49

# long simple merge - even merge inflow - horizon=5000
TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_real_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_c1370_00000_0_2021-09-21_21-06-52


TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_f6fa1_00000_0_2021-10-17_23-57-59

# merge 200
TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_7e284_00000_0_2021-10-18_16-36-45
CHCKPOINT=501

# environment for window test
ENV_DIR=${HOME}/may4/zyl_window_size_test/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_1a367_00000_0_2022-05-04_18-22-44/

# controller trained under different road length
declare -A WINDOW_LEFT 
declare -A POLICY 
declare -A HIGHWAY_LEN 
POLICY[1]=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen600_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_14c1a_00000_0_2022-05-03_21-01-15/
WINDOW_LEFT[1]=522.6
HIGHWAY_LEN[1]=600
POLICY[2]=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen700_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_771ea_00000_0_2022-05-03_22-01-16/
WINDOW_LEFT[2]=622.6
HIGHWAY_LEN[2]=700
POLICY[3]=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen800_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_cc339_00000_0_2022-05-03_23-00-55/
WINDOW_LEFT[3]=722.6
HIGHWAY_LEN[3]=800
POLICY[4]=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen900_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_32694_00000_0_2022-05-04_00-08-12/
WINDOW_LEFT[4]=822.6
HIGHWAY_LEN[4]=900
POLICY[5]=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen1000_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_7bc42_00000_0_2022-05-03_21-04-08/
WINDOW_LEFT[5]=922.6
HIGHWAY_LEN[5]=1000
POLICY[6]=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen1100_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_6246b_00000_0_2022-05-03_22-22-10/
WINDOW_LEFT[6]=1022.6
HIGHWAY_LEN[6]=1100
POLICY[7]=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen1200_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_342d7_00000_0_2022-05-03_23-32-27/
WINDOW_LEFT[7]=1122.6
HIGHWAY_LEN[7]=1200

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

mkdir ${EXP_FOLDER}


J=0

MERGE_INFLOW=200
MAIN_INFLOW=2000
CHCKPOINT=1

WINDOW_RIGHT=100
WINDOW_ABOVE=200

render='no_render'

#for WINDOW_LEFT in 522.6 #200 400 600 800 1000 #100 200 300 400 500 600 700 800 900 1000

AVP=10 
J=0
for horizon in 8000
do
    for measurement in 2000
    do
        WORKING_DIR=$EXP_FOLDER/may10_window_size_${horizon}_${measurement}
        mkdir ${WORKING_DIR}
        for MERGE_LEN in 200 300 400 500 
        do 
            for I in 1 3 #2 3 4 5 6 7 
            do
                let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
                let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
                echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"
                python3 $VISUALIZER \
                    $ENV_DIR \
                    $CHCKPOINT \
                    --agent_action_policy_dir ${POLICY[$I]} \
                    --seed_dir $FLOW_DIR \
                    --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
                    --to_probability \
                    --horizon ${horizon} \
                    --measurement_rate ${measurement} \
                    --highway_len ${HIGHWAY_LEN[7]} ${MERGE_LEN} \
                    --window_size ${WINDOW_LEFT[$I]} ${WINDOW_RIGHT} ${WINDOW_ABOVE} \
                    --print_metric_per_time_step_in_file metrics \
                    --cpu 50 \
                    --render_mode ${render} \
                    >> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${HIGHWAY_LEN[7]}_${MERGE_LEN}.txt  
                    #>> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${WINDOW_LEFT[$I]}_${HIGHWAY_LEN[7]}.txt  
                    # --krauss_controller \
                    #--print_metric_per_time_step_in_file metrics \
                    #--print_vehicles_per_time_step_in_file ${HIGHWAY_LEN[7]}_${AVP} \

                #AVP=10 
                #let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
                #let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
                #echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"
                #python3 $VISUALIZER \
                #	${POLICY[$I]} \
                #	150 \
                #	--seed_dir $FLOW_DIR \
                #	--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
                #	--to_probability \
                #	--highway_len ${HIGHWAY_LEN[7]} \
                #    --krauss_controller \
                #	--horizon 3000 \
                #    --cpu 10 \
                #	--render_mode ${render} 
                #	# >> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${WINDOW_LEFT}.txt &
                #    # --krauss_controller \

            done
        done
    done
done

wait 
source ~/notification_zyl.sh

