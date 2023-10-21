# This program iterates through a directory of files containing .tsv files of sentences to translate
# opens each file and obtains translations from Goolge translate
# it will send all languages to the API to be translated, and will print an error if the language is unsupported
# adds new translation to the dataframe and saves as a new file in target output directory


import os
import sys
from google.cloud import translate_v2 as translate
import pandas as pd

# Env variable necessary for permission
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_key_here"


def translate_directory(directory, out_directory):
    translate_client = translate.Client()
    for filename in os.listdir(directory):
        if filename.endswith('.tsv') and not filename.startswith('.'):
            print(filename)
            with open(os.path.join(directory, filename)) as f:
                supported = True
                data = pd.read_table(f)
                targetLang = data['targetLang'].iloc[0]
                sourceLang = data['sourceLang'].iloc[0]
                sent_list = data['sourceString'].values.tolist()
                new_list = []
                for sent in sent_list:
                    try:
                        result = translate_client.translate(sent, target_language=targetLang)
                        try:
                            translated = result["translatedText"]
                            print(translated)
                            new_list.append(translated)
                        except KeyError:
                            # Prevent the code from crashing if no translation is returned 
                            translated = ''
                            new_list.append([translated])
                            print("KeyError: no translation returned.  Language is " + targetLang)
                    except BaseException:
                        # Prevent the code from crashing if no translation is returned (ie, run of out free translations, unsupported language)
                        supported = False
                        print("######################################")
                        print('Unable to translate: ' + targetLang)
                        break
                if supported:
                    data['translated'] = new_list
                    write_name = out_directory + '/' + sourceLang + '-' + targetLang + '_google.tsv'
                    data.to_csv(write_name, sep='\t')

if __name__ == '__main__':
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    translate_directory(input_directory, output_directory)
