# Method used to segment Chinese translations

import pandas as pd
import jieba
import sys
import os

# Method takes input of text and returns the segmented version
def segment_text(text: str)-> str:
    text_jb = jieba.lcut(text)
    text = ' '.join(text_jb)
    return text

# Method can be used if run in standalone CLI (not part of main.py)
def update_table(filename):
    df = pd.read_table(filename)
    sent_list = df['translated'].values.tolist()
    df['trans_seg'] = df['translated'].apply(segment_text)
    df['target_seg'] = df['targetString'].apply(segment_text)
    df.to_csv(filename, sep='\t')

# Method can be used if run in standalone CLI (not part of main.py)
def find_zh_file(trans_directory):
        for filename in os.listdir(trans_directory):
            if filename.endswith('.tsv') and not filename.startswith('.'):
                with open(os.path.join(trans_directory, filename)) as f:
                    df = pd.read_table(f)
                    targetLang = df['targetLang'].iloc[0]
                    if targetLang == 'zh':
                        return f

# Method used in main.py
# Input is a directory of translations
# Method finds the Chinese file and then updates that file with segmented data
def segment(out_directory):
    for filename in os.listdir(out_directory):
        if filename.endswith('.tsv') and not filename.startswith('.'):
            with open(os.path.join(out_directory, filename)) as f:
                df = pd.read_table(f)
                targetLang = df['targetLang'].iloc[0]
                if targetLang == 'zh':
                    df['trans_seg'] = df['translated'].apply(segment_text)
                    df['target_seg'] = df['targetString'].apply(segment_text)
                    df.to_csv(os.path.join(out_directory, filename), sep='\t')
                    break


if __name__ == '__main__':
    filename = sys.argv[1]
    update_table(filename)
