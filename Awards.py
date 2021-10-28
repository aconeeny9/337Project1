import re
import util
import numpy as np
import imdb_checker as imdb
import helpers

class Awards:
    def __init__(self):
        self.awards_dic = {}
        self.awards_list = []
        self.all_nominated = {}

    def scanner_dispatch(self, match_dic, tweet):
        winnerKeywords = ["won", "wins"]
        filterKeywords = ["Globes", "Golden", "Golden Globes", "#GoldenGlobes", "RT:", "goldenglobes"]
        punctuation = ['\'', ',', ';', '"', ':', '!', '?', ')', '(', ']', '[', '}', '{', '#']
        replacements = [(" or ", "/"), ("Television", "TV"), (" at ", " ")]  # , ("in a ", " ")]
        for word in winnerKeywords:
            if word in tweet:
                string = tweet
                split_punc_string = string.split(". ")
                for split in split_punc_string:
                    if "Best" in split:
                        string = split
                        break
                split_punc_string = string.split("! ")
                for split in split_punc_string:
                    if "Best" in split:
                        string = split
                        break
                split_punc_string = string.split(" for ")
                for split in split_punc_string:
                    if "Best" in split:
                        string = split
                        break
                for rem in punctuation:
                    string = string.replace(rem, "")
                for rem in filterKeywords:
                    string = string.replace(rem, "")
                string = string.replace("'s", "")
                for replace in replacements:
                    string = string.replace(replace[0], replace[1])
                # elt = string

                split_string = string.split()
                index = -1
                for ind, c in enumerate(split_string):
                    if word in c:
                        index = ind
                        break
                # Search backward from keyword for actor/acress name
                search_backward = util.new_search_backward(split_string, index)
                #  Search forward from keyword for award name
                search_forward = util.new_search_forward(split_string, index)
                # if the fragment is an actor or actress, call helper to add frags to dict
                for frags in search_backward:
                    if "Actress" in string and imdb.is_imdb_actress(frags):
                        helpers.add_to_nominees(self.all_nominated, frags, search_forward)
                    elif "Actor" in string and imdb.is_imdb_actor(frags):
                        helpers.add_to_nominees(self.all_nominated, frags, search_forward)
                    elif imdb.is_imdb_title(frags) and "Actor" not in string and "Actress" not in string:
                        helpers.add_to_nominees(self.all_nominated, frags, search_forward)

    def evaluate(self):
        self.all_nominated = helpers.simplify_nominees(self.all_nominated)
        for item in self.all_nominated.items():
            self.awards_list.append(item[1])
