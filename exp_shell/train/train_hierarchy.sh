
export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"

export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8

export TRAINED_POLICY="/home/flow/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/aamas_full"

for AVP in 10  
do
	python3 ../../examples/rllib/multiagent_exps/hierarchical_policy.py --avp ${AVP} --policy_dir ${TRAINED_POLICY}
done

#for AVP in 70 90 
#do
#	python3 ../examples/rllib/multiagent_exps/count_ahead_multiagent_merge4_Merge4_Collaborate_lrschedule.py --avp ${AVP}
#done

#MERGE_INFLOW=200
#for MAIN_INFLOW in 1400 2000 
#do
#	let MAIN_RL_INFLOW=MAIN_INFLOW/10
#	let MAIN_HUMAN_INFLOW=MAIN_INFLOW-MAIN_RL_INFLOW
#	echo $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW
#	python3 ../examples/rllib/multiagent_exps/count_ahead_multiagent_merge4_Merge4_Collaborate_lrschedule.py --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_INFLOW
#done

