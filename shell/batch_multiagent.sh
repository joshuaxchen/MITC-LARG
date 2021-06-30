
export PYTHONPATH="${PYTHONPATH}:${PWD}"

export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8


python3 examples/rllib/multiagent_exps/linearPPO_multiagent_merge4_Merge4_Collaborate_lrschedule.py 

#for AVP in 70 90 100 
#do
#	python3 examples/rllib/multiagent_exps/multiagent_merge4_Merge4_Collaborate_lrschedule.py --avp ${AVP} --num_rl 100
#done

