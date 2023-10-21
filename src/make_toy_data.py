# Simple script used to make toy data directory with 5 sentences per file

import os
import pandas as pd

if __name__ == '__main__':
    directory = '../data/tico19-testset/test'
    toy_directory = '../data/data_toy'
    for filename in os.listdir(directory):
        if filename.endswith('.tsv') and not filename.startswith('.') and filename != 'test.en-kr.tsv' and filename != 'test.en-rw.tsv' and filename != 'test.en-ku.tsv':
            with open(os.path.join(directory, filename)) as f:
                print(filename)
                data = pd.read_table(f)
                data = data.head(5)
                new_name = toy_directory + '/' + filename + '_toy.tsv'
                data.to_csv(new_name, sep='\t')
                print(filename + ' worked!')
    ti_directory = '../data/tico19-testset/test/tigrinya'
    ti_toy = '../data/data_toy/tigrinya'
    for filename in os.listdir(ti_directory):
        if filename.endswith('.tsv') and not filename.startswith('.') and filename != 'test.en-kr.tsv' and filename != 'test.en-rw.tsv' and filename != 'test.en-ku.tsv':
            with open(os.path.join(ti_directory, filename)) as f:
                print(filename)
                data = pd.read_table(f)
                data = data.head(5)
                new_name = ti_toy + '/' + filename + '_toy.tsv'
                data.to_csv(new_name, sep='\t')
                print(filename + ' worked!')
