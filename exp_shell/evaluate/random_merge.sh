FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results/random_merge

POLICY_DIR1=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_740c0_00000_0_2021-07-04_14-31-39
MARK='2000_200_30'

# Random merge inflow
POLICY_DIR2=${HOME}/ray_results/Random_all_placement_Avp30_Main2000_Merge300_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_4f5ed_00000_0_2021-09-14_19-03-09

# Random merge inflow with multiple merge infor
POLICY_DIR3=${HOME}/ray_results/Random_merge_placement_augmented_Avp30_Main2000_Merge300_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4RandomMergeCollaborate-v0_adc6a_00000_0_2021-09-15_17-24-23

# Random merge inflow with multiple merge infor
POLICY_DIR4=${HOME}/ray_results/Random_merge_placement_augmented_Avp30_Main2000_Merge200_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4RandomMergeCollaborate-v0_ef596_00000_0_2021-09-15_20-03-42

# Random merge inflow with multiple merge infor and reversed rl dist
POLICY_DIR5=${HOME}/ray_results/Random_modified_state_merge_placement_augmented_Avp30_Main2000_Merge300_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4RandomMergeModifyDistCollaborate-v0_54c0f_00000_0_2021-09-15_23-41-17


# Even merge inflow with multiple merge infor and reversed rl dist
POLICY_DIR6=${HOME}/ray_results/Even_modified_state_merge_placement_augmented_Avp30_Main2000_Merge200_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4RandomMergeModifyDistCollaborate-v0_435cb_00000_0_2021-09-16_02-32-36

TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_cbf62_00000_0_2021-09-12_15-41-25


TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_157ce_00000_0_2021-09-12_21-55-42


TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_a3705_00000_0_2021-09-13_10-09-49

# window left and right
TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_1d079_00000_0_2021-09-13_15-13-51

# fix length
TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_db37f_00000_0_2021-09-13_19-15-24

# simple merge
TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_e2773_00000_0_2021-09-13_19-29-55


CHCKPOINT=501


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

mkdir ${EXP_FOLDER}
RIGHT_MAIN_INFLOW=2000


MAIN_INFLOW=2000
AVP=5 #200 400 600 800 # 200 400 600 800 # 200 400 600 800
J=0

CHCKPOINT=500
WINDOW_LEFT=-1

WORKING_DIR=$EXP_FOLDER/2000_200_30
mkdir ${WORKING_DIR}

MERGE_INFLOW=200
for RAND_MERGE_PROB in 2 #4 6 8 10 15 20 30 40
do
	for AVP in 10  #2 4 6 8 10 20 30 40
	do
		let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
		let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
		echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"

		python3 $VISUALIZER \
			$POLICY_DIR5 \
			$CHCKPOINT \
			--seed_dir $FLOW_DIR \
			--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
			--merge_random_inflow_percentage ${RAND_MERGE_PROB} \
			--render_mode no_render \
			#>> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${RAND_MERGE_PROB}.txt &
			#--main_merge_human_inflows 2000 300 \
			#--to_probability \
	done
done

#for RAND_MERGE_PROB in 2 4 6 8 10 15 20 30 40
#do
#	for AVP in 0  #2 4 6 8 10 20 30 40
#	do
#		let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
#		let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#		echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"
#
#		python3 $VISUALIZER \
#			$POLICY_DIR5 \
#			$CHCKPOINT \
#			--seed_dir $FLOW_DIR \
#			--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
#			--merge_random_inflow_percentage ${RAND_MERGE_PROB} \
#			--render_mode no_render \
#			>> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${RAND_MERGE_PROB}.txt &
#			#--main_merge_human_inflows 2000 300 \
#			#--to_probability \
#	done
#done


wait

source ~/notification_zyl.sh
