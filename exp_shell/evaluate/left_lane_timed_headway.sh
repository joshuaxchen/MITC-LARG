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

RL_LEFT_TIMED_HEADWAY=${HOME}/ray_results/multiagent_yulin_2000_1400_lanechange_left_av_time_headway_eta1_0.9_eta2_0.1/PPO_LeftLaneHeadwayControlledMultiAgentEnv-v0_3e0ea_00000_0_2022-04-03_14-07-01

RL_LEFT_ACCEL_STATE_10=${HOME}/ray_results/multiagent_yulin_1800_1200_30_lanechange_left_av_accel_eta1_0.9_eta2_0.1/PPO_LeftLaneHeadwayControlledMerge4-v0_6f0b5_00000_0_2022-04-06_19-19-48

FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
# VISUALIZER=$FLOW_DIR/flow/visualize/parallized_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results/lc_14000_8000



echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

MAIN_INFLOW=2000
MERGE_INFLOW=200
AVP=10
J=0

mkdir ${EXP_FOLDER}
RIGHT_MAIN_INFLOW=2000

WORKING_DIR=$EXP_FOLDER
mkdir ${WORKING_DIR}

CHCKPOINT=500
human_or_av=1
render='sumo_gui'
horizon=14000

for horizon in 2000 #14000 #2000 3000 4000 5000 6000 7000 8000 9000 10000 12000 14000
do
for RIGHT_MAIN_INFLOW in 1800 #1400 1600 1800 1900 2000 #2100 2200 # 1800 1900 2000 2100 2200 #1800 1900 #
do
	for LEFT_MAIN_INFLOW in 1200 #1000 1200 1400 1600 #1200 1400 1600 # 1800 #1900 2000 2100 2200 # 1800 1900 2000 2100 2200 #1800 1900 #
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
			    for ASSERTIVE in 100 #0.5 #5 #0.4 0.6 0.8 1
			    do
				for LC_PROB in -1
				do
				    # run AV policy
                    #human_or_av=1
                    if [[(human_or_av -eq 1)]]; then
                        echo "run AV"
                        python3 $VISUALIZER \
                            $RL_LEFT_ACCEL_STATE_10 \
                            $CHCKPOINT \
                            --agent_action_policy_dir $RL_LEFT_ACCEL_STATE_10 \
                            --seed_dir $FLOW_DIR \
                            --lateral_resolution 3.2 \
                            --render_mode ${render} \
                            --human_inflows ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT} \
                            --rl_inflows ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} \
                            --human_lane_change 1 1 \
                            --cpu 10 \
                            --rl_lane_change 0 0 \
                            --merge_inflow ${MERGE_INFLOW} \
                            --speed_gain ${SPEED_GAIN} \
                            --measurement_rate 8000 \
                            --to_probability \
                            --horizon ${horizon} \
                            --assertive ${ASSERTIVE} \
                            --lc_probability ${LC_PROB} 
                        # >> ${WORKING_DIR}/EVAL_${RIGHT_MAIN_INFLOW}_${LEFT_MAIN_INFLOW}_${MERGE_INFLOW}_${AVP_RIGHT}_${AVP_LEFT}_${SPEED_GAIN}_${ASSERTIVE}.txt &
                            #--print_vehicles_per_time_step_in_file ${PWD}/figure/vehicles_${RIGHT_MAIN_INFLOW}_${LEFT_MAIN_INFLOW}_${MERGE_INFLOW}_${AVP_RIGHT}_${AVP_LEFT}_${SPEED_GAIN}_${ASSERTIVE} \
                            #--print_metric_per_time_step_in_file  ${PWD}/figure/AV_${RIGHT_MAIN_INFLOW}_${LEFT_MAIN_INFLOW}_${MERGE_INFLOW}_${AVP_RIGHT}_${AVP_LEFT}_${SPEED_GAIN}_${ASSERTIVE} \
                            #--print_inflow_outflow_var_in_file ${PWD}/log/${horizon} \
                    fi

                    #human_or_av=0
                    if [[(human_or_av -eq 0)]]; then
                        echo "run human"
                        # run human baseline
                        # add no lane changing vehicles at the right lane	
                        let RL_INFLOW_RIGHT=0
                        let RL_INFLOW_LEFT=0
                        let NO_LANCHANGE_HUMAN_INFLOWS_ON_RIGHT=0
                        let HUMAN_INFLOW_RIGHT=RIGHT_MAIN_INFLOW
                        if [[(${AVP_RIGHT} != 0)]]; then # set the amount of vehicles to be non-lane-changing human drivers
                            let NO_LANCHANGE_HUMAN_INFLOWS_ON_RIGHT=RIGHT_MAIN_INFLOW*${AVP_RIGHT}/100		
                            let HUMAN_INFLOW_RIGHT=RIGHT_MAIN_INFLOW-NO_LANCHANGE_HUMAN_INFLOWS_ON_RIGHT
                            echo "avp right is not 0"
                        fi

                        # add no lane changing vehicles at the left lane	
                        let NO_LANCHANGE_HUMAN_INFLOWS_ON_LEFT=0
                        let HUMAN_INFLOW_LEFT=LEFT_MAIN_INFLOW
                        if [[(${AVP_LEFT} != 0)]]; then
                            let NO_LANCHANGE_HUMAN_INFLOWS_ON_LEFT=LEFT_MAIN_INFLOW*${AVP_LEFT}/100		
                            let HUMAN_INFLOW_LEFT=LEFT_MAIN_INFLOW-NO_LANCHANGE_HUMAN_INFLOWS_ON_LEFT
                            echo "avp left is not 0"
                        fi

                        # run human baseline 
                        python3 $VISUALIZER \
                            $RL_LEFT_ACCEL_STATE_10 \
                            $CHCKPOINT \
                            --agent_action_policy_dir $RL_LEFT_ACCEL_STATE_10 \
                            --seed_dir $FLOW_DIR \
                            --lateral_resolution 3.2 \
                            --cpu 10 \
                            --render_mode ${render} \
                            --human_inflows ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT} \
                            --rl_inflows ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} \
                            --human_lane_change 1 1 \
                            --rl_lane_change 0 0 \
                            --merge_inflow ${MERGE_INFLOW} \
                            --speed_gain ${SPEED_GAIN} \
                            --measurement_rate 8000 \
                            --no_lanchange_human_inflows_on_right ${NO_LANCHANGE_HUMAN_INFLOWS_ON_RIGHT} \
                            --no_lanchange_human_inflows_on_left ${NO_LANCHANGE_HUMAN_INFLOWS_ON_LEFT} \
                            --to_probability \
                            --assertive ${ASSERTIVE} \
                            --lc_probability ${LC_PROB} \
                            --horizon ${horizon} 
                            # >> ${WORKING_DIR}/EVAL_human_${RIGHT_MAIN_INFLOW}_${LEFT_MAIN_INFLOW}_${MERGE_INFLOW}_${AVP_RIGHT}_${AVP_LEFT}_${SPEED_GAIN}_${ASSERTIVE}.txt &
                            #--run_random_seed 0 \
                            #--print_vehicles_per_time_step_in_file ${PWD}/figure/human_vehicles_${RIGHT_MAIN_INFLOW}_${LEFT_MAIN_INFLOW}_${MERGE_INFLOW}_${AVP_RIGHT}_${AVP_LEFT}_${SPEED_GAIN}_${ASSERTIVE} \
                            #--print_metric_per_time_step_in_file  ${PWD}/figure/human_${RIGHT_MAIN_INFLOW}_${LEFT_MAIN_INFLOW}_${MERGE_INFLOW}_${AVP_RIGHT}_${AVP_LEFT}_${SPEED_GAIN}_${ASSERTIVE} \
                            #--print_inflow_outflow_var_in_file ${PWD}/log/${horizon} 
                            #--print_metric_per_time_step_in_file  ${PWD}/figure/human_${RIGHT_MAIN_INFLOW}_${LEFT_MAIN_INFLOW}_${MERGE_INFLOW}_${AVP_RIGHT}_${AVP_LEFT}_${SPEED_GAIN}_${ASSERTIVE} \
                        fi
			let J=J+1
		    if ((J == 4)); then
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
done


wait 
source ~/notification_zyl.sh

