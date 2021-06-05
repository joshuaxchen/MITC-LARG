
export PYTHONPATH="${PYTHONPATH}:${PWD}/../"

export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8


#python3 examples/rllib/multiagent_exps/linearPPO_multiagent_merge4_Merge4_Collaborate_lrschedule.py 


#python3 ../examples/rllib/multiagent_exps/random_inflow_multiagent_merge4_Merge4_Collaborate_lrschedule.py --random_main_inflow 2000 1900 --random_merge_inflow 200 
#python3 ../examples/rllib/multiagent_exps/random_inflow_multiagent_merge4_Merge4_Collaborate_lrschedule.py --random_main_inflow 2000 1900 1800 --random_merge_inflow 200 
#nohup python ../examples/rllib/multiagent_exps/random_inflow_multiagent_merge4_Merge4_Collaborate_lrschedule.py --random_main_inflow 2000 1900 1800 1700 --random_merge_inflow 200 
#nohup python ../examples/rllib/multiagent_exps/random_inflow_multiagent_merge4_Merge4_Collaborate_lrschedule.py --random_main_inflow 2000 1900 1800 1700 1600 --random_merge_inflow 200 
nohup python ../examples/rllib/multiagent_exps/random_inflow_multiagent_merge4_Merge4_Collaborate_lrschedule.py --random_main_inflow 2000 1900 1800 1700 1600 1500 --random_merge_inflow 200 

#for AVP in 2000 
#do
#	python3 examples/rllib/multiagent_exps/multiagent_merge4_Merge4_Collaborate_lrschedule.py --avp ${AVP} --num_rl 100
#done

