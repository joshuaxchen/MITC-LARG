#TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/hierarchy_based_on_aamas_full
#TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/aamas_full
declare -A TRAIN_DIR
declare -A MARK 


TRAIN_DIR[1]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp10_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_b6165_00000_0_2021-07-03_10-52-46
MARK[1]='1650_200_10'
AVPS[1]=10

TRAIN_DIR[2]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp10_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_803da_00000_0_2021-07-03_16-56-20 
MARK[2]='1850_200_10'
AVPS[2]=10

# AVP30
TRAIN_DIR[3]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp10_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_74d88_00000_0_2021-07-03_21-20-52
MARK[3]='2000_200_10'
AVPS[3]=10
###############

TRAIN_DIR[4]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_a9c72_00000_0_2021-07-04_01-25-44
MARK[4]='1650_200_30'
AVPS[4]=30


TRAIN_DIR[5]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_0a35b_00000_0_2021-07-04_07-54-59
MARK[5]='1850_200_30'
AVPS[5]=30


TRAIN_DIR[6]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_740c0_00000_0_2021-07-04_14-31-39
MARK[6]='2000_200_30'
AVPS[6]=30


TRAIN_DIR[7]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp50_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_6328a_00000_0_2021-07-04_21-04-53
MARK[7]='1650_200_50'
AVPS[7]=50

TRAIN_DIR[8]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp50_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_6fb5c_00000_0_2021-07-05_05-40-37
MARK[8]='1850_200_50'
AVPS[8]=50


TRAIN_DIR[9]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp50_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_3688f_00000_0_2021-07-05_14-07-16
MARK[9]='2000_200_50'
AVPS[9]=50

##############
TRAIN_DIR[10]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp80_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_5a6ae_00000_0_2021-07-04_01-52-09
MARK[10]='1650_200_80'
AVPS[10]=80


TRAIN_DIR[11]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp80_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_2ad89_00000_0_2021-07-04_11-52-07
MARK[11]='1850_200_80'
AVPS[11]=80

########new############
TRAIN_DIR[12]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp80_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_cb311_00000_0_2021-07-07_12-50-18
MARK[12]='2000_200_80'
AVPS[12]=80
# already have

TRAIN_DIR[13]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp100_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_e4471_00000_0_2021-07-07_15-07-01
MARK[13]='1650_200_100'
AVPS[13]=100
# already have

TRAIN_DIR[14]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp100_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_54bf7_00000_0_2021-07-07_16-28-54
MARK[14]='1850_200_100'
AVPS[14]=100
# dr-wily

TRAIN_DIR[15]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp100_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_56c3a_00000_0_2021-07-07_23-38-27
MARK[15]='2000_200_100'
AVPS[15]=100
# dr-light 




#echo "curious: ${TRAIN_DIR[1]}"

CHCKPOINT=500

FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results
WORKING_DIR=${EXP_FOLDER}/aamas_models_random_inflow

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:$FLOW_DIR"
#${PWD}/$FLOW_DIR/
echo "set python path: $PYTHONPATH"

MERGE_INFLOW=200
echo "************************************************************"
#echo ${TRAIN_DIR[*]}
NUM=0


MERGE_INFLOW=200
mkdir ${WORKING_DIR}
for I in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
	echo "${TRAIN_DIR[$I]}"
	mkdir ${WORKING_DIR}/${MARK[$I]}
	for MAIN_INFLOW in 1600 1650 1700 1750 1800 1850 1900 1950 
	do
		let MAIN_RL_INFLOW=MAIN_INFLOW*${AVPS[$I]}/100
		let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
		echo "evaluate" ${TRAIN_DIR[$I]} ${MARK[$I]} "on AVP ${AVP}"
		echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW
		python3 $VISUALIZER ${TRAIN_DIR[$I]} $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW >> ${WORKING_DIR}/${MARK[$I]}/merge4_EVAL_${MAIN_INFLOW}_$MERGE_INFLOW.txt &
	done
	if ((I == 4 || I==8 || I==12)); then
		wait
	fi
done



