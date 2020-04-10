import sys
import math
from ast import literal_eval
import numpy as np
import pandas as pd


def get_perplexity(probs, log_input=False):
	if not log_input:
		probs = [math.log2(x) for x in probs]
	entropy = -1/len(probs)*sum(probs)
	return 2**entropy

infile = sys.argv[1]
outfile = sys.argv[2]

df = pd.read_csv(infile, sep='\t')

df['scores'] = df['scores'].apply(literal_eval)
df['logs'] = df['scores'].apply(lambda x: [math.log2(item) for item in x])
df['perplexity'] = df['logs'].apply(lambda x: get_perplexity(x, True))

print('Avg. sent perplexity: {}'.format(df['perplexity'].sum()/df.shape[0]))

logs = df['logs'].to_list()
logs = [x for sublist in logs for x in sublist]

print(len(logs))
print(logs[0])
print(sum(logs))
print('Avg. PPL: {}\n'.format(str(get_perplexity(logs, True))))


df.to_csv(outfile, sep='\t')
