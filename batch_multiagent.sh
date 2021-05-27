
export PYTHONPATH="${PYTHONPATH}:${PWD}"

for AVP in 30 50 70 90 100 
do
	python3 examples/rllib/multiagent_exps/multiagent_merge4_Merge4_Collaborate_lrschedule.py --avp ${AVP}
done

