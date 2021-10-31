import numpy as np

import util
import imdb_checker
import re


def suitable_candidate(award_name, candidate):
    if award_name.split()[0].lower() != 'best':
        return any([imdb_checker.is_imdb_actor(candidate), imdb_checker.is_imdb_actress(candidate),
                    imdb_checker.is_imdb_director(candidate)])
    elif 'actor' in award_name:
        return imdb_checker.is_imdb_actor(candidate)
    elif 'actress' in award_name:
        return imdb_checker.is_imdb_actress(candidate)
    elif 'director' in award_name:
        return imdb_checker.is_imdb_director(candidate)
    else:
        return imdb_checker.is_imdb_title(candidate)


def okay_candidate(award_name, candidate):
    if 'actor' in award_name or 'actress' in award_name or 'director' in award_name:
        return imdb_checker.is_imdb_person(candidate)


class Nominees:
    def __init__(self):
        self.nominees = {}
        self.nominees_dic = {}

    def set_awards(self, award_list):
        self.awards_list = award_list
        for award_name in self.awards_list:
            self.nominees[award_name] = []
            self.nominees_dic[award_name] = {}

    def set_winner(self, winner_dic):
        self.winner_dic = winner_dic

    def scanner_dispatch(self, match_dic, tweet):
        pattern = "\s+rt+\s"
        match = re.search(pattern, tweet.lower())
        if match or tweet.lower()[:3] == 'rt ':
            return
        for match_key in match_dic:
            self.__search_nominees(tweet, match_key)


    def __search_nominees(self, tweet, award_name):
        if 'best' in tweet.lower():
            return
        key_words = ['beat', 'better', 'should', 'contender', 'think', 'thought', 'more', 'match', 'against', 'nominados', 'nominate', 'bet', 'want', 'over']
        if not any([key in tweet.lower() for key in key_words]):
            return
        #print(tweet)
        clean_tweet = re.sub(r"[^\w\s\-\\'\"\:]+", '', tweet)
        split_tweet = clean_tweet.split()
        forward = util.search_forward(split_tweet, 0, 10)
        for candidate in forward:
            if suitable_candidate(award_name, candidate) and candidate.lower() not in award_name:
                if candidate in self.nominees_dic[award_name]:
                    self.nominees_dic[award_name][candidate] += 1
                else:
                    self.nominees_dic[award_name][candidate] = 1
            elif okay_candidate(award_name, candidate) and candidate.lower() not in award_name:
                if candidate in self.nominees_dic[award_name]:
                    self.nominees_dic[award_name][candidate] += 0.1
                else:
                    self.nominees_dic[award_name][candidate] = 0.1


    def evaluate(self):
        for award_name in self.nominees_dic:
            if award_name[:4].lower() != 'best':
                self.nominees[award_name] = []
                continue
            keys = []
            values = []
            for key in self.nominees_dic[award_name]:
                keys.append(key)
                values.append(self.nominees_dic[award_name][key])
            if len(keys)<1:
                continue
            keys, values = self.__merge(keys, values)
            sort_index = np.argsort(values)[::-1]
            keys = keys[sort_index]
            values = values[sort_index]
            self.nominees[award_name] = keys.tolist()[:5]
            winner = self.winner_dic[award_name]
            if winner in self.nominees[award_name]:
                self.nominees[award_name].remove(winner)
            else:
                self.nominees[award_name] = self.nominees[award_name][:-1]

    def __merge(self, keys, values):
        remove = []
        for index, key in enumerate(keys):
            if len(key.split()) > 1:
                for index1, key1 in enumerate(keys):
                    if key1 != key and (re.search(r'\b{}\b'.format(key1), key) or re.search(
                            r'\b{}\b'.format(key1.lower()), key)):
                        values[index] += values[index1]
                        remove.append(index1)
        keys = np.array(keys)
        values = np.array(values)
        keys = np.delete(keys, remove)
        values = np.delete(values, remove)
        return keys, values