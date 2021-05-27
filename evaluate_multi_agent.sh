TRAIN_DIR_10=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_ac09e_00000_0_2021-05-26_02-04-54 

CHCKPOINT=500


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}"

for AVP in 10 8 6 4 2
do
	python3 flow/visualize/new_rllib_visualizer.py $TRAIN_DIR_10 $CHCKPOINT --render_mode no_render --handset_avp ${AVP} >> ./avp_multi_agent/av10/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt
done





