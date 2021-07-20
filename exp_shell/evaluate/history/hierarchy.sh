TRAIN_DIR_0=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/hierarchy_based_on_aamas_full
TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_densityahead_hierarchy_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4HierarchyDensityAhead-v0_f8425_00000_0_2021-07-17_23-09-38/

CHCKPOINT=1500

FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results
WORKING_FOLDER=$EXP_FOLDER/density_ahead_${CHCKPOINT}

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:$FLOW_DIR"
#${PWD}/$FLOW_DIR/
echo "set python path: $PYTHONPATH"

MERGE_INFLOW=200
mkdir $WORKING_FOLDER

J=0
for AVP in 1 #2 3 4 5 6 7 8 9 10 12 14 16 18 20 # 10 20 30 #40 50 60 70 80 100
do
	python3 $VISUALIZER $TRAIN_DIR_1 $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} --policy_dir $TRAIN_DIR_0 >> $WORKING_FOLDER/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt 
	let J=J+1
	if ((J == 10)); then   	
		wait
		let J=0
	fi
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








