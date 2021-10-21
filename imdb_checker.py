import pickle

with open('imdb_data.pkl', 'rb') as data_file:
    imdb_data = pickle.load(data_file)
actor_dic, actress_dic, director_dic, title_dic = imdb_data


def is_imdb_actor(name):
    char = name.lower()[0]
    return name in actor_dic[char]


def is_imdb_actress(name):
    char = name.lower()[0]
    return name in actress_dic[char]


def is_imdb_director(name):
    char = name.lower()[0]
    return name in director_dic[char]


def is_imdb_title(name):
    char = name.lower()[0]
    return name in title_dic[char]
