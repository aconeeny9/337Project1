import util
import re
import numpy as np
import imdb_checker


class Host:
    def __init__(self):
        self.host_name = []
        self.host_dic = {}

    def scanner_dispatch(self, match_dic, tweet):
        for match_key in match_dic:
            if match_key == "host":
                self.__search_host(match_dic[match_key], tweet)

    def __search_host(self, indexes, tweet):
        clean_tweet = re.sub('\'s', '', tweet)
        clean_tweet = re.sub(r'[^\w\s]', '', clean_tweet)
        split_tweet = clean_tweet.split()
        for index in indexes:
            start, end = index
            forward_search = util.search_forward(split_tweet, end, 4)
            backward_search = util.search_backward(split_tweet, start, 4)
            candidate_list = forward_search + backward_search
            for candidate in candidate_list:
                if candidate not in self.host_dic:
                    self.host_dic[candidate] = 1
                else:
                    self.host_dic[candidate] += 1

    def evaluate(self):
        keys = []
        values = []
        for key in self.host_dic:
            keys.append(key)
            values.append(self.host_dic[key])
        if len(keys) == 0:
            return
        keys = np.array(keys)
        values = np.array(values)
        sorted_index = np.argsort(values)[::-1]
        keys = keys[sorted_index]
        values = values[sorted_index]
        person = []
        person_values = []
        for index, key in enumerate(keys):
            if imdb_checker.is_imdb_person(key):
                person.append(key)
                person_values.append(values[index])
        if len(person) == 0:
            return
        for index, p in enumerate(person):
            person_values[index] += self.__merge_count(p)
        person = np.array(person)
        person_values = np.array(person_values)
        sorted_index = np.argsort(person_values)[::-1]
        person = person[sorted_index]
        person_values = person_values[sorted_index]
        person_values = person_values.tolist()
        if len(person_values)<=1:
            self.host_name = person.tolist()
            return
        for i in range(1, len(person_values)):
            count = float(person_values[i])
            prev_count = float(person_values[i - 1])
            if (prev_count - count) / prev_count > 0.3:
                break
        self.host_name = person[:i].tolist()

    def __merge_count(self, name):
        words = name.split()
        if len(words) < 2:
            return 0
        first_name = words[0]
        last_name = words[-1]
        extra_count = 0
        if len(first_name) >= 3 and first_name in self.host_dic:
            extra_count += self.host_dic[first_name]
        if len(last_name) >= 3 and last_name in self.host_dic:
            extra_count += self.host_dic[last_name]
        return extra_count

    def to_string(self):
        return "Host:{}".format(', '.join(self.host_name))

    def to_json(self, json_dic):
        if len(self.host_name) > 1:
            json_dic['Hosts'] = self.host_name
        else:
            json_dic['Host'] = self.host_name
