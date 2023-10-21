import azure_translate
import bert_scorer
import comet_scorer
import merge_ti
import score_bleu
import translate_with_google
import zh_segmentation
import sys

if __name__ == '__main__':
    data_directory = sys.argv[1]
    azure_out_directory = sys.argv[2]
    google_out_directory = sys.argv[3]
    print('Starting to tranlsate with Microsoft')
    azure_translate.translate_directory(data_directory, azure_out_directory)
    print('Microsoft complete.  No credits left, so skipping Google.')
    #translate_with_google.translate_directory(data_directory, google_out_directory)
    print('Google complete.  Merging Tigrinya data')
    merge_ti.add_translations_microsoft(data_directory, azure_out_directory)
    merge_ti.add_translations_google(data_directory, google_out_directory)
    print('Tigrinya data combined.  Doing Chinese segmentation')
    zh_segmentation.segment(azure_out_directory)
    zh_segmentation.segment(google_out_directory)
    print('zh segmentation complete.  Scoring BLEU for Microsoft data')
    score_bleu.score_english_to_x(azure_out_directory)
    print('BLEU complete for Microsoft. Beginning Google')
    score_bleu.score_english_to_x(google_out_directory)
    print('All BLEU scores done. Beginning BERTscore for Microsoft data')
    bert_scorer.score_english_to_x(azure_out_directory)
    print('BERTscore complete for Microsoft data, beginning Google')
    bert_scorer.score_english_to_x(google_out_directory)
    print('BERTscores complete for all data. Begnning COMET for Microsoft')
    comet_scorer.score_directory_from_english(azure_out_directory)
    print('COMET complete for Microsoft, beginning Google')
    comet_scorer.score_directory_from_english(google_out_directory)
    print('All translations and scoring completed')
    
    
