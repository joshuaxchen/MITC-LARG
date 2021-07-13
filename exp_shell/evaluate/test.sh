#TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/hierarchy_based_on_aamas_full
#TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/aamas_full
declare -A TRAIN_DIR
declare -A MARK 


TRAIN_DIR[1]=${HOME}/ray_results/yulin_multiagent_Even_Avp10_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_d59fc_00000_0_2021-06-30_12-08-48
MARK[1]='1650_200_10'

TRAIN_DIR[2]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp10_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_803da_00000_0_2021-07-03_16-56-20 
MARK[2]='1850_200_10'


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

AVP=20
I=2
python3 $VISUALIZER ${TRAIN_DIR[$I]} $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --avp_to_probability $AVP 
# --handset_inflow 1485 165 200
#--avp_to_probability ${AVP} 

#mkdir ${FLOW_DIR}/exp_results/aamas_models
#for I in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
#do
#	echo "${TRAIN_DIR[$I]}"
#	mkdir ${FLOW_DIR}/exp_results/aamas_models/${MARK[$I]}
#	for AVP in 1 3 5 7 9 #2 4 6 8 10 20 30 40 50 60 70 80 100
#	do
#		echo "work"
#		echo "evaluate" ${TRAIN_DIR[$I]} ${MARK[$I]} "on AVP ${AVP}"
#		python3 $VISUALIZER ${TRAIN_DIR[$I]} $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/aamas_models/${MARK[$I]}/merge4_${MARK[$I]}_EAVP_${AVP}.txt &
#	done
#	if ((I==8)); then
#		wait
#	fi
#
#done

# || test $I -eq 8 || test $I -eq 12
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








