TRAIN_DIR_10=~/ray_results/yulin_multiagent_highway_merge4_Full_Collaborate_lr_schedule_eta1_0.9_eta2_0.1/discrete_random_main_inflow_merge_200

CHCKPOINT=500


echo "*************add python path to current direction***********"
export PYTHONPATH="${PYTHONPATH}:${PWD}"

for MAIN_RL_INFLOW in 175
do
    for MERGE_HUMAN_INFLOW in 200
    do 
        python3 flow/visualize/new_rllib_visualizer.py \
            $TRAIN_DIR_10 \
            $CHCKPOINT \
            --render_mode no_render \
            --handset_inflow $MAIN_HUMAN_INFLOW $MAIN_RL_INFLOW $MERGE_HUMAN_INFLOW \
            > merge4_arrive_fixed_rollout40_${MAIN_HUMAN_INFLOW}_${MAIN_RL_INFLOW}_$MERGE_HUMAN_INFLOW.txt
    done
done


#for AVP in 10 8 6 4 2
#do
#	python3 flow/visualize/new_rllib_visualizer.py $TRAIN_DIR_10 $CHCKPOINT --render_mode no_render --handset_avp ${AVP} >> ./avp_multi_agent/av10/merge4_2000_200_TAVP_10_EAVP_${AVP}.txt
#done




 
