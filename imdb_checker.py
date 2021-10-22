import pickle

with open('imdb_data.pkl', 'rb') as data_file:
    imdb_data = pickle.load(data_file)
actor, actress, director, person, title = imdb_data


def is_imdb_actor(name):
    return name in actor


def is_imdb_actress(name):
    return name in actress


def is_imdb_director(name):
    return name in director

def is_imdb_person(name):
    return name in person


def is_imdb_title(name):
    return name in title