# lm_examples
Language model examples -- tutorial code for new grad students at TIAL lab.  Update by Courtney Mansfield for building LMs according to her dissertation project.

# Dependencies
* SRI LM: /g/tial/sw/pkgs/srilm-1.7.1/bin/i686-m64/
* pytorch 0.4.0, cuda (or just use the CPU version)
* Python 2.7.x

# Fisher data set
* Original: /g/ssli/projects/disfluencies/fisher
* Various versions split to train and validation: `/g/ssli/projects/disfluencies/ttmt001/fisher_{clean,disf,dtok}`
    * disf: original version with disfluencies
    * clean: version cleaned of disfluencies
    * dtok: version with disfluencies, but not tokenized (e.g. "don't" is not split as "do" + "n't")
    * fsh_1* is in valid, the rest in train
* Stats: 
    * train: from 15522 files -- wc >> 1,181,752 sents; 14,363,366 tokens
    * valid: from 3137 files -- wc >> 268,991 sents; 2,841,422 tokens
For swbd errors surprisal study: use the dtok version.

# Steps
Some of these are already done (this is for documentation purposes only)

**1. Split to train/valid** (should be done already -- skip):

Raw data: 
```
mv fisher/text/fsh_1* fisher_disf/valid/
mv fisher/text/* fisher_disf/train/
```

**2. Preprocessings** (also should be done already -- skip EXCEPT 2d):
    
   2a0. (if files have associcated features -- dtok set):
    `./src/grep_words.sh {train,valid}`

   2a1. (clean and dtok set): merge words into sentences; this takes individual files from `fisher/cleaned/{train,valid}` and puts them in `fisher/fisher_clean/{train,valid}`:
   
    ./src/merge_lines.sh {train,valid}

   2b. make big text file to be used in ngram models:
   
    
    cat train/* > train.txt
    cat valid/* > valid.txt
    

   2c. change things like "s" to "'s" in train.txt and valid.txt (clean and disf versions, not in dtok version):
    
    
    %s/\<s\>/'s/g
    %s/\<ll\>/'ll/g
    %s/\<m\>/'m/g
    %s/\<ve\>/'ve/g
    %s/\<d\>/'d/g
    %s/\<re\>/'re/g
    
   2d. IMPORTANT: if using for surprisal error analysis, change a few more things.  This is not done yet in the raw data!:

    %s/\.//g
    %s/you know/you_know/g
____________________________________________________
The corresponding data are in `/g/ssli/projects/disfluencies/ttmt001/fisher_{disf,clean,dtok}` (without step 2d!)


**3. Make vocabulary from training files** (specific to ngrams):

`python src/ngrams/make_vocab.py --step make_vocab --dtype {disf,clean,dtok}`

**4. Split to smaller chunks:** 
Need this for LSTM model only -- split train.txt and valid.txt into smaller chunks to facilitate parallelization (do this in the directory of your data):

```
split -d -n 40 train.txt
split -d -n 10 valid.txt
```

**5. Train ngrams:**

`./src/ngrams/ngram-lms.sh {disf,clean,dtok}`

**6. Prepare switchboard** (or other dataset) sentences to compute ppl score:

`python src/preprocess_for_models.py swbd_file output_file --tagging`

This produces swbd_*_sents.txt

* ptb = Penn Treebank version of transcripts
* ms = Mississippi State version of transcripts


**7. Compute ngram scores:**

`./src/ngrams/ngram-eval.sh {disf,clean,dtok} {ms,ptb}`


This computes LM model scores (perplexity) on the SWBD dataset.


**8. Convert OOV tokens** to `<unk>` -- preparation step for LSTM LM models:
```
python src/make_vocab.py \
   --train_file {x01,..} \
   --dtype {disf,clean,dtok} \
   --unk_split {train,valid}_splits \
   --step prep_data
```

Batching this:

`src/run_make_vocab.sh {valid,train} {clean,disf,dtok}`

Then 

`cat x*_with_unk files > {train,valid}_with_unk.txt`

**9. Prepare bucketed data** for training LSTM LMs:

NOTE: need to add special words to both clean and disf fisher vocabs: 

`<eos>, <sos>, <pad>`

`python src/lstm_lm/data_preprocess.py --dtype {disf,clean,dtok} --split {valid,train}`

**10. Train LSTM language model** on fisher and score on SWBD:

`./src/lstm_lm/job{5000,5001,5002}.sh`

(Note - the latest version for swbd surprisal analysis is job 5004.  It actually uses a GRU (despite the lstm naming conventions)

**11. Make table of scores**:

```
lstm_lm/run_eval_lstm.sh disf 5000 {ms,ptb}
lstm_lm/run_eval_lstm.sh clean 5001 {ms,ptb}
lstm_lm/run_eval_lstm.sh dtok 5002 {ms,ptb}
```
**12. Get perplexity scores**:
lstm_lm/getppl.sh {ms, ptb}

