HUMAN_DIR=/home/users/flow_user/ray_results/human_multiagent_highway_merge4_MOR_Collaborate_lrschedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateMOR-v0_0573c_00000_0_2021-07-26_11-10-40

TRAIN_DIR=/home/users/flow_user/ray_results/multiagent_yulin_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_6e090_00000_0_2021-08-05_18-04-04/

TRAIN_DIR1=/home/users/flow_user/ray_results/multiagent_yulin_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_352ab_00000_0_2021-08-06_22-47-37/

TRAIN_DIR2=${HOME}/ray_results/multiagent_yulin_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_7f52b_00000_0_2021-08-07_08-08-02/

PRESET_0=${HOME}/ray_results/multiagent_yulin0_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_59fb3_00000_0_2021-08-21_09-16-18/

PRESET_1=${HOME}/ray_results/multiagent_yulin1_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_5a9e2_00000_0_2021-08-21_09-16-19

PRESET_2=${HOME}/ray_results/multiagent_yulin2_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_9abd7_00000_0_2021-08-21_09-18-06

RL_LEFT_MODEL=${HOME}/ray_results/multiagent_yulin_rl_left_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_66b6b_00000_0_2021-08-27_23-35-41

RL_RIGHT_MODEL=${HOME}/ray_results/multiagent_yulin_rl_right_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_5e6dd_00000_0_2021-08-27_23-28-18

RL_MODEL=${HOME}/ray_results/yulin_random_placement_multiagent_Even_Avp30_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_740c0_00000_0_2021-07-04_14-31-39

RL_LEFT_OVAL=${HOME}/ray_results/multiagent_yulin_lanechange_left_oval_eta1_0.9_eta2_0.1/PPO_LeftLaneOvalHighwayPOEnvMerge4Collaborate-v0_d7ca7_00000_0_2021-11-12_21-00-22

RL_LEFT_OVAL_MERGER=${HOME}/ray_results/multiagent_yulin_lanechange_left_oval_with_merger_eta1_0.9_eta2_0.1/PPO_LeftLaneOvalAboutToMergeHighwayPOEnvMerge4Collaborate-v0_b9c5c_00000_0_2021-11-12_22-11-07

RL_LEFT_BASIC=${HOME}/ray_results/multiagent_yulin_lanechange_left_basic_five_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvCollaborate-v0_98fef_00000_0_2021-11-14_20-49-05/


FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results/lane_change_4


CHCKPOINT=500


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

MAIN_INFLOW=2000
MERGE_INFLOW=200
AVP=10
J=0

mkdir ${EXP_FOLDER}
RIGHT_MAIN_INFLOW=2000

WORKING_DIR=$EXP_FOLDER/preset_1
mkdir ${WORKING_DIR}


for RIGHT_MAIN_INFLOW in 2000  # 1800 #1900 2000 2100 2200 # 1800 1900 2000 2100 2200 #1800 1900 #
do
	for LEFT_MAIN_INFLOW in 1600  # 1800 #1900 2000 2100 2200 # 1800 1900 2000 2100 2200 #1800 1900 #
	do
		for AVP_LEFT in 10 #20 30 40 #10 20 30 40 #200 400 600 800 # 200 400 600 800 # 200 400 600 800
		do
		    let RL_INFLOW_LEFT=LEFT_MAIN_INFLOW*${AVP_LEFT}/100
		    let HUMAN_INFLOW_LEFT=LEFT_MAIN_INFLOW-RL_INFLOW_LEFT

		    for AVP_RIGHT in 0 #20 30 40 #10 20 30 40 #200 400 600 800 # 200 400 600 800 # 200 400 600 800
		    do
			let RL_INFLOW_RIGHT=RIGHT_MAIN_INFLOW*${AVP_RIGHT}/100
			let HUMAN_INFLOW_RIGHT=RIGHT_MAIN_INFLOW-RL_INFLOW_RIGHT
			echo ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} 
			echo ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}

			for SPEED_GAIN in 1 #0.2 0.4 0.6 0.8 1
			do
			    for ASSERTIVE in 1 #0.5 #5 #0.4 0.6 0.8 1
			    do
				for LC_PROB in -1
				do
				    python3 $VISUALIZER \
					$RL_LEFT_MODEL \
					$CHCKPOINT \
					--agent_action_policy_dir $RL_MODEL \
					--seed_dir $FLOW_DIR \
					--lateral_resolution 3.2 \
					--render_mode sumo_gui \
					--human_inflows ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}\
					--rl_inflows ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} \
					--human_lane_change 1 1 \
					--rl_lane_change 0 0 \
					--to_probability \
					--merge_inflow ${MERGE_INFLOW} \
					--speed_gain ${SPEED_GAIN} \
					--assertive ${ASSERTIVE} \
					--lc_probability ${LC_PROB} 

				    let J=J+1
				    if ((J == 12)); then
					wait
					let J=0
					echo "another batch"
				    fi
				done
			    done
			done
			done
		done
	done
done


#wait 
#source ~/notification_zyl.sh

