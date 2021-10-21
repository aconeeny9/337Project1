import sys
import json
import util

stream = open('gg2013.json')
data = json.load(stream)

host = {}
awardNames = {}
presenters = {}
nominees = {}
winners = {}

hostKeywords = ["host"]
awardKeywords = ["Best"]
presenterKeywords = ["present"]
nomineeKeywords = ["nominate", "nominee"]
winnerKeywords = ["won", "wins", "winner"]

badKeywords = ["predict", "think", "thought", "bet", "guess", "wish", "knew", "know", "RT", "should"]
filterKeywords = ["Globes", "Golden", "Golden Globes"]

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
                """for each in string.split():
                    if each[0].isupper():
                        if each in host:
                            host[each] += 1
                        else:
                            host[each] = 1"""
        for word in awardKeywords:
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
                        if i in awardNames and i[0].isupper():
                            awardNames[i] += 1
                        elif i[0].isupper():
                            awardNames[i] = 1
                words = util.new_search_forward(string, index)
                for i in words:
                    if i not in filterKeywords:
                        if i in awardNames and i[0].isupper():
                            awardNames[i] += 1
                        elif i[0].isupper():
                            awardNames[i] = 1
                """for each in string.split():
                    if each[0].isupper():
                        if each in host:
                            host[each] += 1
                        else:
                            host[each] = 1"""
        """for word in presenterKeywords:
            if word in tweet['text']:
                presenters.append(tweet['text'])
        for word in nomineeKeywords:
            if word in tweet['text']:
                nominees.append(tweet['text'])
        for word in winnerKeywords:
            if word in tweet['text']:
                winners.append(tweet['text']) """

def compress_best_of_dict(aDictionary):
    keys = list(dict(sorted(aDictionary.items(), key=lambda item: item[1], reverse = True)).keys())
    hosts = ""
    for ind, i in enumerate(keys):
        if i in keys[ind + 1]:
            hosts = keys[ind+1]
        else:
            break
    print(hosts)

compress_best_of_dict(host)

'''print(i)
if ind >= 20:
    break'''
