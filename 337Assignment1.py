import sys
import json

stream = open('gg2013.json')
data = json.load(stream)

host = {}
awardNames = {}
presenters = {}
nominees = {}
winners = {}

hostKeywords = ["host"]
awardKeywords = ["best"]
presenterKeywords = ["present"]
nomineeKeywords = ["nominate", "nominee"]
winnerKeywords = ["won", "wins", "winner"]

badKeywords = ["predict", "think", "thought", "bet", "guess", "wish", "knew", "know"]

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
                for each in string.split():
                    if each[0].isupper():
                        if each in host:
                            host[each] += 1
                        else:
                            host[each] = 1
        """ for word in awardKeywords:
            if word in tweet['text']:
                awardNames.append(tweet['text'])
        for word in presenterKeywords:
            if word in tweet['text']:
                presenters.append(tweet['text'])
        for word in nomineeKeywords:
            if word in tweet['text']:
                nominees.append(tweet['text'])
        for word in winnerKeywords:
            if word in tweet['text']:
                winners.append(tweet['text']) """
print(dict(sorted(host.items(), key=lambda item: item[1], reverse = True)))
'''for i in range(20):
    print(host[i])
for i in range(20):
    print(awardNames[i])
for i in range(20):
    print(presenters[i])'''