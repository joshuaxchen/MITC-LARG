TRAIN_DIR_10=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/RL100_merge4_highway2000_merge200_avp_10
TRAIN_DIR_30=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_30
TRAIN_DIR_50=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_50
TRAIN_DIR_70=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_70
TRAIN_DIR_90=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_90

#TRAIN_DIR_100=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_ac09e_00000_0_2021-05-26_02-04-54 
TRAIN_DIR_Human=/home/users/flow_user/ray_results/yulin_merge_4_HUMAN_Sim/PPO_MergePOEnv-v0_baf56_00000_0_2021-05-26_02-05-19

TRAIN_DIR_linearPPO=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/linearPPO

CHCKPOINT=500


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}"

for AVP in 10 20 30 40 50 #60 70 80 100
do
	python3 flow/visualize/new_rllib_visualizer.py $TRAIN_DIR_linearPPO $CHCKPOINT --render_mode no_render --handset_avp ${AVP} >> ./avp_multi_agent/linearPPO/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt
done



#for AVP in 2 4 6 8 10 30 50 70 80 100
#do
#	python3 flow/visualize/new_rllib_visualizer.py $TRAIN_DIR_10 $CHCKPOINT --render_mode no_render --handset_avp ${AVP} >> ./RL100_avp_multi_agent/av10/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt
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








