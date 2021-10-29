import imdb_checker
import re
import numpy as np
import util


class Winner:
    def __init__(self):
        self.winner = {}
        self.winner_dic = {}

    def set_awards(self, award_list):
        self.awards_list = award_list
        for award_name in self.awards_list:
            self.winner[award_name] = ''
            self.winner_dic[award_name] = {}





    def scanner_dispatch(self, match_dic, tweet):
        for match_key in match_dic:
            if match_key == "best":
                self.__search_best(match_dic['best'], tweet)

    '''win_match = False
        best_match = False
        winner_match = False
        goto_match = False
        for match_key in match_dic:
            if match_key == "best":
                best_match = True
            if match_key == 'win':
                win_match = True
            if match_key == 'winner':
                winner_match = True
            if match_key == 'go to':
                goto_match = True
        if win_match and best_match:
            self.__search_win(match_dic['win'], match_dic['best'], tweet)
        elif winner_match and best_match:
            self.__search_winner(match_dic['winner'], match_dic['best'], tweet)
        elif goto_match and best_match:
            self.__search_goto(match_dic['go to'], match_dic['best'], tweet)
        elif best_match:
            self.__search_best(match_dic['best'], tweet)
        # elif match_key == 'cecil':
        # self.__search_best(match_dic['cecile'], tweet)'''

    def __search_win(self, win_indexes, best_indexes, tweet):
        clean_tweet = re.sub(r'[^\w\s]', '', tweet.lower())
        pattern1 = "wins+\s+best+\s(.+?)\s"
        pattern2 = "wins+\s+the best+\s(.+?)\s"
        match_result1 = re.search(pattern1, clean_tweet)
        match_result2 = re.search(pattern2, clean_tweet)
        if match_result1 or match_result2:
            award_name = self.__name_picker(tweet)
            if award_name:
                print(tweet)
                start, end = win_indexes[0]
                clean_tweet = re.sub('\'s', '', tweet)
                clean_tweet = re.sub(r'[^\w\s]', '', clean_tweet)
                split_tweet = clean_tweet.split()
                candidates = util.search_backward(split_tweet, start, 10)
                for candidate in candidates:
                    if self.__suitable_candiate(award_name, candidate) and candidate.lower() not in award_name:
                        print(candidate.lower())
                        print(award_name)
                        print(candidate.lower() not in award_name)
                        print(candidate)
                        if candidate in self.winner_dic[award_name]:
                            self.winner_dic[award_name][candidate] += 1
                        else:
                            self.winner_dic[award_name][candidate] = 1

    def __search_winner(self, winner_indexes, best_indexes, tweet):
        pass

    def __search_goto(self, goto_indexes, best_index, tweet):
        pass

    def __search_best(self, indexes, tweet):
        award_name = self.__name_picker(tweet)
        if award_name:
            start, end = indexes[0]
            clean_tweet = re.sub(r"[^\w\s\-\\'\"\:]+", '', tweet)
            split_tweet = clean_tweet.split()
            forward = util.search_forward(split_tweet, start, 10)
            backward = util.search_backward(split_tweet, start, 10)
            candidates = forward+backward
            for candidate in candidates:
                if self.__suitable_candidate(award_name, candidate) and candidate.lower() not in award_name:
                    if candidate in self.winner_dic[award_name]:
                        self.winner_dic[award_name][candidate] += 1
                    else:
                        self.winner_dic[award_name][candidate] = 1
                elif self.__okay_candidate(award_name, candidate) and candidate.lower() not in award_name:
                    if candidate in self.winner_dic[award_name]:
                        self.winner_dic[award_name][candidate] += 0.1
                    else:
                        self.winner_dic[award_name][candidate] = 0.1

    def __suitable_candidate(self, award_name, candidate):
        if 'actor' in award_name:
            return imdb_checker.is_imdb_actor(candidate)
        elif 'actress' in award_name:
            return imdb_checker.is_imdb_actress(candidate)
        elif 'director' in award_name:
            return imdb_checker.is_imdb_director(candidate)
        else:
            return imdb_checker.is_imdb_title(candidate)

    def __okay_candidate(self, award_name, candidate):
        if 'actor' in award_name or 'actress' in award_name or 'director' in award_name:
            return imdb_checker.is_imdb_person(candidate)

    def __search_cecile(self, indexes, tweet):
        pass

    def __name_picker(self, tweet):
        for award_name in self.awards_list:
            if self.__name_matcher(award_name, tweet):
                return award_name
            else:
                match = re.search(r'\btelevision\b'.format(award_name),award_name.lower())
                if match:
                    award_name2 = re.sub(r'\btelevision\b', 'tv', award_name.lower())
                    if self.__name_matcher(award_name2, tweet):
                        return award_name
        return None

    def __name_matcher(self, award_name, tweet):
        award_name = re.sub(r'[^\w\s]', '', award_name.lower())
        clean_tweet = re.sub(r'[^\w\s]', '', tweet.lower())
        match = re.search(r'\b{}\b'.format(award_name),clean_tweet)
        if match:
            return True
        else:
            return False

    def __merge(self,candidates, values):
        for index, candidate in enumerate(candidates):
            if len(candidate.split())>1:
                for index1, candidate1 in enumerate(candidates):
                    if candidate1!=candidate and (re.search(r'\b{}\b'.format(candidate1), candidate) or re.search(r'\b{}\b'.format(candidate1.lower()), candidate)):
                        values[index] += values[index1]

    def evaluate(self):
        for key in self.winner_dic:
            candidates_dic = self.winner_dic[key]
            candidates = []
            values = []
            for candidate in candidates_dic:
                candidates.append(candidate)
                values.append(candidates_dic[candidate])
            self.__merge(candidates, values)
            candidates = np.array(candidates)
            values = np.array(values)
            sorted_index = np.argsort(values)[::-1]
            candidates = candidates[sorted_index]
            candidates = list(candidates)
            if len(candidates)>0:
                for candidate in candidates:
                    if not re.match(r'^[_\W]+$', candidate):
                        break
                self.winner[key] = candidate
            correct = {"best screenplay - motion picture":"django unchained",
                    "best director - motion picture": "ben affleck",
                    "best performance by an actress in a television series - comedy or musical":"lena dunham",
                    "best foreign language film":"amour",
                    "best performance by an actor in a supporting role in a motion picture":"christoph waltz",
                    "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television":"maggie smith",
                    "best motion picture - comedy or musical": "les miserables",
                    "best performance by an actress in a motion picture - comedy or musical": "jennifer lawrence",
                    "best mini-series or motion picture made for television":  "game change",
                    "best original score - motion picture":"life of pi",
                    "best performance by an actress in a television series - drama":"claire danes",
                    "best performance by an actress in a motion picture - drama": "jessica chastain",
                    "cecil b. demille award": "jodie foster",
                    "best performance by an actor in a motion picture - comedy or musical":"hugh jackman",
                    "best motion picture - drama": "argo",
                    "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television": "ed harris",
                    "best performance by an actress in a supporting role in a motion picture":  "anne hathaway",
                    "best television series - drama": "homeland",
                    "best performance by an actor in a mini-series or motion picture made for television": "kevin costner",
                    "best performance by an actress in a mini-series or motion picture made for television": "julianne moore",
                    "best animated feature film": "brave",
                    "best original song - motion picture": "skyfall",
                    "best performance by an actor in a motion picture - drama": "daniel day-lewis",
                    "best television series - comedy or musical": "girls",
                    "best performance by an actor in a television series - drama": "damian lewis",
                    "best performance by an actor in a television series - comedy or musical": "don cheadle"}
        for award_name in self.awards_list:
            c = correct[award_name]
            a = self.winner[award_name]
            if c.lower() != a.lower():
                print(award_name, c, a)
                print(self.winner_dic[award_name])



