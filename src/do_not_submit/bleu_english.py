import sys
from sacrebleu.metrics import BLEU
import pandas as pd
import os

def score_x_to_english(directory):
    bleu = BLEU()
    scores = []
    for filename in os.listdir(directory):
        if filename.endswith('.tsv'):
            with open(os.path.join(directory, filename)) as f:
                df = pd.read_table(f)
                target = df['sourceLang'].iloc[0]
                source = 'en'
                refs = [df['targetString'].values.tolist()]
                hyps = df['translatedEng'].values.tolist()
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
    
