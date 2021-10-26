import sys
import json
import util
import imdb_checker as imdb
import helpers

stream = open('gg2013.json')
data = json.load(stream)
#print(type(data))

host = {}
awardNames = {}
presenters = {}
nominees = {}
winners = {}
winner_award = []
awards = {}
award_winners = []
all_nominated = {}

hostKeywords = ["host"]
awardKeywords = ["Best"]
presenterKeywords = ["present"]
nomineeKeywords = ["nominate", "nominee"]
#winnerKeywords = ["won", "wins", "winner"]
winnerKeywords = ["won", "wins"]

badKeywords = ["predict", "think", "thought", "bet", "guess", "wish", "knew", "know", "should"]
filterKeywords = ["Globes", "Golden", "Golden Globes", "#GoldenGlobes", "RT:", "goldenglobes"]
punctuation = ['\'',',',';','"',':','!','?',')','(',']','[','}','{','#']
replacements = [(" or ", "/"), ("Television","TV"),(" at "," "), ("in a ", " ")]

for tweet in data:
    goodTweet = True
    for word in badKeywords:
        if word in tweet['text']:
            goodTweet = False
    if goodTweet == True:
        for word in hostKeywords:
            if word in tweet['text']:
                string = tweet['text'].strip('.,;":!?)(][}{')
                string = string.replace("'s", "")
                string = string.split()
                index = -1
                for ind, c in enumerate(string):
                    if word in c:
                        index = ind
                        break
                words = util.new_search_backward(string, index)
                for i in words:
                    if i not in filterKeywords:
                        if i in host and i[0].isupper():
                            host[i] += 1
                        elif i[0].isupper():
                            host[i] = 1
                words = util.new_search_forward(string, index)
                for i in words:
                    if i not in filterKeywords:
                        if i in host and i[0].isupper():
                            host[i] += 1
                        elif i[0].isupper():
                            host[i] = 1
        # Look through tweets for winner keywords "wins", "won"
        for word in winnerKeywords:
            if word in tweet['text']:
                string = tweet['text']
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
                    string = string.replace(replace[0],replace[1])
                #elt = string
                
                
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
                        helpers.add_to_nominees(all_nominated, frags, search_forward)
                    elif "Actor" in string and imdb.is_imdb_actor(frags):
                        helpers.add_to_nominees(all_nominated, frags, search_forward)
                    elif imdb.is_imdb_title(frags) and "Actor" not in string and "Actress" not in string:
                        helpers.add_to_nominees(all_nominated, frags, search_forward)
        
all_nominated = helpers.simplify_nominees(all_nominated)

for item in all_nominated.items():
    print(item)


def compress_best_of_dict(aDictionary):
    keys = list(dict(sorted(aDictionary.items(), key=lambda item: item[1], reverse = True)).keys())
    hosts = ""
    for ind, i in enumerate(keys):
        if i in keys[ind + 1]:
            hosts = keys[ind+1]
        else:
            break
    print(hosts)

#compress_best_of_dict(host)



stream.close()