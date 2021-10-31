import string

import util
from Host import Host
from Awards_temp import Awards
from Winner import Winner
from RedCarpet import RedCarpet
import imdb_checker
import json
from Nominees import Nominees
from Surprise import Surprise
import re

# please add any bad keywords here
blacklist_keywords = [
    ["blacklist",
     ["predict", "predicts", "predicted", "prediction", "predictions", "next year", "bet", "guess", "wish"]]
]

# please add any good keywords here
whitelist_keywords = [
    ["host", ["host", "hosts", "hosting", "hosted"]],
    ['best', ['Best']],
    ["win", ['wins', 'winning']],
    ['winner', ['winner']],
    ['go to', ['goes to']],
    ['award', ['is awarded to']]
]
host_scanner = Host()
awards_scanner = Awards()
winner_scanner = Winner()
nominees_scanner = Nominees()


def tweet_extraction(year, award_list):
    imdb_checker.load_dataset(year)
    winner_scanner.set_awards(award_list)
    addition = ['cecil', []]
    for award in award_list:
        if award.split()[0].lower() != 'best':
            word1 = award.split()[0]
            word2 = award.split()[1]
            word1 = word1[0].upper()+word1[1:]
            word2 = word2[0].upper()+word2[1:]
            addition[1].append(' '.join([word1, word2]).strip(string.punctuation))
    whitelist_keywords.append(addition)
    # load tweet from csv
    path = 'gg{}.json'.format(year)
    tweets = []
    with open(path, 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        # iterate through all the tweets and extract information from them
        for index, tweet in enumerate(data):
            tweet = tweet['text']
            tweets.append(tweet)
            # check if the tweet contain any bad keywords
            if util.keyword_matcher(blacklist_keywords, tweet)[0]:
                continue
            # check if the tweet contain any good keywords
            contain_keyword, match_list = util.keyword_matcher(whitelist_keywords, tweet)
            if contain_keyword:
                match_dic = util.merge_matches(match_list)
                host_scanner.scanner_dispatch(match_dic, tweet)
                awards_scanner.scanner_dispatch(match_dic, tweet)
                winner_scanner.scanner_dispatch(match_dic, tweet)
    host_scanner.evaluate()
    awards_scanner.evaluate()
    winner_scanner.evaluate()
    winners = get_winner()
    nominees_scanner.set_winner(winners)
    keywords = []
    for key in winners:
        keywords.append([key, [winners[key]], [winners[key].lower()], [winners[key].upper()]])
    nominees_scanner.set_awards(award_list)
    for tweet in tweets:
        contain_keyword, match_list = util.keyword_matcher(keywords, tweet)
        if contain_keyword:
            match_dic = util.merge_matches(match_list)
            nominees_scanner.scanner_dispatch(match_dic, tweet)
    nominees_scanner.evaluate()
    print(host_scanner.to_string())
    util.write_json([host_scanner], 'gg2013.json')

def red_carpet(year):
    red_carpet_scanner = RedCarpet()
    keywords = [
        ["red carpet", ["red carpet", "Red Carpet", "red carpet".upper(), 'redcarpet', 'dress']]]
    path = 'gg{}.json'.format(year)
    with open(path, 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        for index, tweet in enumerate(data):
            tweet = tweet['text']
            # check if the tweet contain any good keywords
            contain_keyword, match_list = util.keyword_matcher(keywords, tweet)
            if contain_keyword:
                match_dic = util.merge_matches(match_list)
                red_carpet_scanner.scanner_dispatch(match_dic, tweet)
    red_carpet_scanner.evaluate()

def surprise(year):
    surprise_scanner  = Surprise()
    path = 'gg{}.json'.format(year)
    with open(path, 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        for index, tweet in enumerate(data):
            tweet = tweet['text']
            # check if the tweet contain any good keywords
            surprise_scanner.scanner_dispatch(tweet)
    surprise_scanner.evaluate()



def get_host():
    return host_scanner.host_name


def get_award():
    return awards_scanner.awards_list


def get_winner():
    return winner_scanner.winner

def get_nominees():
    return nominees_scanner.nominees


if __name__ == '__main__':
    OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama',
                            'best performance by an actress in a motion picture - drama',
                            'best performance by an actor in a motion picture - drama',
                            'best motion picture - comedy or musical',
                            'best performance by an actress in a motion picture - comedy or musical',
                            'best performance by an actor in a motion picture - comedy or musical',
                            'best animated feature film', 'best foreign language film',
                            'best performance by an actress in a supporting role in a motion picture',
                            'best performance by an actor in a supporting role in a motion picture',
                            'best director - motion picture', 'best screenplay - motion picture',
                            'best original score - motion picture', 'best original song - motion picture',
                            'best television series - drama',
                            'best performance by an actress in a television series - drama',
                            'best performance by an actor in a television series - drama',
                            'best television series - comedy or musical',
                            'best performance by an actress in a television series - comedy or musical',
                            'best performance by an actor in a television series - comedy or musical',
                            'best mini-series or motion picture made for television',
                            'best performance by an actress in a mini-series or motion picture made for television',
                            'best performance by an actor in a mini-series or motion picture made for television',
                            'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                            'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

    #tweet_extraction(2013, OFFICIAL_AWARDS_1315)
    #red_carpet(2013)
    surprise(2013)
