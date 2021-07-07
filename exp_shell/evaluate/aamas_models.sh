#TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/hierarchy_based_on_aamas_full
#TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/aamas_full
declare -A TRAIN_DIR
declare -A MARK 


TRAIN_DIR[1]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp10_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_d59fc_00000_0_2021-06-30_12-08-48'
MARK[1]='1650_200_10'

TRAIN_DIR[2]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp10_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_1cf3e_00000_0_2021-06-30_18-51-39' 
MARK[2]='2000_200_10'

# AVP30
TRAIN_DIR[3]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp30_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_ee3b1_00000_0_2021-06-30_18-43-11'
MARK[3]='1650_200_30'

TRAIN_DIR[4]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp30_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_d1a31_00000_0_2021-07-01_00-47-28'
MARK[4]='1850_200_30'


TRAIN_DIR[5]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_7c1f0_00000_0_2021-07-01_07-25-56'
MARK[5]='2000_200_30'


# AVP50
TRAIN_DIR[6]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp50_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_08b48_00000_0_2021-07-01_14-03-34'
MARK[6]='1650_200_50'


TRAIN_DIR[7]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp50_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_9a8de_00000_0_2021-07-01_21-45-47'
MARK[7]='1850_200_50'


TRAIN_DIR[8]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp50_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_77c29_00000_0_2021-07-02_05-58-43'
MARK[8]='2000_200_50'


# AVP80
TRAIN_DIR[9]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp80_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_f1df5_00000_0_2021-07-02_14-37-32'
MARK[9]='1650_200_80'

TRAIN_DIR[10]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp80_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_811d5_00000_0_2021-07-03_00-50-00'
MARK[10]='1850_200_80'

TRAIN_DIR[11]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp80_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_ba955_00000_0_2021-07-03_11-43-00'
MARK[11]='2000_200_80'

TRAIN_DIR[12]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp100_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_1d245_00000_0_2021-07-05_11-43-23'
MARK[12]='1650_200_100'

TRAIN_DIR[13]='/home/users/flow_user/ray_results/yulin_multiagent_Even_Avp100_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_8a7f3_00000_0_2021-07-01_16-08-53'
MARK[13]='2000_200_100'

# new 


#echo "curious: ${TRAIN_DIR[1]}"

CHCKPOINT=500

FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:$FLOW_DIR"
#${PWD}/$FLOW_DIR/
echo "set python path: $PYTHONPATH"

MERGE_INFLOW=200
echo "************************************************************"
#echo ${TRAIN_DIR[*]}
NUM=0

for I in 10 11 12 13
do
	echo "${TRAIN_DIR[$I]}"
	mkdir ~/yulin/MITC-LARGE/exp_results/aamas_models/${MARK[$I]}
	for AVP in 2 4 6 8 10 20 30 40 50 60 70 80 100
	do
		echo "evaluate" ${TRAIN_DIR[$I]} ${MARK[$I]} "on AVP ${AVP}"
		python3 $VISUALIZER ${TRAIN_DIR[$I]} $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/aamas_models/${MARK[$I]}/merge4_${MARK[$I]}_EAVP_${AVP}.txt &
		#let NUM=(NUM+1)
		#echo $NUM
		#if (($NUM>10))
		#then
		#	let NUM=(NUM-10)
		#	echo $NUM
		#	wait
		#fi
	done
	wait
done

#for AVP in 2 4 6 8 10 20 30 40 50 60 70 80 100
#do
#	python3 $VISUALIZER $TRAIN_DIR_1 $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/aamas_models/1650_200_10/merge4_1650_200_TAVP_10_EAVP_${AVP}.txt &
#	if
#done
#
#wait 
#
#for AVP in 40 50 60 70 80 100
#do
#	python3 $VISUALIZER $TRAIN_DIR_1 $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/aamas/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt &
#done
#


#for MAIN_INFLOW in 1300 1400 1500 1600 1700 1800 1900 2000 
#do
#	let MAIN_RL_INFLOW=MAIN_INFLOW/10
#	let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#	echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW 
#	python3 flow/visualize/new_rllib_visualizer.py \
#		$TRAIN_DIR_1 \
#       		$CHCKPOINT \
#		--render_mode no_render \
#		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
#		> ./exp_results/adaptive_headway/continous/main${MAIN_INFLOW}_merge200.txt &
#done
#
#wait 

#for MAIN_INFLOW in 1300 1400 1500 1600 1700 1800 1900 2000 
#do
#	let MAIN_RL_INFLOW=MAIN_INFLOW/10
#	let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#	echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW 
#	python3 flow/visualize/new_rllib_visualizer.py \
#		$TRAIN_DIR_2 \
#       		$CHCKPOINT \
#		--render_mode no_render \
#		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
#		> ./exp_results/adaptive_headway/discrete/main${MAIN_INFLOW}_merge200.txt &
#done
#
#wait
#
#for MAIN_INFLOW in 1300 1400 1500 1600 1700 1800 1900 2000 
#do
#	let MAIN_RL_INFLOW=MAIN_INFLOW/10
#	let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#	echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW 
#	python3 flow/visualize/new_rllib_visualizer.py \
#		$TRAIN_DIR_3 \
#       		$CHCKPOINT \
#		--render_mode no_render \
#		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
#		> ./exp_results/adaptive_headway/discrete_countahead/main${MAIN_INFLOW}_merge200.txt &
#done


#for AVP in 2 4 6 8 10 30 50 70 80 100
#do
#	python3 flow/visualize/new_rllib_visualizer.py $TRAIN_DIR_30 $CHCKPOINT --render_mode no_render --handset_avp ${AVP} >> ./avp_multi_agent/av30/merge4_2000_200_TAVP_30_EAVP_${AVP}.txt
#done

#for AVP in 10 20 30 40 50 70 80 100
#do
#	python3 flow/visualize/new_rllib_visualizer.py $TRAIN_DIR_50 $CHCKPOINT --render_mode no_render --handset_avp ${AVP} >> ./avp_multi_agent/av50/merge4_2000_200_TAVP_50_EAVP_${AVP}.txt
#done
#
#for AVP in 10 20 30 40 50 60 70 80 100
#do
#	python3 flow/visualize/new_rllib_visualizer.py $TRAIN_DIR_70 $CHCKPOINT --render_mode no_render --handset_avp ${AVP} >> ./avp_multi_agent/av70/merge4_2000_200_TAVP_70_EAVP_${AVP}.txt
#done
#
#for AVP in 10 20 30 40 50 60 70 80 90 100
#do
#	python3 flow/visualize/new_rllib_visualizer.py $TRAIN_DIR_90 $CHCKPOINT --render_mode no_render --handset_avp ${AVP} >> ./avp_multi_agent/av90/merge4_2000_200_TAVP_90_EAVP_${AVP}.txt
#done








