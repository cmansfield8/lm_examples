#!/usr/bin/env python

import os
import sys
from collections import Counter
import argparse
import pandas as pd
import cPickle as pickle

def get_lm_scores(in_file, out_file, df_idx, ftype, eos=True):
    a = pickle.load(open(in_file))
    list_row = []
    assert len(a) == len(df_idx)
    for i, scores in enumerate(a):
        row = df_idx.iloc[i]
        # col_name = 'ms_sent' if ftype == 'ms' else 'tree_sent'
        # num_tokens = len(row[col_name].split())
        # if eos:
        #    num_tokens += 1
        # else:
        #    scores = scores[:-1]
        # assert num_tokens == len(scores)
        list_row.append({'file': row.file, \
                'speaker': row.speaker, \
                'turn': row.turn, \
                'sent_num': row.sent_num, \
                'scores': scores})
    df = pd.DataFrame(list_row)
    cols = ['file', 'speaker', 'turn', 'sent_num', 'scores']
    df.to_csv(out_file, sep='\t', index=False, columns=cols, header=True)

if __name__ == '__main__':
    pa = argparse.ArgumentParser(description='Get scores from lstm model')
    pa.add_argument('--common_dir', \
            default='../../exp1', \
            help='project directory')
    pa.add_argument('--in_dir', \
            default='../../exp1', \
            help='project directory')
    pa.add_argument('--out_dir', \
            default='../../exp1', \
            help='output directory')
    pa.add_argument('--dtype', \
            default='dtok', type=str, \
            help='clean,disf,dtok')
    pa.add_argument('--ftype', \
            default='ms', type=str, \
            help='ms or ptb sentences')
    pa.add_argument('--modelname', \
            default='lstm-lm-2220', type=str, \
            help='lstm model name')

    args = pa.parse_args()
    # swbd_ptb_sents_ppl.txt
    basename = 'swbd_{}_scores_{}.pickle'.format(args.ftype, args.modelname)
    in_file = os.path.join(args.in_dir, 'fisher_' + args.dtype, basename)
    print "reading scores from file", in_file
    outname = "swbd_{}_{}_scores.tsv".format(args.ftype, args.modelname)
    out_file = os.path.join(args.out_dir, outname)

    # file with sentence indices
    idx_file = os.path.join(args.common_dir, 'swb_full.tsv')
    print "idx common file:", idx_file
    df_idx = pd.read_csv(idx_file, sep='\t')

    get_lm_scores(in_file, out_file, df_idx, args.ftype)

