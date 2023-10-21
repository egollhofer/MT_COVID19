import os
import sys
import re
import pandas as pd


def remove_punctuation(text):
    text = re.sub(r'^(\[\')', '', text)
    text = re.sub(r'(\'\])$', '', text)
    return text

def update_translations(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.tsv') and not filename.startswith('.'):
            with open(os.path.join(directory, filename)) as f:
                df = pd.read_table(f)
                df['translated'] = df['translated'].apply(remove_punctuation)
                out_name = '/Users/elizabethgollhofer/Desktop/575/LT4CPR/data/azure_out/' + filename
                df.to_csv(out_name, sep='\t')

if __name__ == '__main__':
    directory = sys.argv[1]
    update_translations(directory)
