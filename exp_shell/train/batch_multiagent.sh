

export PYTHONPATH="${PYTHONPATH}:${PWD}/../../"
export RAY_MEMORY_MONITOR_ERROR_THRESHOLD=0.8



for AVP in 90 70 50 30 
do
    python3 ../../examples/rllib/multiagent_exps/multiagent_merge4_Merge4_Collaborate_lrschedule.py --avp ${AVP}
done

