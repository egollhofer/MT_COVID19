# Method reads translations from English to generic Tigrinya
# Adds those translations to the files with unique dialects of Tigrinya

import os
import sys
import re
import pandas as pd

# Method written for use as standalone code (not part of main.py pipleine)
def add_translations_old(file, api, out_directory):
    ti_dr = '../data/tico19-testset/test/tigrinya'
    with_translations = pd.read_table(file)
    translation_list = with_translations['translated'].values.tolist()
    for filename in os.listdir(ti_dr):
        if filename.endswith('.tsv') and not filename.startswith('.'):
            with open(os.path.join(ti_dr, filename)) as f:
                df = pd.read_table(f)
                df['translated'] = translation_list
                out_name = re.sub(r'(\.tsv)$', '', filename)
                out_name = out_directory + '/' + out_name + "_" + api + '.tsv'
                df.to_csv(out_name, sep='\t')

# Method written for use in main.py to update Microsoft translate files    
def add_translations_microsoft(data_directory, azure_out_directory):
    # find the folder storing un-translated TI dialects
    ti_dr = data_directory + '/tigrinya'
    # get the translations using Microsoft into generic ti dialect
    ti_microsoft = identify_translations(azure_out_directory)
    ti_microsoft_translations = ti_microsoft['translated'].values.tolist()
    # add translations to un-translated TI dialects and save them in output
    for filename in os.listdir(ti_dr):
        if filename.endswith('.tsv') and not filename.startswith('.'):
            with open(os.path.join(ti_dr, filename)) as f:
                df = pd.read_table(f)
                df['translated'] = ti_microsoft_translations
                out_name = re.sub(r'(\.tsv)$', '', filename)
                out_name = azure_out_directory + '/' + out_name + '_microsoft.tsv'
                df.to_csv(out_name, sep='\t')

# Method written for use in main.py to update Goolge translate files 
def add_translations_google(data_directory, google_out_directory):
    # find the folder storing un-translated TI dialects
    ti_dr = data_directory + '/tigrinya'
    # get the translations using google into generic ti dialect
    ti_google = identify_translations(google_out_directory)
    ti_google_translations = ti_google['translated'].values.tolist()
    # add translations to un-translated TI dialects and save them in output
    for filename in os.listdir(ti_dr):
        if filename.endswith('.tsv') and not filename.startswith('.'):
            with open(os.path.join(ti_dr, filename)) as f:
                df = pd.read_table(f)
                df['translated'] = ti_google_translations
                out_name = re.sub(r'(\.tsv)$', '', filename)
                out_name = google_out_directory + '/' + out_name + '_google.tsv'
                df.to_csv(out_name, sep='\t')

# Method finds Tigrinya translations in a directory of many translations
def identify_translations(trans_directory):
    for filename in os.listdir(trans_directory):
        if filename.endswith('.tsv') and not filename.startswith('.'):
            with open(os.path.join(trans_directory, filename)) as f:
                df = pd.read_table(f)
                targetLang = df['targetLang'].iloc[0]
                if targetLang == 'ti':
                    return df

    

if __name__ == '__main__':
    file = sys.argv[1]
    api = sys.argv[2]
    out_directory = sys.argv[3]
    add_translations_old(file, api, out_directory)
