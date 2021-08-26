
export PYTHONPATH="${PYTHONPATH}:${PWD}/../"

export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8


for AVP in 10 30 50  
do
	python3 ../examples/rllib/multiagent_exps/count_ahead_multiagent_merge4_Merge4_Collaborate_lrschedule.py --avp ${AVP}
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

