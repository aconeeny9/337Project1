# Contains helpers for  nominees

# Function takes a name of someone nominated and a list of sentence fragments
# It builds up a large dictionary of all fragments related to the name to build a weighting system
# To extract the award name from
def add_to_nominees(all_nominated, name, fragments):
    if len(name.split()) == 1:
        for nominated in all_nominated:
            if name in nominated:
                name = nominated
                break
    if name in all_nominated:
        for frag in fragments:
            if frag != '' and frag.split()[0] == "Best":
                if frag in all_nominated[name]:
                    all_nominated[name][frag] += 1
                else:
                    all_nominated[name][frag] = 1
    else:
        val = {}
        for frag in fragments:
            if frag != '' and frag.split()[0] == "Best":
                val[frag] = 1
        all_nominated[name] = val

# Passed a dictionary of the form {key: {nested_key: value, nested_key: value}, ...}
# Flattens the dict to {key: maxOfNestedDict, ...}
def extract_highest(nested_dict):
    flat_dict = {}
    for nest in nested_dict.items():
        item = nest[1]
        sorted_frags = dict(sorted(item.items(), key=lambda item: item[1], reverse = True)).keys()
        award = ""
        for ind, key in enumerate(list(sorted_frags)):
            award = key
            break
        if award != '':
            flat_dict[nest[0]] = award
    return flat_dict

def award_name_search(data):
    best_split = data.split("Best")[1]
    rest_split = best_split.split()
    award_name = "Best "
    for word in rest_split:
        if word[0].isupper():
            award_name = award_name + word + " "
    return award_name

def compress_duplicates(this_dict):
    remove_list = []
    for ind, key in enumerate(list(this_dict.keys())):
        if len(key.split()) == 1:
            for i, second_key in enumerate(list(this_dict.keys())):
                if key in second_key and i != ind:
                    add_to_nominees(this_dict, second_key, list(this_dict[key].keys()))
                    if key not in remove_list:
                        remove_list.append(key)
    
    for item in remove_list:
        this_dict.pop(item)
    
    return this_dict

# Compresses the top elements in a dictionary and returns the dictionary
def compress_best(aDictionary):
    keys_dict = dict(sorted(aDictionary.items(), key=lambda item: item[1], reverse = True)).keys()
    keys = list(keys_dict)
    string = ""
    val = 0
    stop_ind = 0
    for ind, i in enumerate(keys):
        if ind < len(keys) - 1 and i in keys[ind + 1]:
            string = keys[ind+1]
            if ind == 0:
                val = aDictionary[string] + aDictionary[i]
            else:
                val += aDictionary[string]
            stop_ind = ind+1
        elif ind < len(keys) - 1 and keys[ind+1] in i:
            string = i
            if ind == 0:
                val = aDictionary[keys[ind+1]] + aDictionary[i]
            else:
                val += aDictionary[string]
            stop_ind = ind+2
        else:
            break
    new_dict = {string:val}
    for ind, i in enumerate(keys):
        if ind > stop_ind:
            new_dict[i] = aDictionary[i]

    return new_dict


def simplify_nominees(nominated):
    compressed_nominees = {}
    for nominated in nominated.items():
        item = compress_best(nominated[1])
        sorted_vals = dict(sorted(item.items(), key=lambda item: item[1], reverse = True))
        compressed_nominees[nominated[0]] = item
    compressed_nominees = compress_duplicates(compressed_nominees)
    wins = extract_highest(compressed_nominees)
    return wins