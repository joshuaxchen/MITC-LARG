FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results/new_window_size

# merge 200

TRAIN_DIR_1=${HOME}/ray_results/Even_placement_PostAAMAS_Avp10_Main2000_Merge200_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_d7953_00000_0_2021-10-20_11-07-36

TRAIN_DIR_2=${HOME}/ray_results/Random_placement_PostAAMAS_Avp10_Main2000_Merge200_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_7fc47_00000_0_2021-10-20_11-05-09

TRAIN_DIR_3=${HOME}/AAAI_Results/Distributed_5TupleCDM_e1=0.8_e2=0.2/best/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_2be0d_00001_1_2021-01-19_17-48-51

TRAIN_DIR_4=${HOME}/ray_results/multiagent_normalized_distance_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateNormalizedToDistance-v0_9bd30_00000_0_2021-10-23_16-45-58

TRAIN_DIR_5=${HOME}/ray_results/multiagent_normalized_time_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateNormalizedToTime-v0_a712e_00000_0_2021-10-23_20-56-50

TRAIN_DIR_6=${HOME}/ray_results/multiagent_normalized_time_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateNormalizedToTime-v0_92974_00000_0_2021-10-24_15-25-47

CHCKPOINT=500


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

mkdir ${EXP_FOLDER}

WORKING_DIR=$EXP_FOLDER/long_merge
mkdir ${WORKING_DIR}

J=0

MERGE_INFLOW=200
MAIN_INFLOW=2000

WINDOW_RIGHT=0

for WINDOW_LEFT in 200 #400 600 800 1000 #100 200 300 400 500 600 700 800 900 1000
do
	AVP=10 
	let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
	let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
	echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"
	python3 $VISUALIZER \
		$TRAIN_DIR_5 \
		$CHCKPOINT \
		--seed_dir $FLOW_DIR \
		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
		--render_mode sumo_gui
		#>> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${WINDOW_LEFT}.txt &
	 	#--print_metric_per_time_step_in_file ${PWD}/longmerge_human \
		#--window_size ${WINDOW_LEFT} ${WINDOW_RIGHT} \
		#--to_probability \
		#--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
		#--horizon 4000 \
		#--i696 \


	done


wait 
source ~/notification_zyl.sh

