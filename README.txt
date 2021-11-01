CS 337 Project 1: Tweet Mining & The Golden Globes

Team Members: Abigail Coneeny, Rachel Kantor, Ran Sa

Due Date: 31 October 2021


To run this project, please create a python venv then run pip install -r requirements.txt. You also must install ... 

Spacy:
pip install -U pip setuptools wheel
pip install -U spacy

You need to download the model for spacy:
python -m spacy download en_core_web_sm

You also need to download the model for textblob:
python -m textblob.download_corpora

Once this is complete, run 'python autograder.py <year>'. This calls the gg_api.py file that uses accessor functions to display information from 'extraction.py'.
This will run the minimal requirement of the project.

To run the extra features, please run...
python extraction.py
!!!Warning!!!:
Please run the minimum requirement before running any additional features. For example, if you want to run additional features for 2013, then you should run the minimal requirement for 2013 before running the additional features.
There are three extra features included in this project:
1. It will look for the best dress, worst dress, and most controversial celebrities during the golden globe (worst and controversial are not guaranteed to be found). It will also attach the brand of the outfit and a link to the image if possible.
2. It will look for the most unexpected event during the golden globe and show a few tweets that are related to this event.
3. It will look for the most unexpected winner and search for the candidate that most people thought will win the award.
To run the additional features for a different year, please change the year number in line 161 and 162 in the extraction file.


The Github Repo can be found at https://github.com/aconeeny9/337Project1.git, with the final version of the code held in the 'framework' branch.


RunTime:
2013:
Minimal requirement: 0m 29s
Additional features: 0m 40s

2015:
Minimal requirement: 4m 35s
Additional features: 10m 19s

Hardware tested on:
CPU: Intel i7 11700k
RAM: 32G DDR4
