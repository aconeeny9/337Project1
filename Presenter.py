import util
import imdb_checker as imdb
import re
import numpy

class Presenter:
    def __init__(self):
        self.presenter = {}
        self.presenter_dic = {}
        self.presenter_collect = []

    def set_awards(self, award_list):
        self.awards_list = award_list
        for award_name in self.awards_list:
            self.presenter[award_name] = []
            self.presenter_dic[award_name] = {}

    def set_winners(self, winner_list):
        self.winner_dict = winner_list
    
    def scanner_dispatch(self, tweet):
        if 'present' in tweet.lower():
            self.__search_presenter(tweet)

    def __search_presenter(self, tweet):
        clean_tweet = re.sub('\'s', '', tweet)
        clean_tweet = re.sub(r'[^\w\s]', '', clean_tweet)
        split_string = clean_tweet.split()
        
        index = -1
        for ind, c in enumerate(split_string):
            if "present" in c.lower():
                index = ind
                break
        if index == -1:
            return

        search_backward = util.search_backward(split_string, index, 5)
        search_backward.extend(util.new_search_backward(split_string, index))
        search_forward = util.search_forward(split_string, index, 5)
        search_forward.extend(util.new_search_forward(split_string, index))
        search_backward.extend(search_forward)
        for candidate in search_backward:
            if imdb.is_imdb_person(candidate):
                self.presenter_collect.append([candidate, tweet])
    
    def __simplify_dict(self, dictionary):
        for person in dictionary:
            for x in dictionary:
                if x in person and x != person and dictionary[x] != -1 and dictionary[person] != -1:
                    dictionary[person] += dictionary[x]
                    dictionary[x] = -1
        return dictionary

    def __get_presenters(self, d):
        d = sorted(d.items(), key=lambda t: t[1])
        d.reverse()
        d = dict(d)
        d = self.__simplify_dict(d)
        d = sorted(d.items(), key=lambda t: t[1])
        d.reverse()
        
        d = [x for x in d if x[1] != -1 and " " in x[0]]

        if len(d) <= 0:
            return []
        one = d[0][0]
        if len(d) <= 1:
            return [one]
        two = d[1][0]

        if (numpy.floor(d[0][1] / 2) - 1) > d[1][1]:
            return [one]
        else:
            return [one, two]

    def evaluate(self):
        for candidate in self.presenter_collect:
            for i in self.winner_dict:
                winner = self.winner_dict[i].lower()
                if winner in candidate[1].lower() and candidate[0].lower() not in winner:
                    if candidate[0] in self.presenter_dic:
                        self.presenter_dic[candidate[0]] += winner
                    else:
                        self.presenter_dic[candidate[0]] = winner
            for award in self.awards_list:
                if award in candidate[1].lower() and candidate[0].lower() not in award and candidate[0].lower() not in self.winner_dict[award]:
                    if candidate[0] in self.presenter_dic:
                        self.presenter_dic[candidate[0]] += award
                    else:
                        self.presenter_dic[candidate[0]] = award

        for key in self.awards_list:
            options = {}
            for presenter in self.presenter_dic:
                if(key in self.presenter_dic[presenter]):
                    if presenter in options:
                        options[presenter] += self.presenter_dic[presenter].count(key)
                    else:
                        options[presenter] = self.presenter_dic[presenter].count(key)
                if(self.winner_dict[key].lower() in self.presenter_dic[presenter]):
                    if presenter in options:
                        options[presenter] += self.presenter_dic[presenter].count(self.winner_dict[key].lower())
                    else:
                        options[presenter] = self.presenter_dic[presenter].count(self.winner_dict[key].lower())
            self.presenter[key] = self.__get_presenters(options)