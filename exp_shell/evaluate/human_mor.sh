HUMAN_DIR=/home/users/flow_user/ray_results/human_multiagent_highway_merge4_MOR_Collaborate_lrschedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateMOR-v0_0573c_00000_0_2021-07-26_11-10-40
TRAIN_DIR=/home/users/yulin/ray_results/multiagent_highway_merge4_MOR_Collaborate_lrschedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateMOR-v0_56341_00000_0_2021-07-26_18-51-03

FLOW_DIR=${PWD}/../..

CHCKPOINT=1


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

#python3 ../../flow/visualize/new_rllib_visualizer.py \
#	$HUMAN_DIR\
#	$CHCKPOINT \
#	--seed_dir $FLOW_DIR \
#	> ../../exp_results/human_mor/temp.txt 

LOC1=500
DIST_BETWEEN=500
AFTER=100

AVP=10

for DIST_BETWEEN in 500 1000
do
	let LOC2=LOC1+DIST_BETWEEN
	let TOTAL=LOC2+AFTER

	python3 ../../flow/visualize/new_rllib_visualizer.py \
		$HUMAN_DIR \
		$CHCKPOINT \
		--seed_dir $FLOW_DIR \
		--render_mode no_render \
		--avp_to_probability ${AVP} \
		--highway_len ${TOTAL} \
		--on_ramps ${LOC1} ${LOC2} \
		> ../../exp_results/human_mor/mor_EVAL_2000_200_10_${LOC1}_${LOC2}.txt & 
done

wait 
source ~/notification_zyl.sh

#--render_mode no_render \
#--main_merge_human_inflows $MAIN_INFLOW $MERGE_INFLOW \


#for AVP in 2 4 6 8 10 30 50 70 80 100
#do
#	python3 flow/visualize/new_rllib_visualizer.py $HUMAN_DIR $CHCKPOINT --render_mode no_render --handset_avp ${AVP} >> ./exp_results/adaptive_headway/avp10/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt &
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








