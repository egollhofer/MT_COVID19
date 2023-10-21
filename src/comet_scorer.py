# Program iterates through a directory of files containing gold translations and machine translations
# Each file contains data from English to one target language
# Finds the COMET score for each file (if covered) and wrties to .tsv output

import os
import sys
import pandas as pd
from comet import download_model, load_from_checkpoint

model_path = download_model("Unbabel/wmt22-comet-da")
model = load_from_checkpoint(model_path)

# Need a list of supported languages by Comet
comet_supported_languages = {'am', 'ar', 'bn', 'zh', 'fa', 'fr', 'hi', 'id', 'ku', 'mr', 'ms', 'ne', 'ps', 'pt-BR', 'ru',
                             'so', 'ur', 'es-LA', 'sw'}

# Method returns the data in format required by Comet for scoring
# Data must be in a list of dictionarys
# keys 'src', 'mt', and 'ref' and values are sentences
def format_data(df):
    src_list = df['sourceString'].values.tolist()
    mt_list = df['translated'].values.tolist()
    ref_list = df['targetString'].values.tolist()
    data_list = []
    for i in range(len(src_list)):
        data_dict = {'src': src_list[i], 'mt': mt_list[i], 'ref': ref_list[i]}
        data_list.append(data_dict)
    return data_list

# Method goes through files in a dictionary of translations from English
# Checks to see if file is a supported langauge
# If supported, obtains the COMET score for the language
# Saves all scores in a .tsv
def score_directory_from_english(directory):
    score_list = []
    # iterate through the directory
    for filename in os.listdir(directory):
        if filename.endswith('.tsv') and not filename.startswith('.'):
            with open(os.path.join(directory, filename)) as f:
                df = pd.read_table(f)
                targetLang = df['targetLang'].iloc[0]
                if targetLang == 'es-419' or targetLang == 'es':
                    targetLang = 'es-LA'
                if targetLang in comet_supported_languages:
                    data_list = format_data(df)
                    model_output = model.predict(data_list, batch_size=8, gpus=0)
                    system_score = model_output['system_score']
                    score_list.append([targetLang, system_score])
                    print(targetLang + " " + str(system_score))
                else:
                    print(targetLang + " is unsupported")
    score_df = pd.DataFrame(score_list, columns=['targetLang', 'system score'])
    out_name = directory + '/scores/comet_scores_from_english.tsv'
    score_df.to_csv(out_name, sep='\t')

if __name__ == '__main__':
    directory = sys.argv[1]
    score_directory_from_english(directory)
