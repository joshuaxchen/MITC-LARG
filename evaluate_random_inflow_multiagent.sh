
export PYTHONPATH="${PYTHONPATH}:${PWD}/"

export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8


#python3 examples/rllib/multiagent_exps/linearPPO_multiagent_merge4_Merge4_Collaborate_lrschedule.py 


#nohup python3 ../examples/rllib/multiagent_exps/random_inflow_multiagent_merge4_Merge4_Collaborate_lrschedule.py --random_main_inflow 2000 1900 --random_merge_inflow 200 
#nohup python3 ../examples/rllib/multiagent_exps/random_inflow_multiagent_merge4_Merge4_Collaborate_lrschedule.py --random_main_inflow 2000 1900 1800 --random_merge_inflow 200 
#python3 ../examples/rllib/multiagent_exps/random_inflow_multiagent_merge4_Merge4_Collaborate_lrschedule.py --random_main_inflow 2000 1900 1800 1700 --random_merge_inflow 200 
#python3 ../examples/rllib/multiagent_exps/random_inflow_multiagent_merge4_Merge4_Collaborate_lrschedule.py --random_main_inflow 2000 1900 1800 1700 1600 --random_merge_inflow 200 

TRAIN_DIR=~/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/random_main2000-1900_merge200
CHCKPOINT=500

MERGE_INFLOW=200

for MAIN_INFLOW in 2000 1900 1800 1700 1600 1500 1400 
do
	#MAIN_HUMAN_INFLOW= xargs printf "%.*f\n" "$MAIN_HUMAN_INFLOW"
	let MAIN_RL_INFLOW=MAIN_INFLOW/10
	let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
	echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW
	python3 ./flow/visualize/new_rllib_visualizer.py \
		$TRAIN_DIR \
		$CHCKPOINT \
		--render_mode no_render \
		--handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW \
		> ./exp_results/random_inflow/main2000-1900_merge200/${MAIN_INFLOW}_$MERGE_INFLOW.txt
done

