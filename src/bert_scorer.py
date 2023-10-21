# Program iterates through a directory of files containing gold translations and machine translations
# Each file contains data from English to one target language
# Finds the BERTscore for each file and writes to a .tsv output

from bert_score import BERTScorer
import pandas as pd
import os
import sys



# Method obtains BERTscores for sentences translated from English
# Scores are NOT rescaled
# Saves all scores in a .tsv file
def score_english_to_x(directory):
        scores = []
        for filename in os.listdir(directory):
                if filename.endswith('.tsv') and not filename.startswith('.'):
                        with open(os.path.join(directory, filename)) as f:
                                df = pd.read_table(f)
                                target = df['targetLang'].iloc[0]
                                source = 'en'
                                if target != 'zh':
                                        try:
                                                scorer = BERTScorer(lang=target)
                                                ref_list = df['targetString'].values.tolist()
                                                refs_formateed = []
                                                for r in ref_list:
                                                        refs_formateed.append([r])
                                                hyps = df['translated'].values.tolist()
                                                P, R, F1 = scorer.score(hyps, refs_formateed)
                                                precision = P.mean().item()
                                                recall = R.mean().item()
                                                f1_score = F1.mean().item()
                                                print(target + " " + str(f1_score))
                                                scores.append([source, target, f1_score, precision, recall, "no baseline"])
                                        except ValueError:
                                                print("Abbreviation not found for language: " + target)
                                # Chinese files are in a different format as it is segmented after translation
                                # This section of code is written for the updated formatting of Chinese files to use segmented columns of file
                                else:
                                        scorer = BERTScorer(lang=target)
                                        ref_list = df['target_seg'].values.tolist()
                                        refs_formateed = []
                                        for r in ref_list:
                                                refs_formateed.append([r])
                                        hyps = df['trans_seg'].values.tolist()
                                        P, R, F1 = scorer.score(hyps, refs_formateed)
                                        precision = P.mean().item()
                                        recall = R.mean().item()
                                        f1_score = F1.mean().item()
                                        print(target + " " + str(f1_score))
                                        scores.append([source, target, f1_score, precision, recall, "no baseline"])
        scores_df = pd.DataFrame(scores, columns=['sourceLang',
                                                          'targetLang',
                                                          'F1',
                                                          'precision',
                                                          'recall',
                                                          'baseline?'])
        write_name = directory + '/scores/BERT_scores_from_english.tsv'
        scores_df.to_csv(write_name, sep='\t')

if __name__ == '__main__':
    translated_directory = sys.argv[1]
    score_english_to_x(translated_directory)

