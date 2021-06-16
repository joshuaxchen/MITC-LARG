TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/continuous_adaptive_headway_avp10_main2000_merge200_maxheadway20
TRAIN_DIR_2=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/adaptive_discrete_action_avp10_main2000_merge200_maxheadway20
TRAIN_DIR_3=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/adaptive_headway_count_ahead_fixed_action_avp10_main2000_merge200_maxheadway20
TRAIN_DIR_4=~/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4AdaptiveHeadway-v0_6dae2_00000_0_2021-06-15_16-34-13
#TRAIN_DIR_30=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_30
#TRAIN_DIR_50=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_50
#TRAIN_DIR_70=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_70
#TRAIN_DIR_90=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_90

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

for AVP in 2 4 6 8 10 20 30 #40 50 60 70 80 100
do
	python3 $VISUALIZER $TRAIN_DIR_4 $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/adaptive_headway/continuous_penality/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt &
done

wait 

for AVP in 40 50 60 70 80 100
do
	python3 $VISUALIZER $TRAIN_DIR_4 $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/adaptive_headway/continuous_penality/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt &
done




