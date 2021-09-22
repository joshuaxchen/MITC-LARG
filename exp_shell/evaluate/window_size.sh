FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results/window_size

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


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

mkdir ${EXP_FOLDER}

WORKING_DIR=$EXP_FOLDER/simple_merge
mkdir ${WORKING_DIR}

J=0

MERGE_INFLOW=200
MAIN_INFLOW=2000
CHCKPOINT=501

WINDOW_RIGHT=0

for WINDOW_LEFT in 100 #200 300 400 500 600 700 800
do
	#AVP=10 
	#let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
	#let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
	#echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"
	#python3 $VISUALIZER \
	#	$TRAIN_DIR \
	#	$CHCKPOINT \
	#	--seed_dir $FLOW_DIR \
	#	--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
	#	--to_probability \
	#	--print_metric_per_time_step_in_file ${PWD}/longmerge \
	#	--window_size ${WINDOW_LEFT} ${WINDOW_RIGHT} \
	#	--render_mode no_render \
	#	>> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${WINDOW_LEFT}.txt &

	AVP=0 
	let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
	let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
	echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"
	python3 $VISUALIZER \
		$TRAIN_DIR \
		$CHCKPOINT \
		--seed_dir $FLOW_DIR \
		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
		--to_probability \
		--window_size ${WINDOW_LEFT} ${WINDOW_RIGHT} \
	 	--print_metric_per_time_step_in_file ${PWD}/longmerge \
		--render_mode no_render 
		#>> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${WINDOW_LEFT}.txt &
done


wait 
source ~/notification_zyl.sh

