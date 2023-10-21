# LT4CPR

This repository was created as part of a class project for LING575 (Language Technology for Crisis Response) at the University of Washington.
This project evaluates the efficacy of commercially available machine translation tools on COVIT-19 related content.  For details of the findings, please reference the final report in this directory.


# The following readme was submitted to ensure graders were able to replicate my results.

### This code has been tested on Patas using a virtual enviroment
To set up your environment, please follow the steps described below:

1. Unzip repository

2. Navigate to directory src.  Reproduce the conda environment used for the project. Use this command:

```
#In directory src
conda env create -f 575_brown_env.yml
```
3. Activate the conda environment.  Use this command:

```
conda activate 575_brown_env
```
### To run an end-to-end version with toy data (5 sentences per language):

```
# You are encouraged to activate the virtual environment
conda activate 575_brown_env
# In directory src
./run.sh ../data/data_toy ../data/toy_azure ../data/toy_google
```

Important note: My Google account has utilized all of its credits, so the code will not translate using Google MT

The code will not crash - it will print a message letting you know it was unable to translate

The remainder of the code runs appropriately using sentences already translated in the Google toy output directory


### To collect the data used in the paper, the following steps were used:

Note: please do not run these steps!

The translations will exceed the cost of the remaining credits in my account

The scoring is a *very* lengthy process with the full TICO-19 dataset

```
# In directory src
# Environment activated 
conda activate 575_brown_env
# To get translations
python translate_with_google.py ../data/tico19-testset/test ../data/google_out
python azure_translate.py ../data/tico19-testset/test ../data/azure_out
# To segment Chinese data
python zh_segmentation.py ../data/google_out/en-zh_google.tsv
python zh_segmentation.py ../data/azure_out/en-zh-Hans_microsoft.tsv
# To add tigrinya translations to other dialects
python merge_ti.py ../data/azure_out/en-ti_microsoft.tsv microsoft ../data/azure_out
python merge_ti.py ../data/google_out/en-ti_google.tsv google ../data/google_out
# To score 
python score_bleu.py ../data/google_out
python score_bleu.py ../data/azure_out
python bert_scorer.py ../data/google_out
python bert_scorer.py ../data/azure_out
python comet_scorer.py ../data/google_out
python comet_scorer.py ../data/azure_out
```

### Selection of human evaluation sentences was completed outside the main pipeline
To run a demo version of this code you can run the following command
```
# In directory src
conda activate 575_brown_env
python human_eval.py
```

### Directory structure
### src directory
This folder contains all code, including yml file to create virtual environment.

### data directory
Folder azure_out contains all Microsoft translations and scores I obtained English -> X

Folder data_from_Vipasha contains translations and scores X->E provided by my collaborator

Folder data_toy contains a directory of files with only 5 sentences each so a demo version of the pipeline can be run

Folder google_out contains all Google translations and scores I obtained English -> X

Folder tico19-testset contains files downloaded from TICO-19.  Note this has been modified to remove test files with formatting errors and to separate out Tigrinya files.

Folder toy_azure contains all Microsoft translations and scores obtained running the main pipeline with the toy data directory.

Folder toy_google contains all Google translations and scores obtained running the main pipeline with the toy data directory.

### human_eval directory

If you are interested in looking at the sentences scored by the evaluators in this paper, you can look at the file all_sentences.tsv

There were some sentences that the evaluators feel may have been mis-aligned in the TICO files.

These sentences were scored for fluency but were not scored for accuracy.

Any sentence in all_sentences.tsv that does NOT have a score for accuracy may indicate an error in the original TICO file.
