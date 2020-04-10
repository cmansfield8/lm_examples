#!/bin/bash

dtype=$1
modelname=lstm-lm-$2
ftype=$3
base_dir=/mnt/d/sync-dir/lm_examples/exp1

# make table of scores:
python get_lstm_results.py --in_dir ${base_dir} \
 --out_dir ${base_dir}/fisher_${dtype} --ftype ${ftype} \
 --dtype $dtype --modelname $modelname

#python get_perplexity.py "${base_dir}/fisher_${dtype}/swbd_${ftype}_${modelname}_scores.tsv" "${base_dir}/fisher_${dtype}/swbd_${ftype}_${modelname}_scores_ppl.tsv"
