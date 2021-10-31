import string

import util
from Host import Host
from Awards import Awards
from Winner import Winner
from nominees_to_awards import Nominees
from Presenter import Presenter
import imdb_checker
import json

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
presenter_scanner = Presenter()

def tweet_extraction(year, award_list):
    imdb_checker.load_dataset(year)
    winner_scanner.set_awards(award_list)
    presenter_scanner.set_awards(award_list)
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
    with open(path, 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        # iterate through all the tweets and extract information from them
        for index, tweet in enumerate(data):
            #if index % 10000 == 0:
                #print(index)
            tweet = tweet['text']
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
            presenter_scanner.scanner_dispatch(tweet)
    host_scanner.evaluate()
    awards_scanner.evaluate()
    winner_scanner.evaluate()
    nominees_scanner.evaluate(data, award_list)
    presenter_scanner.set_winners(winner_scanner.winner)
    presenter_scanner.evaluate()
    print(host_scanner.to_string())
    util.write_json([host_scanner], 'gg2013.json')
        with open('winner.pkl', 'wb') as winner_file:
        pickle.dump(winner_scanner.winner, winner_file)



def red_carpet(year):
    imdb_checker.load_dataset(year)
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
    imdb_checker.load_dataset(year)
    surprise_scanner = Surprise()
    with open('winner.pkl', 'rb') as data_file:
        winners = pickle.load(data_file)
    path = 'gg{}.json'.format(year)
    with open(path, 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        keywords = []
        for key in winners:
            keywords.append([key, [winners[key]], [winners[key].lower()], [winners[key].upper()]])
        surprise_scanner.set_winner(winners)
        for index, tweet in enumerate(data):
            tweet = tweet['text']
            contain_keyword, match_list = util.keyword_matcher(keywords, tweet)
            if contain_keyword:
                match_dic = util.merge_matches(match_list)
                surprise_scanner.scanner_dispatch_1(match_dic, tweet)
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


def get_presenter():
    return presenter_scanner.presenter


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

    tweet_extraction(2013, OFFICIAL_AWARDS_1315)
    #red_carpet(2013)
    #surprise(2013)
