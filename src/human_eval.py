# Gets subset of 50 sentences each from:
    # Somali -> English translations by Microsoft and Google
    # French -> English translations by Microsoft and Goolge
    # Marathi -> English translations by Microsoft and Google
# First, run get sample and comment out "unscramble"
# Give to human evaluator and have them put in their scores
# Comment out get sample and run "unscramble" to get average
# scores for each language and each API

# Can be run in a demo mode with both unscrambled
# If run in demo mode, will return scores of 100.0 for all evaluations

import random
import pandas as pd

# Method gets a random list of 50 indices from 2100
def get_indices():
    all_indices = []
    for i in range(2100):
        all_indices.append(i)
    sample = random.sample(all_indices, 50)
    return sample

# Method gets a subset of 50 random sentences
# Adds column indicating MT API is Google
def get_sentences_google(df):
    indices = get_indices()
    subset = df.iloc[indices]
    subset['mt_api'] = 'google'
    return subset

# Method gets a subset of 50 random sentences
# Adds column indicating MT AP is Microsoft
def get_sentences_microsoft(df):
    indices = get_indices()
    subset = df.iloc[indices]
    subset['mt_api'] = 'microsoft'
    return subset


# Method which opens up the dataframe with all information, concatenates it with the scores
# get subsets for each langauge with each mt api
# finds mean scores for human eval of fluency and adequacy
# writes those scores to an output file
def unscramble(evaluator_name):
    out_directory = '../data/human_eval/' + evaluator_name
    out_filename = out_directory + '_all_data.tsv'
    sents_only_out_name = out_directory + '_sents_only.tsv'
    human_evals = []
    sents = pd.read_table(out_filename)
    scores = pd.read_table(sents_only_out_name)
    combined = pd.concat([sents, scores], axis=1)
    so = combined[combined['targetLang'] == 'so']
    so_g = so[so['mt_api'] == 'google']
    ascore = so_g['adequacy'].mean()
    fscore = so_g['fluency'].mean()
    human_evals.append(['so', 'google', ascore, fscore])
    so_m = so[so['mt_api'] == 'microsoft']
    ascore = so_m['adequacy'].mean()
    fscore = so_m['fluency'].mean()
    human_evals.append(['so', 'microsoft', ascore, fscore])
    mr = combined[combined['targetLang'] == 'mr']
    mr_g = mr[mr['mt_api'] == 'google']
    ascore = mr_g['adequacy'].mean()
    fscore = mr_g['fluency'].mean()
    human_evals.append(['mr', 'google', ascore, fscore])
    mr_m = mr[mr['mt_api'] == 'microsoft']
    ascore = mr_m['adequacy'].mean()
    fscore = mr_m['fluency'].mean()
    human_evals.append(['mr', 'microsoft', ascore, fscore])
    fr = combined[combined['targetLang'] == 'fr']
    fr_g = fr[fr['mt_api'] == 'google']
    ascore = fr_g['adequacy'].mean()
    fscore = fr_g['fluency'].mean()
    human_evals.append(['fr', 'google', ascore, fscore])
    fr_m = fr[fr['mt_api'] == 'microsoft']
    ascore = fr_m['adequacy'].mean()
    fscore = fr_m['fluency'].mean()
    human_evals.append(['fr', 'microsoft', ascore, fscore])
    eval_df = pd.DataFrame(human_evals, columns=['language', 'api', 'adequacy', 'fluency'])
    score_summary_filename = out_directory + '_score_summary.tsv'
    eval_df.to_csv(score_summary_filename, sep='\t')

# Method takes as input .tsv files with English translations of Somali, French, and Marathi data and name of evaluator
# Selects a subset of 50 random sentences from each file and concatenates into single DataFrame
# Shuffles the order of sentences to randomize
# Saves DataFrame to a new file
# Makes additional file with sentences for evaluation
def get_sample(somali_translations_google, somali_translations_microsoft, french_translations_google, french_translations_microsoft, marathi_translations_google, marathi_translations_microsoft, evaluator_name):
    so_google = pd.read_table(somali_translations_google)
    sents = get_sentences_google(so_google)
    so_microsoft = pd.read_table(somali_translations_microsoft)
    sents = pd.concat([sents, get_sentences_microsoft(so_microsoft)])
    fr_google = pd.read_table(french_translations_google)
    sents = pd.concat([sents, get_sentences_google(fr_google)])
    fr_microsoft = pd.read_table(french_translations_microsoft)
    sents = pd.concat([sents, get_sentences_microsoft(fr_microsoft)])
    mr_google = pd.read_table(marathi_translations_google)
    sents = pd.concat([sents, get_sentences_google(mr_google)])
    mr_microsoft = pd.read_table(marathi_translations_microsoft)
    sents = pd.concat([sents, get_sentences_microsoft(mr_microsoft)])
    sents = sents.sample(frac=1)
    out_directory = '../data/human_eval/' + evaluator_name
    out_filename = out_directory + '_all_data.tsv'
    sents.to_csv(out_filename, sep='\t')
    sents_only = sents[['sourceString', 'en-mt']]
    sents_only['adequacy'] = 100
    sents_only['fluency'] = 100
    sents_only_out_name = out_directory + '_sents_only.tsv'
    sents_only.to_csv(sents_only_out_name, sep='\t')

if __name__ == '__main__':
    somali_translations_google = '../data/data_from_Vipasha/google/so_en.tsv'
    somali_translations_microsoft = '../data/data_from_Vipasha/microsoft/so_en.tsv'
    french_translations_google = '../data/data_from_Vipasha/google/fr_en.tsv'
    french_translations_microsoft = '../data/data_from_Vipasha/microsoft/fr_en.tsv'
    marathi_translations_google = '../data/data_from_Vipasha/google/mr_en.tsv'
    marathi_translations_microsoft = '../data/data_from_Vipasha/microsoft/mr_en.tsv'
    evaluator_name = 'author_1'
    get_sample(somali_translations_google, somali_translations_microsoft, french_translations_google, french_translations_microsoft, marathi_translations_google, marathi_translations_microsoft, evaluator_name)
    unscramble(evaluator_name)

