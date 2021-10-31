from textblob import TextBlob
import spacy
import re
import numpy as np
import imdb_checker


class RedCarpet:
    def __init__(self):
        self.best_dress = {}
        self.person = {}
        self.nlp = spacy.load("en_core_web_trf")
        self.brand = {"Louis": "Louis Vuitton", 'Gucci': 'Gucci', 'Balenciaga': 'Balenciaga', 'Dior': 'Christian Dior',
                      'Prada': 'Prada',
                      'Ferragamo': 'Salvatore Ferragamo', 'Fendi': 'Fendi', 'YSL': 'Yves Saint Laurent',
                      'Saint Laurent': 'Yves Saint Laurent',
                      'Givenchy': 'Givenchy', 'McQueen': 'Alexander McQueen', 'Armani': 'Giorgio Armani',
                      'Tom Ford': 'Tom Ford',
                      'Burberry': 'Burberry', 'CK': 'Calvin Klein', 'Ralph Lauren': 'Ralph Lauren',
                      'Valentino': 'Valentino',
                      'Zegna': 'Ermenegildo Zegna', 'Hugo Boss': 'Hugo Boss', 'Hermes': 'Hermes',
                      'Dolce & Gabbana': 'Dolce & Gabbana',
                      'Dolce': 'Dolce & Gabbana', 'Gabbana': 'Dolce & Gabbana', 'Chanel': 'Chanel',
                      'Roberto Cavalli': 'Roberto Cavalli',
                      'Max Azria Atelier': 'Max Azria Atelier', 'Vera Wang': 'Vera Wang',
                      'Donna Karan Atelier': 'Donna Karan Atelier', 'Erdem': 'Erdem',
                      'Carolina Herrera': 'Carolina Herrera', 'Miu Miu': 'Miu Miu', 'Versace': 'Versace'}

    def scanner_dispatch(self, match_dic, tweet):
        for match_key in match_dic:
            self.__analyze_tweet(tweet)

    def __analyze_tweet(self, tweet):
        blob = TextBlob(tweet)
        structure = [0, 0, 0, '', '']
        indicate = False
        for sent in blob.sentences:
            score = sent.sentiment.polarity
            if score != 0:
                indicate = True
                structure[0] += score
                if score > 0:
                    structure[1] += 1
                else:
                    structure[2] += 1
        if indicate:
            doc = self.nlp(tweet)
            people = []
            brand = ''
            link = ''
            for ent in doc.ents:
                bad_key = ['red carpet', 'Red Carpet', 'red carpet'.upper(), 'redcarpet', 'RedCarpet', 'REDCARPET']
                if ent.label_ == 'PERSON' and not any([k in ent.text for k in bad_key]) and imdb_checker.is_imdb_person(ent.text):
                    p = ent.text
                    people.append(p)
                if ent.label_ == 'ORG':
                    if re.sub(r'[^\w\s]', '', ent.text) in self.brand:
                        brand = self.brand[re.sub(r'[^\w\s]', '', ent.text)]
            if len(people) < 1:
                return
            for frag in tweet.split():
                if 'http://t.co/' in frag:
                    link = frag
            structure[3] = brand
            structure[4] = link
            for p in people:
                p = re.sub('\'s', '', p)
                if p.lower() not in self.best_dress:
                    self.best_dress[p.lower()] = structure
                else:
                    self.best_dress[p.lower()][0] += structure[0]
                    self.best_dress[p.lower()][1] += structure[1]
                    self.best_dress[p.lower()][2] += structure[2]
                    if len(structure[3])>0:
                        self.best_dress[p.lower()][3] = structure[3]
                    if len(structure[4]) > 0:
                        self.best_dress[p.lower()][4] = structure[4]

    def evaluate(self):
        names = []
        total = []
        avg = []
        sum = []
        diff = []
        pos = []
        neg = []
        outfits = []
        links = []
        for key in self.best_dress:
            names.append(key)
            t, p, n, b, l = self.best_dress[key]
            total.append(t)
            pos.append(p)
            neg.append(n)
            outfits.append(b)
            links.append(l)
            avg.append(t / (p + n))
            sum.append(p + n)
            diff.append(abs(p - n))
        names = np.array(names)
        total = np.array(total)
        avg = np.array(avg)
        sum = np.array(sum)
        diff = np.array(diff)
        pos = np.array(pos)
        neg = np.array(neg)
        outfits = np.array(outfits)
        links = np.array(links)
        sort_index = np.argsort(total)[::-1]
        sum = sum[sort_index]
        diff = diff[sort_index]
        avg = avg[sort_index]
        s = "{} is people's favorite celebrity on the red carpet\n".format(names[sort_index][0])
        outfit = outfits[sort_index][0]
        if len(outfit) > 0:
            o = "Outfit provided by: {}\n".format(outfit)
        else:
            o = ''
        link = links[sort_index][0]
        if len(link) > 0:
            l = 'Image Link: {}'.format(link)
        else:
            l = ''
        print(s + ' ' + o + ' ' + l)
        sort_index = np.argsort(total)
        sum = sum[sort_index]
        diff = diff[sort_index]
        avg = avg[sort_index]
        total = total[sort_index]
        if avg[0]<0.2:
            s = "{} is people's least favorite celebrity on the red carpet\n".format(names[sort_index][0])
            outfit = outfits[sort_index][0]
            if len(outfit) > 0:
                o = "Outfit provided by: {}\n".format(outfit)
            else:
                o = ''
            link = links[sort_index][0]
            if len(link) > 0:
                l = 'Image Link: {}'.format(link)
            else:
                l = ''
            print(s + ' ' + o + ' ' + l)

        sort_index = np.argsort(sum)[::-1]
        sum = sum[sort_index]
        diff = diff[sort_index]
        indicate = False
        for index, s in enumerate(sum):
            if diff[index]<0.2:
                indicate = True
                break
            if index>sum.shape[0]*0.2:
                break
        if indicate:
            s = "{} is the most controversial celebrity on the red carpet\n".format(names[sort_index][index])
            outfit = outfits[sort_index][index]
            if len(outfit) > 0:
                o = "Outfit provided by: {}\n".format(outfit)
            else:
                o = ''
            link = links[sort_index][index]
            if len(link) > 0:
                l = 'Image Link: {}'.format(link)
            else:
                l = ''
            print(s + ' ' + o + ' ' + l)