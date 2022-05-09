#TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/hierarchy_based_on_aamas_full
#TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/aamas_full
declare -A TRAIN_DIR
declare -A MARK 

TRAIN_DIR[1]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp10_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_b6165_00000_0_2021-07-03_10-52-46
MARK[1]='1650_200_10'

TRAIN_DIR[2]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp10_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_803da_00000_0_2021-07-03_16-56-20 
MARK[2]='1850_200_10'

# AVP30
TRAIN_DIR[3]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp10_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_74d88_00000_0_2021-07-03_21-20-52
MARK[3]='2000_200_10'
###############

TRAIN_DIR[4]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_a9c72_00000_0_2021-07-04_01-25-44
MARK[4]='1650_200_30'


TRAIN_DIR[5]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_0a35b_00000_0_2021-07-04_07-54-59
MARK[5]='1850_200_30'


TRAIN_DIR[6]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_740c0_00000_0_2021-07-04_14-31-39
MARK[6]='2000_200_30'


TRAIN_DIR[7]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp50_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_6328a_00000_0_2021-07-04_21-04-53
MARK[7]='1650_200_50'

TRAIN_DIR[8]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp50_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_6fb5c_00000_0_2021-07-05_05-40-37
MARK[8]='1850_200_50'


TRAIN_DIR[9]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp50_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_3688f_00000_0_2021-07-05_14-07-16
MARK[9]='2000_200_50'

##############
TRAIN_DIR[10]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp80_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_5a6ae_00000_0_2021-07-04_01-52-09
MARK[10]='1650_200_80'


TRAIN_DIR[11]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp80_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_2ad89_00000_0_2021-07-04_11-52-07
MARK[11]='1850_200_80'

########new############
TRAIN_DIR[12]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp80_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_cb311_00000_0_2021-07-07_12-50-18
MARK[12]='2000_200_80'
# already have

TRAIN_DIR[13]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp100_Main1650_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_e4471_00000_0_2021-07-07_15-07-01
MARK[13]='1650_200_100'
# already have

TRAIN_DIR[14]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp100_Main1850_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_54bf7_00000_0_2021-07-07_16-28-54
MARK[14]='1850_200_100'
# dr-wily

TRAIN_DIR[15]=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp100_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_56c3a_00000_0_2021-07-07_23-38-27
MARK[15]='2000_200_100'
# dr-light 

# the model trained under IDM human driver
TRAIN_DIR[16]=${HOME}/ray_results/Random_placement_IDMAAMAS_Avp30_Main2000_Merge200_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_af511_00000_0_2022-04-14_14-04-18

# the model trained under IDM human driver, AV with no change in reward

TRAIN_DIR[17]=${HOME}/april14_models/Random_placement_IDMAAMASreward_Avp30_Main2000_Merge200_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.09999999999999998/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_cdbdb_00000_0_2022-04-15_21-13-27

TRAIN_DIR[18]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_c0308_00000_0_2022-04-20_21-07-09

TRAIN_DIR[19]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality0.1_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_c0308_00000_0_2022-04-20_21-07-09/

TRAIN_DIR[20]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality0.2_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_e8fe6_00000_0_2022-04-21_00-00-05/

TRAIN_DIR[21]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality0.4_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_85dbf_00000_0_2022-04-21_00-04-29/

TRAIN_DIR[22]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality0.8_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_22449_00000_0_2022-04-21_00-08-51/

TRAIN_DIR[23]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality2.0_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_3a589_00000_0_2022-04-21_14-07-02/

TRAIN_DIR[24]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality4.0_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_b4a4e_00000_0_2022-04-21_14-10-28/

TRAIN_DIR[25]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality1.6_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_bc713_00000_0_2022-04-21_18-06-54/

TRAIN_DIR[26]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality1.2_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_291e7_00000_0_2022-04-21_18-09-56/

TRAIN_DIR[27]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality1.0_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_0b6a0_00000_0_2022-04-21_21-51-01/


TRAIN_DIR[28]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality0.9_2000_200_30_accel_eta1_0.90_eta2_0.10/PPO_SingleLaneController-v0_46644_00000_0_2022-04-21_21-52-40/

TRAIN_DIR[29]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality0.9_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.30/PPO_SingleLaneController-v0_911a8_00000_0_2022-04-21_23-34-58/

TRAIN_DIR[30]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality0.9_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.60/PPO_SingleLaneController-v0_a29f1_00000_0_2022-04-22_18-47-57/

TRAIN_DIR[31]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_penality0.9_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.90/PPO_SingleLaneController-v0_a83d4_00000_0_2022-04-22_18-48-06/

TRAIN_DIR[32]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.05/PPO_SingleLaneController-v0_8b7ff_00000_0_2022-04-23_00-02-16/

TRAIN_DIR[33]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.10/PPO_SingleLaneController-v0_8c008_00000_0_2022-04-22_23-33-39/

TRAIN_DIR[34]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.20/PPO_SingleLaneController-v0_924e7_00000_0_2022-04-22_23-33-49/

TRAIN_DIR[35]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.30/PPO_SingleLaneController-v0_6577c_00000_0_2022-04-23_00-01-12/

TRAIN_DIR[36]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.40/PPO_SingleLaneController-v0_435a9_00000_0_2022-04-24_00-27-41/

TRAIN_DIR[37]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.50/PPO_SingleLaneController-v0_35e55_00000_0_2022-04-24_00-27-19/

TRAIN_DIR[38]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.60/PPO_SingleLaneController-v0_67d10_00000_0_2022-04-24_00-43-02/

TRAIN_DIR[39]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.00_eta2_1.00_eta3_0.20/PPO_SingleLaneController-v0_cc97d_00000_0_2022-04-24_21-45-42/

TRAIN_DIR[40]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.00_eta2_1.00_eta3_0.30/PPO_SingleLaneController-v0_c84b8_00000_0_2022-04-24_21-45-35/
 
TRAIN_DIR[41]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.00_eta2_1.00_eta3_0.40/PPO_SingleLaneController-v0_faf10_00000_0_2022-04-25_03-23-26/
 
TRAIN_DIR[42]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.00_eta2_1.00_eta3_0.50/PPO_SingleLaneController-v0_d02e8_00000_0_2022-04-25_00-01-49/

TRAIN_DIR[43]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.00_eta2_1.00_eta3_0.60/PPO_SingleLaneController-v0_3cb10_00000_0_2022-04-25_07-42-58/

TRAIN_DIR[44]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.00_eta2_1.00_eta3_0.70/PPO_SingleLaneController-v0_29d0c_00000_0_2022-04-25_00-18-38/

TRAIN_DIR[45]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.00_eta2_1.00_eta3_0.80/PPO_SingleLaneController-v0_7f409_00000_0_2022-04-25_03-55-46/

# so far, the best: speed max 30 with penality for the delay
TRAIN_DIR[45]=${HOME}/april20_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_3c5e6_00000_0_2022-04-25_15-35-25/

# fix the speed issue
TRAIN_DIR[46]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.10/PPO_SingleLaneController-v0_78df3_00000_0_2022-04-25_12-02-21/

TRAIN_DIR[47]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.30/PPO_SingleLaneController-v0_bf8db_00000_0_2022-04-25_11-42-51/

# normalize the speed as reward
TRAIN_DIR[48]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.30/PPO_SingleLaneController-v0_bf8db_00000_0_2022-04-25_11-42-51/

TRAIN_DIR[49]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.10/PPO_SingleLaneController-v0_44d24_00000_0_2022-04-25_15-35-39/

TRAIN_DIR[50]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.20/PPO_SingleLaneController-v0_af8ad_00000_0_2022-04-25_16-43-03/

TRAIN_DIR[51]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_03c69_00000_0_2022-04-25_15-33-50/

TRAIN_DIR[53]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.30/PPO_SingleLaneController-v0_3e27e_00000_0_2022-04-25_18-27-16/

# so far the best
TRAIN_DIR[52]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.70_eta2_0.30_eta3_0.20/PPO_SingleLaneController-v0_00543_00000_0_2022-04-25_18-25-32/

TRAIN_DIR[54]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.50_eta2_0.50_eta3_0.20/PPO_SingleLaneController-v0_308e1_00000_0_2022-04-25_22-30-16/

TRAIN_DIR[55]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.60_eta2_0.40_eta3_0.20/PPO_SingleLaneController-v0_f508b_00000_0_2022-04-25_22-14-17/

# 
TRAIN_DIR[56]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.70_eta2_0.30_eta3_0.20/PPO_SingleLaneController-v0_00543_00000_0_2022-04-25_18-25-32/


# so far the best 1551
TRAIN_DIR[57]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.60_eta2_0.40_eta3_0.20/PPO_SingleLaneController-v0_f508b_00000_0_2022-04-25_22-14-17/


TRAIN_DIR[58]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.80_eta2_0.20_eta3_0.10/PPO_SingleLaneController-v0_45294_00000_0_2022-04-26_02-41-23/

TRAIN_DIR[59]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.80_eta2_0.20_eta3_0.20/PPO_SingleLaneController-v0_39ef4_00000_0_2022-04-26_00-03-35/

TRAIN_DIR[60]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_normalization_2000_200_30_accel_eta1_0.80_eta2_0.20_eta3_0.30/PPO_SingleLaneController-v0_a3135_00000_0_2022-04-26_00-20-50/

TRAIN_DIR[61]=${HOME}/april25_models/multiagent_single_lane_single_lane_controller_horizon_2000_speed_max30_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_c88d3_00000_0_2022-04-25_22-13-02/

# go back to original reward
TRAIN_DIR[62]=${HOME}/april26_models/multiagent_single_lane_single_lane_controller_horizon_2000_original_krauss_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_6a66d_00000_0_2022-04-26_12-22-14/

TRAIN_DIR[63]=${HOME}/april26_models/multiagent_single_lane_single_lane_controller_horizon_2000_Original_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_SingleLaneController-v0_7cfb8_00000_0_2022-04-26_11-54-08/

TRAIN_DIR[64]=${HOME}/april26_models/multiagent_single_lane_single_lane_controller_horizon_2000_avg_3_speeds_2000_200_30_accel_eta1_0.90_eta2_0.10_eta3_0.00/PPO_BehindCurrentAheadSingleLaneController-v0_91b4f_00000_0_2022-04-26_13-27-46/
#echo "curious: ${TRAIN_DIR[1]}"


CHCKPOINT=150

FLOW_DIR=${PWD}/../..
# VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
VISUALIZER=$FLOW_DIR/flow/visualize/parallized_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results
WORKING_DIR=$EXP_FOLDER/april26_single_lane/

# 1. 1650_200_30 I=4
# 2. 1850_200_30 I=5
# 3. 2000_200_30 I=6

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:$FLOW_DIR"
#${PWD}/$FLOW_DIR/
echo "set python path: $PYTHONPATH"

echo "************************************************************"
#echo ${TRAIN_DIR[*]}
NUM=0

MERGE_INFLOW=200

mkdir ${WORKING_DIR}
J=0
for I in 62 63 64 #3 7 8 9 10 #11 12 13 14 15 1 #7 8 9 10 11 12 13 14 15
do
	echo "${TRAIN_DIR[$I]}"
	#mkdir ${WORKING_DIR}/${MARK[$I]}

	for MERGE_INFLOW in 200 #400 600 800 #180 190 200 210 220 230 240 250 260 270 280 290 300 310 320 330 340 350 360 370 380 390 400 500 600 700 800 900 1000 
	do
		for MAIN_INFLOW in 2000 #1700 1800 1900 2000 #1650 #2000 #1850 1650
		do
			for AVP in 10 #2 3 4 5 6 7 8 9 10 12 14 16 18 20 25 30 35 40
			do
				let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
				let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
				echo "evaluate" ${TRAIN_DIR[$I]} ${MARK[$I]} "on AVP ${AVP}"
				echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW

                if (($I==62)); then
                    FNAME="IJCAI_Krauss"
                elif (($I==63)); then
                    FNAME="IJCAI_IDM"
                elif (($I==64)); then
                    FNAME="IJCAI_avg_speed"
                fi
                echo "fname" ${FNAME}

				python3 $VISUALIZER \
					${TRAIN_DIR[$I]} \
					$CHCKPOINT \
					--render_mode no_render \
					--seed_dir $FLOW_DIR \
				    --cpu 10 \
					--measurement_rate 5000 \
					--horizon 2000 \
					--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
					>> ${WORKING_DIR}/${FNAME}_EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_even.txt &

                python3 $VISUALIZER \
					${TRAIN_DIR[$I]} \
					$CHCKPOINT \
					--render_mode no_render \
					--seed_dir $FLOW_DIR \
				    --cpu 10 \
                    --to_probability \
					--measurement_rate 5000 \
					--horizon 2000 \
					--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
					>> ${WORKING_DIR}/${FNAME}_EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_random.txt &

					#--to_probability \
                    #--print_vehicles_per_time_step_in_file april26_avg_3_speeds_krauss_idm_even \
				let J=J+1
				if ((J == 30)); then
					wait
					let J=0
					echo "another batch"
				fi
			done
		done
	done 
done

#--history_file_name random_${MARK[$I]}_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP} \
#>> ${WORKING_DIR}/${MARK[$I]}/merge4_EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}.txt &

				#python3 $VISUALIZER ${TRAIN_DIR[$I]} $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --to_probability --history_file_name random_${MARK[$I]}_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP} --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW 

				#python3 $VISUALIZER ${TRAIN_DIR[$I]} $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --to_probability --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW >> ${WORKING_DIR}/${MARK[$I]}/merge4_EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}.txt &
wait
source ~/notification_zyl.sh
#for I in 4 
#do
#	echo "${TRAIN_DIR[$I]}"
#	mkdir ${WORKING_DIR}/${MARK[$I]}
#	for MAIN_INFLOW in 1650 1850 
#	do
#		for AVP in 30 
#		do
#			let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
#			let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#			echo "evaluate" ${TRAIN_DIR[$I]} ${MARK[$I]} "on AVP ${AVP}"
#			echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW
#			python3 $VISUALIZER ${TRAIN_DIR[$I]} $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --avp_to_probability ${AVP} --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW >> ${WORKING_DIR}/${MARK[$I]}/merge4_EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}.txt &
#		done
#	done
#	
#done

#for I in  4 5
#do
#	echo "${TRAIN_DIR[$I]}"
#	mkdir ${WORKING_DIR}/${MARK[$I]}
#	for MAIN_INFLOW in 1600 1700 1800 1900 2000
#	do
#		for AVP in 1 2 3 4 5 6 7 8 9 10 12 14 16 18 20
#		do
#			let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
#			let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#			echo "evaluate" ${TRAIN_DIR[$I]} ${MARK[$I]} "on AVP ${AVP}"
#			echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW
#			python3 $VISUALIZER ${TRAIN_DIR[$I]} $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --avp_to_probability ${AVP} --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW >> ${WORKING_DIR}/${MARK[$I]}/merge4_EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}.txt &
#		done
#		wait
#	done
#	
#done



#mkdir $WORKING_DIR
#for I in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
#do
#	echo "${TRAIN_DIR[$I]}"
#	mkdir ${WORKING_DIR}/${MARK[$I]}
#	for MAIN_INFLOW in 1600 1650 1700 1750 1800 1850 1900 1950 2000
#	do
#		let MAIN_RL_INFLOW=MAIN_INFLOW*${AVPS[$I]}/100
#		let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#		echo "evaluate" ${TRAIN_DIR[$I]} ${MARK[$I]} "on AVP ${AVP}"
#		echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW
#		python3 $VISUALIZER ${TRAIN_DIR[$I]} $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --avp_to_probability ${AVPS[$I]} --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW >> ${WORKING_DIR}/${MARK[$I]}/merge4_EVAL_${MAIN_INFLOW}_$MERGE_INFLOW.txt &
#	done
#	if ((I == 4 || I==8 || I==12)); then
#		wait
#	fi
#done


