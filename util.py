import json
import re


def keyword_matcher(keywords, tweet):
    clean_tweet = re.sub('\'s', '', tweet)
    clean_tweet = re.sub(r'[^\w\s]', '', clean_tweet)
    matches = []
    for keyword in keywords:
        key_id = keyword[0]
        patterns = keyword[1]
        for pattern in patterns:
            if re.search(r"\b{}\b".format(pattern), clean_tweet):
                start, end = __find_index(pattern, clean_tweet)
                matches.append([key_id, start, end])
    if len(matches) > 0:
        found_pattern = True
    else:
        found_pattern = False
    return found_pattern, matches


def __find_index(keyword, tweet):
    split_keyword = keyword.split()
    if len(split_keyword) < 2:
        start = tweet.split().index(keyword)
        end = start
    else:
        start = tweet.split().index(split_keyword[0])
        end = tweet.split().index(split_keyword[-1])
    return start, end


def merge_matches(match_list):
    match_dic = {}
    for match in match_list:
        match_id = match[0]
        start, end = match[-2:]
        if match_id not in match_dic:
            match_dic[match_id] = [[start, end]]
        else:
            match_dic[match_id].append([start, end])
    return match_dic


def search_forward(data, starting_index, search_range):
    if starting_index == len(data) - 1:
        return []
    return convolution(data[starting_index + 1:], search_range)


def search_backward(data, starting_index, search_range):
    if starting_index == 0:
        return []
    return convolution(data[:starting_index], search_range)


def convolution(data, search_range):
    if search_range > len(data):
        search_range = len(data)
    result = []
    for i in range(1, search_range + 1):
        convolution_helper(i, data, result)
    return result


def convolution_helper(window_size, data, result):
    for i in range(len(data) - window_size + 1):
        result.append(' '.join(data[i:i + window_size]))


def new_search_forward(data, starting_index, inclusive = False):
    if starting_index == len(data) - 1:
        return []
    fragments = []
    for index in range(starting_index+1, len(data)):
        if inclusive:
            fragments.append(" ".join(data[starting_index:index + 1]))
        else:
            fragments.append(" ".join(data[starting_index + 1:index + 1]))
    return fragments


def new_search_backward(data, starting_index, inclusive = False):
    if starting_index == 0:
        return []
    fragments = []
    for index in range(1, starting_index+1):
        if inclusive:
            fragments.append(" ".join(data[starting_index - index:starting_index+1]))
        else:
            fragments.append(" ".join(data[starting_index - index:starting_index]))
    return fragments


def write_json(data_objects, year):
    host, awards, presenter, nominees, winner = data_objects
    json_data = {'Host':host.host_name}
    json_data['Extracted Awards'] = awards.awards_list
    for award_name in winner.winner:
        json_data[award_name] = {
            "Presenters": presenter.presenter[award_name],

            "Nominees": nominees.nominees[award_name],

            "Winner": winner.winner[award_name]
        }
    file_name = 'gg'+str(int(year))+"extraction.json"
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file)
