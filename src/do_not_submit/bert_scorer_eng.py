# Method obtains BERTscores for all translations in a directory

from bert_score import BERTScorer
import pandas as pd
import os
import sys

# Method obtains BERTscores for sentences translated INTO English
# Obtains scores both rescaled to baseline and not rescaled to baseline
# Saves all scores in a .tsv file
def score_x_to_english(directory):
        scores = []
        for filename in os.listdir(directory):
                if filename.endswith('.tsv'):
                        with open(os.path.join(directory, filename)) as f:
                                scorer = BERTScorer(lang='en', rescale_with_baseline=True)
                                df = pd.read_table(f)
                                source = df['targetLang'].iloc[0]
                                target = 'en'
                                ref_list = df['sourceString'].values.tolist()
                                refs_formateed = []
                                for r in ref_list:
                                        refs_formateed.append([r])
                                hyps = df['translatedEng'].values.tolist()
                                P, R, F1 = scorer.score(hyps, refs_formateed)
                                precision_rescaled = P.mean().item()
                                recall_rescaled = R.mean().item()
                                f1_score_rescaled = F1.mean().item()
                                print(source + ' rescaled ' + str(f1_score_rescaled))
                                scorer = BERTScorer(lang='en', rescale_with_baseline=False)
                                P, R, F1 = scorer.score(hyps, refs_formateed)
                                precision = P.mean().item()
                                recall = R.mean().item()
                                f1_score = F1.mean().item()
                                print(source + ' not rescaled ' + str(f1_score))
                                
                                scores.append([source, target, f1_score_rescaled, precision_rescaled, recall_rescaled, f1_score, precision, recall])
        scores_df = pd.DataFrame(scores, columns=['sourceLang',
                                                  'targetLang',
                                                  'F1_rescaled',
                                                  'precision_rescaled',
                                                  'recall_rescaled',
                                                  'F1',
                                                  'precision',
                                                  'recall'])
        write_name = directory + '/scores/BERT_scores_to_english.tsv'
        scores_df.to_csv(write_name, sep='\t')
