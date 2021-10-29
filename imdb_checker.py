import pickle


def load_dataset(year):
    with open('{}.pkl'.format(year), 'rb') as data_file:
        imdb_data = pickle.load(data_file)
    global person, actor, actress, director, title
    person, actor, actress, director, title = imdb_data
    global person2, actor2, actress2, director2, title2
    if year != 2010:
        year = year - 1
        with open('{}.pkl'.format(year), 'rb') as data_file:
            imdb_data2 = pickle.load(data_file)
        person2, actor2, actress2, director2, title2 = imdb_data2
    else:
        person2 = None
        actor2 = None
        actress2 = None
        director2 = None
        title2 = None


def is_imdb_actor(name):
    if name in actor or name in actor2:
        return True
    else:
        return False


def is_imdb_actress(name):
    if name in actress or name in actress2:
        return True
    else:
        return False


def is_imdb_director(name):
    if name in director or name in director2:
        return True
    else:
        return False


def is_imdb_person(name):
    return name in person


def is_imdb_title(name):
    if name in title or name in title2:
        return True
    else:
        return False
