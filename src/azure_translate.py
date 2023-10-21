# This program iterates through a directory of files containing .tsv files of sentences to translate
# opens each file and obtains translations from Microsoft translate
# it will send all languages to the API to be translated, and will print an error if the language is unsupported
# adds new translation to the dataframe and saves as a new file in target output directory

import requests
import uuid
import pandas as pd
import os
import sys

# Details of my account - needs to be sent with request
key = 'insert_your_key_here'
endpoint = "https://api.cognitive.microsofttranslator.com"
location = 'westus2'
path = '/translate'
constructed_url = endpoint + path

# Information that is sent with each request
headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# Parameters sent with each request
# The code updates with 'to' and 'from' based on the languages of sentences in each document
params = {
    'api-version': '3.0',
}

# Following method is written to translate from the source language to target
# In TICO files, the source langauge is always English, so this method only translates E->X
def translate_directory(directory, out_directory):
    for filename in os.listdir(directory):
        if filename.endswith('.tsv') and not filename.startswith('.'):
            with open(os.path.join(directory, filename)) as f:
                print(filename)
                supported = True
                data = pd.read_table(f)
                to_lang = data['targetLang'].iloc[0]
                if to_lang == 'es-LA':
                    to_lang = 'es'
                elif to_lang == 'zh':
                    to_lang = 'zh-Hans'
                sourceLang = data['sourceLang'].iloc[0]
                # Update the parameters with the source and target language
                params['to'] = to_lang
                params['from'] = sourceLang
                sent_list = data['sourceString'].values.tolist()
                new_list = []
                # The code is written to send each sentences one at a time
                # There is an hourly character limit and a per-request character limit
                # As I am not interested in speed it sends sentenes one at a time to avoid exceeding limits
                for sent in sent_list:
                    body = []
                    body.append({'text': sent})
                    request = requests.post(constructed_url, params=params, headers=headers, json=body)
                    if request.reason == "Bad Request":
                        # This happens when the language is unsupported
                        supported = False
                        print("######################################")
                        print('unsupported language found: ' + to_lang)
                        break
                    response = request.json()
                    try:
                        translated = response[0]['translations'][0]['text']
                        new_list.append([translated])
                        print(translated)
                    except KeyError:
                        # Prevent the code from crashing if no translation is returned (ie, run of out free translations)
                        translated = ''
                        new_list.append([translated])
                        print("KeyError: no translation returned.  Language is " + to_lang)
                if supported:
                    data['translated'] = new_list
                    write_name = out_directory + '/' + sourceLang + '-' + to_lang + '_microsoft.tsv'
                    data.to_csv(write_name, sep='\t')

if __name__ == '__main__':
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    translate_directory(input_directory, output_directory)
