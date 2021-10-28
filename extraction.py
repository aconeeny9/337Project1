import util
from Host import Host
from Awards_temp import Awards

# please add any bad keywords here
blacklist_keywords = [
    ["blacklist",
     ["predict", "predicts", "predicted", "prediction", "predictions", "next year", "bet", "guess", "wish"]]
]

# please add any good keywords here
whitelist_keywords = [
    ["host", ["host", "hosts", "hosting", "hosted"]],
    ['best', ['Best']],
    ["win", ['win', 'wins', 'won']],
    ['go to', ['go to', 'goes to', 'went to']],
    ['nominate', ["nominate", "nominee"]]
]
host_scanner = Host()
awards_scanner = Awards()


def tweet_extraction(year):
    # load tweet from csv
    tweets = util.load_data('gg{}.json'.format(year))
    # iterate through all the tweets and extract information from them
    lent = len(tweets)
    for index, tweet in enumerate(tweets):
        # check if the tweet contain any bad keywords
        if util.keyword_matcher(blacklist_keywords, tweet)[0]:
            continue
        # check if the tweet contain any good keywords
        contain_keyword, match_list = util.keyword_matcher(whitelist_keywords, tweet)
        if contain_keyword:
            match_dic = util.merge_matches(match_list)
            host_scanner.scanner_dispatch(match_dic, tweet)
            awards_scanner.scanner_dispatch(match_dic, tweet)
    host_scanner.evaluate()
    awards_scanner.evaluate()
    print(host_scanner.to_string())
    util.write_json([host_scanner], 'gg2013.json')


def get_host():
    return host_scanner.host_name


def get_award():
    return awards_scanner.awards_list


if __name__ == '__main__':
    tweet_extraction(2013)
