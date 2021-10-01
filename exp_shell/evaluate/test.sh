#TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/hierarchy_based_on_aamas_full
#TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/aamas_full
declare -A TRAIN_DIR
declare -A MARK 

#echo "curious: ${TRAIN_DIR[1]}"
TRAIN_DIR[1]=${HOME}/ray_results/multiagent_New_Even_Avp10_Main2000_Merge200_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_231b0_00000_0_2021-09-29_22-26-01

MARK[1]='2000_200_10'


FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results
WORKING_DIR=$EXP_FOLDER/test_random/

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

CHCKPOINT=500

mkdir ${WORKING_DIR}
J=0
for I in 1 #5 6 #7 8 9 10 11 12 13 14 15
do
	echo "${TRAIN_DIR[$I]}"
	mkdir ${WORKING_DIR}/${MARK[$I]}

	for MERGE_INFLOW in 200 #190 200 210 220 230 240 250 260 270 280 290 300 310 320 330 340 350 360 370 380 390 400 500 600 700 800 900 1000 
	do
		for MAIN_INFLOW in 1600 1700 1800 1900 2000 #1650
		do
			for AVP in 10 #1 5 10 16 20 30 40
			do
				let MAIN_RL_INFLOW=MAIN_INFLOW*${AVP}/100
				let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
				echo "evaluate" ${TRAIN_DIR[$I]} ${MARK[$I]} "on AVP ${AVP}"
				echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW

				python3 $VISUALIZER ${TRAIN_DIR[$I]} $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --to_probability --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW >> ${WORKING_DIR}/${MARK[$I]}/merge4_random_EVAL_${MAIN_INFLOW}_${MERGE_INFLOW}_${AVP}.txt &
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


