FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results/new_window_size

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
ENV_DIR=${HOME}/ray_results/zyl_window_size_test/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_f86a2_00000_0_2022-05-04_17-17-22/

# controller trained under different road length
POLICY_DIR_1=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen600_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_14c1a_00000_0_2022-05-03_21-01-15/
POLICY_DIR_2=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen700_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_771ea_00000_0_2022-05-03_22-01-16/
POLICY_DIR_3=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen800_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_cc339_00000_0_2022-05-03_23-00-55/
POLICY_DIR_4=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen900_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_32694_00000_0_2022-05-04_00-08-12/
POLICY_DIR_5=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen1000_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_7bc42_00000_0_2022-05-03_21-04-08/
POLICY_DIR_6=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen1100_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_6246b_00000_0_2022-05-03_22-22-10/
POLICY_DIR_7=${HOME}/may4/multiagent_single_lane_single_lane_controller_highwaylen1200_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_342d7_00000_0_2022-05-03_23-32-27/

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

mkdir ${EXP_FOLDER}

WORKING_DIR=$EXP_FOLDER/long_merge_1
mkdir ${WORKING_DIR}

J=0

MERGE_INFLOW=200
MAIN_INFLOW=2000
CHCKPOINT=1

WINDOW_RIGHT=100
WINDOW_ABOVE=200

render='sumo_gui'

for WINDOW_LEFT in 400 #200 400 600 800 1000 #100 200 300 400 500 600 700 800 900 1000
do
	AVP=0 
	let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
	let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
	echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"
	python3 $VISUALIZER \
		$ENV_DIR \
		$CHCKPOINT \
        --agent_action_policy_dir $POLICY_DIR_1 \
		--seed_dir $FLOW_DIR \
		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
		--to_probability \
		--horizon 3000 \
		--highway_len 600 \
        --cpu 10 \
		--window_size ${WINDOW_LEFT} ${WINDOW_RIGHT} ${WINDOW_ABOVE} \
		--render_mode ${render} 
		# >> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${WINDOW_LEFT}.txt &

done

wait 
source ~/notification_zyl.sh

