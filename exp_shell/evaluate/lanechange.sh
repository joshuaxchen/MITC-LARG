HUMAN_DIR=/home/users/flow_user/ray_results/human_multiagent_highway_merge4_MOR_Collaborate_lrschedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4CollaborateMOR-v0_0573c_00000_0_2021-07-26_11-10-40

TRAIN_DIR=/home/users/flow_user/ray_results/multiagent_yulin_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_6e090_00000_0_2021-08-05_18-04-04/

TRAIN_DIR1=/home/users/flow_user/ray_results/multiagent_yulin_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_352ab_00000_0_2021-08-06_22-47-37/

TRAIN_DIR2=${HOME}/ray_results/multiagent_yulin_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_7f52b_00000_0_2021-08-07_08-08-02/

PRESET_0=${HOME}/ray_results/multiagent_yulin0_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_59fb3_00000_0_2021-08-21_09-16-18/

PRESET_1=${HOME}/ray_results/multiagent_yulin1_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_5a9e2_00000_0_2021-08-21_09-16-19

PRESET_2=${HOME}/ray_results/multiagent_yulin2_lanechange_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_9abd7_00000_0_2021-08-21_09-18-06

FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results/lane_change


CHCKPOINT=500


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

#python3 ../../flow/visualize/new_rllib_visualizer.py \
#	$HUMAN_DIR\
#	$CHCKPOINT \
#	--seed_dir $FLOW_DIR \
#	> ../../exp_results/human_mor/temp.txt 

MAIN_INFLOW=2000
MERGE_INFLOW=200
AVP=10
J=0

WORKING_DIR=$EXP_FOLDER/preset_0
mkdir ${WORKING_DIR}

for MAIN_INFLOW in 2000 # 1800 #1900 2000 2100 2200 # 1800 1900 2000 2100 2200 #1800 1900 #
do
	for AVP in 10 #200 400 600 800 # 200 400 600 800 # 200 400 600 800
	do
		let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
		let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW

		for RL_RIGHT_LEFT in 0
		do
			if ((RL_RIGHT_LEFT == 0)); then
				RL_INFLOW_LEFT=0
				RL_INFLOW_RIGHT=${MAIN_RL_INFLOW}
				HUMAN_INFLOW_LEFT=${MAIN_INFLOW}
				HUMAN_INFLOW_RIGHT=${MAIN_HUMAN_INFLOW}
			else # otherwise, rl vehicles on the left
				RL_INFLOW_LEFT=${MAIN_RL_INFLOW}
				RL_INFLOW_RIGHT=0
				HUMAN_INFLOW_LEFT=${MAIN_HUMAN_INFLOW}
				HUMAN_INFLOW_RIGHT=${MAIN_INFLOW}
			fi
			echo ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} 
			echo ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}

			for RIGHT_HUMAN_LANE_CHANGE in 0
			do 
				for AGGRESSIVE in 0.2 0.4 0.6 0.8 1
				do
					python3 $VISUALIZER \
						$PRESET_0 \
						$CHCKPOINT \
						--seed_dir $FLOW_DIR \
						--lateral_resolution 3.2 \
						--render_mode no_render \
						--human_inflows ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}\
						--rl_inflows ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} \
						--human_lane_change ${RIGHT_HUMAN_LANE_CHANGE} 0 \
						--rl_lane_change 0 0 \
						--merge_inflow ${MERGE_INFLOW} \
						--aggressive ${AGGRESSIVE} 
						>> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${RL_RIGHT_LEFT}_${RIGHT_HUMAN_LANE_CHANGE}_${AGGRESSIVE}.txt &

					let J=J+1
					if ((J == 20)); then
						wait
						let J=0
						echo "another batch"
					fi
				done
			done
		done
	done
done

WORKING_DIR=$EXP_FOLDER/preset_1
mkdir ${WORKING_DIR}

for MAIN_INFLOW in 2000 # 1800 #1900 2000 2100 2200 # 1800 1900 2000 2100 2200 #1800 1900 #
do
	for AVP in 10 #200 400 600 800 # 200 400 600 800 # 200 400 600 800
	do
		let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
		let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW

		for RL_RIGHT_LEFT in 0
		do
			if ((RL_RIGHT_LEFT == 0)); then
				RL_INFLOW_LEFT=0
				RL_INFLOW_RIGHT=${MAIN_RL_INFLOW}
				HUMAN_INFLOW_LEFT=${MAIN_INFLOW}
				HUMAN_INFLOW_RIGHT=${MAIN_HUMAN_INFLOW}
			else # otherwise, rl vehicles on the left
				RL_INFLOW_LEFT=${MAIN_RL_INFLOW}
				RL_INFLOW_RIGHT=0
				HUMAN_INFLOW_LEFT=${MAIN_HUMAN_INFLOW}
				HUMAN_INFLOW_RIGHT=${MAIN_INFLOW}
			fi
			echo ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} 
			echo ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}

			for RIGHT_HUMAN_LANE_CHANGE in 1
			do 
				for AGGRESSIVE in 0.2 0.4 0.6 0.8 1
				do
					python3 $VISUALIZER \
						$PRESET_1 \
						$CHCKPOINT \
						--seed_dir $FLOW_DIR \
						--lateral_resolution 3.2 \
						--render_mode no_render \
						--human_inflows ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}\
						--rl_inflows ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} \
						--human_lane_change ${RIGHT_HUMAN_LANE_CHANGE} 0 \
						--rl_lane_change 0 0 \
						--merge_inflow ${MERGE_INFLOW} \
						--aggressive ${AGGRESSIVE} \
						>> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${RL_RIGHT_LEFT}_${RIGHT_HUMAN_LANE_CHANGE}_${AGGRESSIVE}.txt &

					let J=J+1
					if ((J == 20)); then
						wait
						let J=0
						echo "another batch"
					fi
				done
			done
		done
	done
done
#
WORKING_DIR=$EXP_FOLDER/preset_2
mkdir ${WORKING_DIR}

for MAIN_INFLOW in 2000 # 1800 #1900 2000 2100 2200 # 1800 1900 2000 2100 2200 #1800 1900 #
do
	for AVP in 10 #200 400 600 800 # 200 400 600 800 # 200 400 600 800
	do
		let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
		let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW

		for RL_RIGHT_LEFT in 1
		do
			if ((RL_RIGHT_LEFT == 0)); then
				RL_INFLOW_LEFT=0
				RL_INFLOW_RIGHT=${MAIN_RL_INFLOW}
				HUMAN_INFLOW_LEFT=${MAIN_INFLOW}
				HUMAN_INFLOW_RIGHT=${MAIN_HUMAN_INFLOW}
			else # otherwise, rl vehicles on the left
				RL_INFLOW_LEFT=${MAIN_RL_INFLOW}
				RL_INFLOW_RIGHT=0
				HUMAN_INFLOW_LEFT=${MAIN_HUMAN_INFLOW}
				HUMAN_INFLOW_RIGHT=${MAIN_INFLOW}
			fi
			echo ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} 
			echo ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}

			for RIGHT_HUMAN_LANE_CHANGE in 1
			do 
				for AGGRESSIVE in 0.2 0.4 0.6 0.8 1
				do
					python3 $VISUALIZER \
						$PRESET_2 \
						$CHCKPOINT \
						--seed_dir $FLOW_DIR \
						--lateral_resolution 3.2 \
						--render_mode no_render \
						--human_inflows ${HUMAN_INFLOW_RIGHT} ${HUMAN_INFLOW_LEFT}\
						--rl_inflows ${RL_INFLOW_RIGHT} ${RL_INFLOW_LEFT} \
						--human_lane_change ${RIGHT_HUMAN_LANE_CHANGE} 0 \
						--rl_lane_change 0 0 \
						--merge_inflow ${MERGE_INFLOW} \
						--aggressive ${AGGRESSIVE} \
						>> ${WORKING_DIR}/EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}_${RL_RIGHT_LEFT}_${RIGHT_HUMAN_LANE_CHANGE}_${AGGRESSIVE}.txt &

					let J=J+1
					if ((J == 20)); then
						wait
						let J=0
						echo "another batch"
					fi
				done
			done
		done
	done
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








