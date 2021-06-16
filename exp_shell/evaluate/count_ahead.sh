TRAIN_DIR_1=/home/users/flow_user/ray_results/yulin_countahead_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/zero_count_ahead_main2000_merge200_avp10

CHCKPOINT=500

FLOW_DIR=${PWD}/../..
VISUALIZER=$FLOW_DIR/flow/visualize/new_rllib_visualizer.py
EXP_FOLDER=$FLOW_DIR/exp_results

echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:$FLOW_DIR"
#${PWD}/$FLOW_DIR/
echo "set python path: $PYTHONPATH"

MERGE_INFLOW=200

for AVP in 2 4 6 8 10 20 30 #40 50 60 70 80 100
do
	python3 $VISUALIZER $TRAIN_DIR_1 $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/count_ahead/zero/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt &
done

wait 

for AVP in 40 50 60 70 80 100
do
	python3 $VISUALIZER $TRAIN_DIR_1 $CHCKPOINT --render_mode no_render --seed_dir $FLOW_DIR --handset_avp ${AVP} >> $EXP_FOLDER/count_ahead/zero/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt &
done



