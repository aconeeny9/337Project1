import spacy
import numpy as np
import re
import util
import imdb_checker


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


class Surprise:
    def __init__(self):
        self.tweet = {}
        self.nlp = spacy.load("en_core_web_trf")
        self.candidate_dic = {}

    def set_winner(self, winner_dic):
        self.winner_dic = winner_dic
        for award_name in self.winner_dic:
            self.candidate_dic[award_name] = {}

    def scanner_dispatch(self, tweet):
        if tweet[:3].lower() == 'rt ':
            return
        keywords = ['what?', 'wtf?', "?!?!", "!?!?"]
        if any(k in tweet.lower() for k in keywords):
            doc = self.nlp(tweet)
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    p = ent.text
                    if p.lower() not in self.tweet:
                        self.tweet[p.lower()] = [tweet]
                    else:
                        self.tweet[p.lower()].append(tweet)

    def scanner_dispatch_1(self, match_dic, tweet):
        pattern = "\s+rt+\s"
        match = re.search(pattern, tweet.lower())
        if match or tweet.lower()[:3] == 'rt ':
            return
        for match_key in match_dic:
            self.__search_unexpected(tweet, match_key)

    def __search_unexpected(self, tweet, award_name):
        if 'best' in tweet.lower():
            return
        key_words = ['what?', 'wtf?', "?!?!", "!?!?", 'unexpect', 'imagine', 'not expect', 'should', 'better', 'think', 'thought', 'more', 'match',  'bet', 'want']
        if not any(k in tweet.lower() for k in key_words):
            return
        clean_tweet = re.sub(r"[^\w\s\-\\'\"\:]+", '', tweet)
        split_tweet = clean_tweet.split()
        forward = util.search_forward(split_tweet, 0, 10)
        for candidate in forward:
            if suitable_candidate(award_name, candidate) and candidate.lower() not in award_name:
                if candidate in self.candidate_dic[award_name]:
                    self.candidate_dic[award_name][candidate] += 1
                else:
                    self.candidate_dic[award_name][candidate] = 1
            elif okay_candidate(award_name, candidate) and candidate.lower() not in award_name:
                if candidate in self.candidate_dic[award_name]:
                    self.candidate_dic[award_name][candidate] += 0.1
                else:
                    self.candidate_dic[award_name][candidate] = 0.1

    def evaluate(self):
        length = []
        keys = []
        for key in self.tweet:
            keys.append(key)
            length.append(len(self.tweet[key]))
        length = np.array(length)
        keys = np.array(keys)
        sort_index = np.argsort(length)[::-1]
        length = length[sort_index]
        keys = keys[sort_index]
        tweets = self.tweet[keys[0]]
        print("The person that brings most surprise to the audience is {} !".format(keys[0]))
        print('Here are some tweets about {}:'.format(keys[0]))
        length = len(tweets)
        indexes = np.random.randint(length, size=3)
        for index in indexes:
            print(sorted(tweets, key=len, reverse=True)[index])
        big_struct = []
        for award_name in self.candidate_dic:
            keys = []
            values = []
            for key in self.candidate_dic[award_name]:
                keys.append(key)
                values.append(self.candidate_dic[award_name][key])
            if len(keys) < 1:
                continue
            keys, values = self.__merge(keys, values)
            sort_index = np.argsort(values)[::-1]
            keys = keys[sort_index]
            values = values[sort_index]
            structure = [award_name]
            for index, key in enumerate(keys):
                if key not in self.winner_dic[award_name]:
                    structure.append(key)
                    structure.append(values[index])
                    break
            big_struct.append(structure)
        big_struct = np.array(big_struct)
        sort_index = np.argsort(big_struct[:, -1])[::-1]
        big_struct = big_struct[sort_index]
        print('The most unexpected winner is {} for the {} award'.format(self.winner_dic[big_struct[0][0]], big_struct[0][0]))
        print("A lot of people believe {} would win this award instead".format(big_struct[0][1]))




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
