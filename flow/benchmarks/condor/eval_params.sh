#!/bin/bash
source ~/.bashrc
conda activate flow_test_ray1.0.1
echo "$@"
#python condor/eval_params.py --params $2 -o $1 --benchmark_name $3 --controller_name $4
eval "python condor/eval_params.py ${@}"
