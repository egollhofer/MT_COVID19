# Program iterates through a directory of files containing gold translations and machine translations
# Each file contains data from English to one target language
# Finds the BLEU score for each file and writes a .tsv with all BLEU scores

import sys
from sacrebleu.metrics import BLEU
import pandas as pd
import os

def score_english_to_x(directory):
    bleu = BLEU()
    scores = []
    for filename in os.listdir(directory):
        if filename.endswith('.tsv') and not filename.startswith('.'):
            with open(os.path.join(directory, filename)) as f:
                df = pd.read_table(f)
                source = df['sourceLang'].iloc[0]
                target = df['targetLang'].iloc[0]
                if target != 'zh':
                    refs = [df['targetString'].values.tolist()]
                    hyps = df['translated'].values.tolist()
                    result = bleu.corpus_score(hyps, refs)
                    print(result)
                    scores.append([source, target, result.score, result.precisions, result.bp, result.ratio])

                # Chinese data file is formatted differently, so section of code looks to utilize segmented column
                else:
                    refs = [df['target_seg'].values.tolist()]
                    hyps = df['trans_seg'].values.tolist()
                    result = bleu.corpus_score(hyps, refs)
                    print(result)
                    scores.append([source, target, result.score, result.precisions, result.bp, result.ratio])
    scores_df = pd.DataFrame(scores, columns=['sourceLang',
                                                  'targetLang',
                                                  'BLEUscore',
                                                  'precisions',
                                                  "brevityPenalty",
                                                  'ratio'])                    
    write_name = directory + "/scores/BLEU_scores_from_English.tsv"
    scores_df.to_csv(write_name, sep='\t')

if __name__ == '__main__':
    translated_directory = sys.argv[1]
    score_english_to_x(translated_directory)
