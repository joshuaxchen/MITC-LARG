TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/continuous_adaptive_headway_avp10_main2000_merge200_maxheadway20
TRAIN_DIR_2=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/adaptive_discrete_action_avp10_main2000_merge200_maxheadway20
TRAIN_DIR_3=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/adaptive_headway_count_ahead_fixed_action_avp10_main2000_merge200_maxheadway20
TRAIN_DIR_4=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/adaptive_headway_continous_act_penality_main2000_merge200_maxheadway10
#TRAIN_DIR_30=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_30
#TRAIN_DIR_50=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_50
#TRAIN_DIR_70=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_70
#TRAIN_DIR_90=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_90

TRAIN_DIR_5=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/penality
TRAIN_DIR_6=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/adaptive_headway_penality_main2000_merge200_avp10_maxheadway50
TRAIN_DIR_7=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/new_adaptive_headway_avp10_main2000_merge200_maxheadway50

#TRAIN_DIR_100=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_ac09e_00000_0_2021-05-26_02-04-54 

TRAIN_DIR_Centralizd=/home/users/flow_user/ray_results/yulin_centeralized_adaptive_headway_binary/PPO_MergePOEnvAdaptiveHeadway-v0_0dd89_00000_0_2021-06-13_11-47-35
TRAIN_DIR_Binary=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/binary

CHCKPOINT=500

FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:$FLOW_DIR"
#${PWD}/$FLOW_DIR/
echo "set python path: $PYTHONPATH"

MERGE_INFLOW=200

#for MAIN_INFLOW in 1300 1400 1500 1600 1700 1800 1900 2000 
#do
#	let MAIN_RL_INFLOW=MAIN_INFLOW/10
#	let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#	echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW 
#	python3 flow/visualize/new_rllib_visualizer.py \
#		$TRAIN_DIR_Binary \
#       		$CHCKPOINT \
#		--render_mode no_render \
#		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
#		> ./exp_results/adaptive_headway/binary/main${MAIN_INFLOW}_merge200.txt &
#done

for AVP in 2 4 6 8 10 20 30 #40 50 60 70 80 100
do
	python3 $VISUALIZER $TRAIN_DIR_7 $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/adaptive_headway/new_adaptive_avp10_max50/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt &
done

wait 

for AVP in 40 50 60 70 80 100
do
	python3 $VISUALIZER $TRAIN_DIR_7 $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/adaptive_headway/new_adaptive_avp10_max50/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt &
done



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








