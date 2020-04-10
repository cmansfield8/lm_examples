#!/bin/bash

# conda activate lmenv
source /homes/coman8/anaconda3/bin/activate /homes/coman8/anaconda3/envs/lmenv
# GPU version
#source /homes/ttmt001/transitory/pytorch-exps/pytorch-0.4.0-gpu/bin/activate
# CPU version
# source /homes/ttmt001/transitory/pytorch-exps/pytorch-0.4.0-cpu/bin/activate

RUN_ID=5005
SEED=3000
DTYPE=cont
emsize=256
nhid=128
model_type=GRU

basedir=/homes/coman8/lm_examples/src/lstm_lm
cd $basedir
# Training
#python train_lm.py \
#    --model_type $model_type \
#    --epochs 50 --dtype $DTYPE \
#    --emsize $emsize --nhid $nhid \
#    --batch_size 128  --seed $SEED \
#    --save /homes/coman8/lm_examples/exp1/lstm-lm-${RUN_ID}.pt \
#    --cuda >> /homes/coman8/lm_examples/exp1/logs/job${RUN_ID}.log

for ftype in ms ptb
do
    python score_swbd.py \
        --model_type $model_type \
	--dtype $DTYPE \
        --emsize $emsize \
        --nhid $nhid \
        --seed $SEED \
        --save /homes/coman8/lm_examples/exp1/lstm-lm-${RUN_ID}30.pt \
        --ftype $ftype --cuda --eos >> /homes/coman8/lm_examples/exp1/logs/logsjob${RUN_ID}.log
done
