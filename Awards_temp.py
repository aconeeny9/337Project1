import re
import util
import numpy as np


class Awards:
    def __init__(self):
        self.awards_dic = {}
        self.awards_list = []

    def scanner_dispatch(self, match_dic, tweet):
        win_match = False
        best_match = False
        goto_match = False
        for match_key in match_dic:
            if match_key == "best":
                best_match = True
            if match_key == "win":
                win_match = True
            if match_key == 'go to':
                goto_match = True
        if best_match:
            if win_match and best_match:
                self.__search_1(match_dic['best'], tweet)
            elif goto_match and best_match:
                self.__search_2(match_dic['go to'], tweet)
            else:
                self.__search_3(match_dic['best'], tweet)

    def __search_1(self, indexes, tweet):
        # wins
        pattern = "wins+\s+best+\s(.+?)\s+!"
        match_result = re.search(pattern, tweet.lower())
        if match_result:
            clean_tweet = re.sub('\'s', '', tweet)
            clean_tweet = re.sub(r'[^\w\s]', '', clean_tweet)
            split_tweet = clean_tweet.split()
            for index in indexes:
                start, end = index
                forward_search = util.new_search_forward(split_tweet, end)
                for candidate in forward_search:
                    if len(candidate.split()) > 3:
                        if candidate not in self.awards_dic:
                            self.awards_dic[candidate] = 1
                        else:
                            self.awards_dic[candidate] += 1

    def __search_2(self, indexes, tweet):
        # go to
        pattern = "best+\s(.+?)\s+goes to"
        match_result = re.search(pattern, tweet.lower())
        if match_result:
            match = match_result.group()
            clean_tweet = re.sub('\'s', '', match.lower())
            clean_tweet = re.sub(r'[^\w\s]', '', clean_tweet)
            split_tweet = clean_tweet.split()[:-2]
            candidate = ' '.join(split_tweet)
            if len(candidate.split()) > 3:
                if candidate not in self.awards_dic:
                    self.awards_dic[candidate] = 1
                else:
                    self.awards_dic[candidate] += 1


    def __search_3(self, indexes, tweet):
        # -
        '''pattern = "best\s+(.+?)\s+-+\s+(.+?)\s+-"
        match_result = re.search(pattern, tweet.lower())
        if match_result:
            match = match_result.group()
            clean_tweet = re.sub('\'s', '', match.lower())
            candidate = re.sub(r'[^\w\s]', '', clean_tweet)
            print(candidate)
            if len(candidate.split()) > 3:
                if candidate not in self.awards_dic:
                    self.awards_dic[candidate] = 1
                else:
                    self.awards_dic[candidate] += 1
            return'''

        pattern = "Best+\s(.+?)\s+: "
        match_result = re.search(pattern, tweet)
        if match_result:
            tweet = match_result.group()
            #print(tweet)
            #clean_tweet = re.sub('\'s', '', tweet)
            #clean_tweet = re.sub(r'[^\w\s]', '', clean_tweet)
            split_tweet = tweet.split()[:-2]
            for index in indexes:
                start, end = index
                forward_search = util.new_search_forward(split_tweet, end, inclusive=True)
                for candidate in forward_search:
                    candidate = candidate.strip(" .,-:")
                    if len(candidate.split()) > 3:
                        if candidate not in self.awards_dic:
                            self.awards_dic[candidate] = 1
                        else:
                            self.awards_dic[candidate] += 1
            return

    def evaluate(self):
        keys = []
        values = []
        for key in self.awards_dic:
            keys.append(key)
            values.append(self.awards_dic[key])
        if len(keys) == 0:
            return
        keys = np.array(keys)
        values = np.array(values)
        sorted_index = np.argsort(values)[::-1]
        keys = keys[sorted_index]
        values = values[sorted_index]
        value_list = []
        for index, key in enumerate(keys):
            self.awards_list.append(key)
            value_list.append(values[index])
            if index >= 50:
                break
        self.__merge(keys, values, value_list)
        value_list = np.array(value_list)
        sorted_index = np.argsort(value_list)[::-1]
        keys = np.array(self.awards_list)[sorted_index]
        values = value_list[sorted_index]
        self.awards_list = []
        for index, key in enumerate(keys):
            self.awards_list.append(key)
            print(key, values[index])
            #value_list.append(values[index])
            if index >= 25:
                break

    def __merge(self, keys, values, value_list):
        for index, name in enumerate(keys):
            for index1, name1 in enumerate(self.awards_list):
                if name != name1 and name in name1:
                    value_list[index1] += values[index]
