import re
import string
import numpy as np
import nltk


class Awards:
    def __init__(self):
        self.awards_dic = {}
        self.awards_list = []

    def scanner_dispatch(self, match_dic, tweet):
        pattern = "\s+rt+\s"
        match = re.search(pattern, tweet.lower())
        if match or tweet.lower()[:3] == 'rt ':
            return
        win_match = False
        best_match = False
        goto_match = False
        winner_match = False
        award_match = False
        for match_key in match_dic:
            if match_key == "best":
                best_match = True
            if match_key == "win":
                win_match = True
            if match_key == 'go to':
                goto_match = True
            if match_key == 'winner':
                winner_match = True
            if match_key == 'award':
                award_match = True
        if best_match:
            if win_match and best_match:
                self.__search_win(tweet)
            elif goto_match and best_match:
                self.__search_goto(tweet)
            elif winner_match and best_match:
                self.__search_winner(tweet)
            elif award_match and best_match:
                self.__search_award(tweet)
            else:
                self.__search_best(tweet)

    def __add_to_dic(self, candidate):
        bad_key = ['gold', 'Gold', 'globe', 'Globe']
        if any([k in candidate for k in bad_key]):
            return
        candidate = candidate.strip()
        candidate = candidate.strip(string.punctuation)
        candidate = candidate.strip()
        match = re.search(r'\btv\b', candidate.lower())
        if match:
            candidate = re.sub(r'\btv\b', 'television', candidate.lower())
        candidate = candidate.lower()
        candidate = ' '.join(re.sub(r"[^\w\s]+", '', candidate).split())
        if len(candidate.split()) > 3:
            if candidate not in self.awards_dic:
                self.awards_dic[candidate] = 1
            else:
                self.awards_dic[candidate] += 1

    def __search_award(self, tweet):
        pattern = "best+\s(.+?)\s+is awarded to+\s"
        match_result = re.search(pattern, tweet.lower())
        if match_result:
            span = match_result.span()
            start = span[0]
            end = span[-1]
            tweet = tweet[start:end]
            short_tweet = ' '.join(tweet.split()[:-3])
            self.__add_to_dic(short_tweet)

    def __search_winner(self, tweet):
        pattern = "winner for+\s+best+\s"
        match_result = re.search(pattern, tweet.lower())
        if match_result:
            span = match_result.span()
            start = span[0]
            end = span[-1]
            rest = re.split(r'[.#?!]+', tweet[end:])
            if len(rest) > 0:
                rest = rest[0]
                d = ['for', 'is']
                d = r"\b(?:{})\b".format("|".join(d))
                rest = re.split(d, rest)[0]
            tweet = tweet[start:end] + rest
            short_tweet = ' '.join(tweet.split()[2:])
            self.__add_to_dic(short_tweet)

    def __search_win(self, tweet):
        pattern = "wins+\s+best+\s"
        pattern1 = "winning+\s+best+\s"
        match_result = re.search(pattern, tweet.lower())
        match_result1 = re.search(pattern1, tweet.lower())
        if match_result or match_result1:
            if match_result:
                span = match_result.span()
            else:
                span = match_result1.span()
            start = span[0]
            end = span[-1]
            rest = re.split(r'[.#?!]+', tweet[end:])
            if len(rest) > 0:
                rest = rest[0]
                d = ['for', 'is']
                d = r"\b(?:{})\b".format("|".join(d))
                rest = re.split(d, rest)[0]
            tweet = tweet[start:end] + rest
            short_tweet = ' '.join(tweet.split()[1:])
            self.__add_to_dic(short_tweet)

    def __search_goto(self, tweet):
        pattern = "best+\s(.+?)\s+goes to"
        match_result = re.search(pattern, tweet.lower())
        if match_result:
            span = match_result.span()
            start = span[0]
            end = span[-1]
            tweet = tweet[start:end]
            short_tweet = ' '.join(tweet.split()[:-2])
            self.__add_to_dic(short_tweet)

    def __search_best(self, tweet):
        pattern = "Best+\s(.+?)\s+: "
        match_result = re.search(pattern, tweet)
        if match_result:
            span = match_result.span()
            start = span[0]
            end = span[-1]
            tweet = tweet[start:end]
            short_tweet = ' '.join(tweet.split()[:-1])
            self.__add_to_dic(short_tweet)
            return
        pattern = "Best+\s(.+?): "
        match_result = re.search(pattern, tweet)
        if match_result:
            span = match_result.span()
            start = span[0]
            end = span[-1]
            tweet = tweet[start:end]
            self.__add_to_dic(tweet[:-1])
            return

        pattern = "best\s+(.+?)\s+-+\s"
        match_result = re.search(pattern, tweet.lower())
        if match_result:
            span = match_result.span()
            start, end = span
            self.__add_to_dic(tweet[start:end])

    def evaluate(self):
        keys = []
        values = []
        for key in self.awards_dic:
            keys.append(key)
            values.append(self.awards_dic[key])
        if len(keys) == 0:
            return
        keys, values = self.__merge(keys, values)
        sort_index = np.argsort(values)[::-1]
        keys = keys[sort_index]
        keys = keys.tolist()
        self.awards_list = keys[:26]


    def __merge(self, keys, values):
        remove = []
        for index, key in enumerate(keys):
            alter_key = self.__transform(key)
            if alter_key in keys:
                better_index = keys.index(alter_key)
                values[better_index] += values[index]
                remove.append(index)
        keys = np.array(keys)
        values = np.array(values)
        keys = np.delete(keys, remove)
        values = np.delete(values, remove)
        return keys, values

    def __transform(self, key):
        match = re.search(r'\bbest supporting actor\b', key)
        if match:
            result = re.sub(r'\bbest supporting actor\b', 'best performance by an actor in a supporting role', key)
            return result
        match = re.search(r'\bbest supporting actress\b', key)
        if match:
            result = re.sub(r'\bbest supporting actress\b', 'best performance by an actress in a supporting role', key)
            return result
        match = re.search(r'\bbest actor\b', key)
        if match:
            result = re.sub(r'\bbest actor\b', 'best performance by an actor', key)
            return result
        match = re.search(r'\bbest actress\b', key)
        if match:
            result = re.sub(r'\bbest actress\b', 'best performance by an actress', key)
            return result
