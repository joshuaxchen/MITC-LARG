FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results/window_size

POLICY_DIR=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_740c0_00000_0_2021-07-04_14-31-39
MARK='2000_200_30'

TRAIN_DIR=${HOME}/ray_results/multiagent_yulin_window_size_long_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate-v0_cbf62_00000_0_2021-09-12_15-41-25

CHCKPOINT=500


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

mkdir ${EXP_FOLDER}
RIGHT_MAIN_INFLOW=2000

WORKING_DIR=$EXP_FOLDER/trial_2
mkdir ${WORKING_DIR}


MERGE_INFLOW=200
MAIN_INFLOW=2000
AVP=10 #200 400 600 800 # 200 400 600 800 # 200 400 600 800
J=0
let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
echo "Avp:${AVP}, Inflows:${MAIN_HUMAN_INFLOW} ${MAIN_RL_INFLOW} ${MERGE_INFLOW}"

for WINDOW_SIZE in 600 #500 600 700 
do 
	python3 $VISUALIZER \
		$POLICY_DIR \
		$CHCKPOINT \
		--seed_dir $FLOW_DIR \
		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
		--to_probability \
		--render_mode no_render \
		>> ${WORKING_DIR}/EVAL_no_window_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}.txt 
		# --window_size ${WINDOW_SIZE} \
	let J=J+1
	if ((J == 30)); then
		wait
		let J=0
		echo "another batch"
	fi

done

wait 
source ~/notification_zyl.sh

