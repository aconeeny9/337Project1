import sys
import json
import util
import imdb_checker as imdb
import helpers
from award_categories import Awards

punctuation = ['\'',',',';','"',':','!','?',')','(',']','[','}','{','#']
zero_score = [' by ', ' an ', ' in ', ' a ', ' - ', ' made for ', ' or ',' mini-series ','  performance ']#, ' for ', 'mini-series ',' performance ', ' made ', ' role ']# ' motion ', ' mini-series ', ' performance ']
replacements = [("TV", "Television"), ("Good luck", "good luck"), ("C.K.", "CK"), (" or ", "/")]#s, ("motion picture", "movie")]
filterKeywords = ["Globes", "Golden", "Golden Globes", "#GoldenGlobes", "RT:", "goldenglobes", "Globe", "GG", "good luck", "congrats", "congratulations","Congratulations"]

categories = Awards()

class Nominees():
    def __init__(self):
        self.nominees = {}

    # Takes data as raw tweet data & awards as the hardcoded list of strings
    # Scores each tweet as containing a number of keywords per award, added to dictionary of award_nominees
    def get_nominees(self, data, awards):
        nominees_by_award = self.create_award_dict(awards)
        for whole_tweet in data:
            tweet = whole_tweet['text']
            best_score = 0
            best_award = ''
            nominated = ''
            for words in replacements:
                tweet = tweet.replace(words[0],words[1])
            for award in awards:
                if categories.is_valid_award(award, tweet):
                    score = 0
                    award_for_scoring = award
                    for item in zero_score:
                        award_for_scoring = award_for_scoring.replace(item, " ")
                    parsed_award = award_for_scoring.split()

                    for frag in parsed_award:
                        if frag in tweet.lower():
                            score += 1
                    score = score/len(parsed_award)
                    if categories.award_types[award][0]=='person' or score > .75:
                        for filter_word in filterKeywords:
                            tweet = tweet.replace(filter_word, "")
                        nominee = self.extract_nominee(tweet, award)
                        if nominee != '' and score > best_score:
                            best_score = score
                            best_award = award
                            nominated = nominee
            if nominated != '':
                if nominated in nominees_by_award[best_award]:
                    nominees_by_award[best_award][nominated] += best_score
                else:
                    nominees_by_award[best_award][nominated] = best_score
        self.nominees = self.get_raw_nominees(self.filter(nominees_by_award),awards)
        #self.nominees = nominees_by_award
        print(json.dumps(self.nominees, indent=4))


    def get_raw_nominees(self, aDict, awards):
        new_dict = self.create_award_dict(awards)
        for award in aDict.keys():
            nominee_list = []
            for nominee in aDict[award].items():
                nominee_list.append(nominee[0])
            new_dict[award] = nominee_list
        return new_dict


    # Takes a tweet and the award we are mapping the nominee in the tweet to
    # Return the nominee, else return ""
    def extract_nominee(self, tweet, award):
        split_punc_string = tweet.split(". ")
        for split in split_punc_string:
            if "Best" in split:
                tweet = split
                break
        split_punc_string = tweet.split("! ")
        for split in split_punc_string:
            if "Best" in split:
                tweet = split
                break
        for rem in punctuation:
            tweet = tweet.replace(rem, "")
        parsed_tweet = tweet.split()
        capitalized_elements = []
        for ind, word in enumerate(parsed_tweet):
            if word[0].isupper() and word.lower() not in award:
                capitalized_elements.append(word)
        nominee = ""
        for word in capitalized_elements:
            possible_nominee_frags = util.new_search_forward(capitalized_elements, capitalized_elements.index(word))
            # if the fragment is an actor or actress, call helper to add frags to dict
            #nominee = ""
            for fragment in possible_nominee_frags:
                    if "actress" in award and "actress" in tweet.lower() and imdb.is_imdb_actress(fragment):
                        if len(fragment.split()) > 1:
                            nominee = fragment
                        #return fragment
                    elif "actor" in award and "actor" in tweet.lower() and imdb.is_imdb_actor(fragment):
                        if len(fragment.split()) > 1:
                            nominee = fragment
                        #return fragment
                    elif "director" in award and "director" in tweet.lower() and imdb.is_imdb_director(fragment):
                        if len(fragment.split()) > 1:
                            nominee = fragment
                    elif imdb.is_imdb_title(fragment) and "actor" not in award and "actress" not in award and "director" not in award:
                        if fragment not in nominee:
                            nominee = fragment
                        #return fragment
                    elif nominee != "":
                        if nominee not in fragment:
                            return nominee
                    #else:
                        #break
        return nominee


    def create_award_dict(self, awards):
        new_dict = {}
        for award in awards:
            new_dict[award] = {}
        return new_dict


    def filter(self, aDict):
        new_dict = {}
        for item in aDict.items():
            nest_dict = {}
            for nested_item in item[1].items():
                if categories.award_types[item[0]][0]=='person' or nested_item[1] > 1:
                    nest_dict[nested_item[0]] = nested_item[1]
            new_dict[item[0]] = nest_dict
        return new_dict

    def evaluate(self, data, awards):
        self.get_nominees(data, awards)



