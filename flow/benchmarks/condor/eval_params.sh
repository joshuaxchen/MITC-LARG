#!/bin/bash
source ~/.bashrc
conda activate flow_2019_11
echo $1
echo $2
echo $3
echo $4
python eval_params.py --params $2 -o $1 --benchmark_name $3 --controller_name $4
