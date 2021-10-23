#TRAIN_DIR_10=/home/users/flow_user/ray_results/yulin_adaptive_headway_eta1_0.9_eta2_0.1/adaptive_headway_avp10_main2000_merge200/
#TRAIN_DIR_30=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_30
#TRAIN_DIR_50=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_50
#TRAIN_DIR_70=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_70
#TRAIN_DIR_90=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/merge4_highway2000_merge200_avp_90

#TRAIN_DIR_100=/home/users/flow_user/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/PPO_MultiAgentHighwayPOEnvMerge4Collaborate-v0_ac09e_00000_0_2021-05-26_02-04-54 

HUMAN_DIR=/home/users/yulin/ray_results/yulin_merge_4_HUMAN_Sim/PPO_MergePOEnv-v0_baf56_00000_0_2021-05-26_02-05-19 


FLOW_DIR=${PWD}/../..

CHCKPOINT=1


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

MERGE_INFLOW=200
J=0
for MAIN_INFLOW in 1600 1650 #1610 1620 1630 1640 1650 1660 1670 1680 1690 1710 1720 1730 1740 1750 1760 1770 1780 1790
do
	for MERGE_INFLOW in 200 # 500 600 700 800 900 1000 1100 1200 1300 1400 1500 # 180 190 200 210 220 230 240 250 260 270 280 290 300 310 320 330 340 350 360 370 380 390 400 
	do
		#MAIN_HUMAN_INFLOW= xargs printf "%.*f\n" "$MAIN_HUMAN_INFLOW"
		echo $MAIN_INFLOW $MERGE_INFLOW
		python3 ../../flow/visualize/new_rllib_visualizer.py \
			$HUMAN_DIR \
			$CHCKPOINT \
			--render_mode sumo_gui \
			--seed_dir $FLOW_DIR \
			--history_file_name human_${MAIN_INFLOW}_${MERGE_INFLOW} \
			--main_merge_human_inflows $MAIN_INFLOW $MERGE_INFLOW \
			> ../../exp_results/human/${MAIN_INFLOW}_${MERGE_INFLOW}.txt &
		let J=J+1
		if ((J == 8)); then
			wait
			let J=0
			echo "another batch"
		fi
	done
done

wait
source ~/notification_zyl.sh

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








