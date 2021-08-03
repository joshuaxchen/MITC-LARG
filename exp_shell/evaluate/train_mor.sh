HUMAN_DIR=/home/users/flow_user/ray_results/human_multiagent_highway_merge4_MOR_Collaborate_lrschedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateMOR-v0_0573c_00000_0_2021-07-26_11-10-40
TRAIN_DIR=/home/users/yulin/ray_results/multiagent_highway_merge4_MOR_Collaborate_lrschedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateMOR-v0_56341_00000_0_2021-07-26_18-51-03

AAMAS_DIR=/home/users/yulin/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_740c0_00000_0_2021-07-04_14-31-39/

ON_OFF_RAMP_DIR=/home/users/yulin/ray_results/multiagent_highway_merge4_MOR_Collaborate_lrschedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateMOR-v0_aa661_00000_0_2021-07-27_15-31-47

FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results
WORKING_DIR=$EXP_FOLDER/mor/

CHCKPOINT=1


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

#python3 ../../flow/visualize/new_rllib_visualizer.py \
#	$HUMAN_DIR\
#	$CHCKPOINT \
#	--seed_dir $FLOW_DIR \
#	> ../../exp_results/human_mor/temp.txt 

#echo "PYTHONPATH=. python3 -m pudb.run ../../flow/visualize/new_rllib_visualizer.py $TRAIN_DIR $CHCKPOINT --agent_action_policy_dir ${AAMAS_DIR} --seed_dir $FLOW_DIR --render_mode no_render"
CHCKPOINT=500
# -m pudb.run 

for MERGE_INFLOW in 200
do
	for MAIN_INFLOW in 2000
	do
		for AVP in 10 # 1 2 3 4 5 6 7 8 9 10 12 14 16 18 20
		do
			let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
			let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW

			python3 $VISUALIZER \
				$ON_OFF_RAMP_DIR \
				$CHCKPOINT \
				--seed_dir $FLOW_DIR \
				--render_mode no_render \
				--avp_to_probability ${AVP} \
				--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
				> $WORKING_DIR/trainmor_EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}.txt 
		done 
	done
done

#--agent_action_policy_dir ${AAMAS_DIR} \

