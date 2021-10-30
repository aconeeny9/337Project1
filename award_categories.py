
class Awards():
    def __init__(self):
        self.television_keywords = ['television', 'series', 'mini-series']
        #self.movie_keywords = [['motion picture'], ['television', 'series', 'mini-series']]
        self.person_keywords = ['performance', 'actor', 'actress', 'director', 'cecil']
        self.award_types = {
            'cecil b. demille award': ['person', '', ['cecil', 'demille']], 
            'best motion picture - drama': ['film', 'theater', ['drama']],
            'best performance by an actress in a motion picture - drama': ['person', 'theater', ['drama']],
            'best performance by an actor in a motion picture - drama': ['person', 'theater',['drama']], 
            'best motion picture - comedy or musical': ['film', 'theater', ['comedy/musical']], 
            'best performance by an actress in a motion picture - comedy or musical': ['person', 'theater',['comedy/musical']], 
            'best performance by an actor in a motion picture - comedy or musical': ['person', 'theater',['comedy/musical']], 
            'best animated feature film': ['film', 'theater',['animated','film']], 
            'best foreign language film': ['film', 'theater',['foreign','film']], 
            'best performance by an actress in a supporting role in a motion picture': ['person', 'theater',['actress','supporting']], 
            'best performance by an actor in a supporting role in a motion picture': ['person', 'theater',['actor','supporting']], 
            'best director - motion picture': ['person', 'theater',['best director']], 
            'best screenplay - motion picture': ['person', 'theater',['best screenplay']], 
            'best original score - motion picture': ['film', 'theater',['original score']], 
            'best original song - motion picture': ['film', 'theater',['original song']], 
            'best television series - drama': ['series', 'television',['television','series','drama']], 
            'best performance by an actress in a television series - drama': ['person', 'television',['actress','television','drama']], 
            'best performance by an actor in a television series - drama': ['person', 'television',['actor','television','drama']], 
            'best television series - comedy or musical': ['series', 'television',['series','comedy/musical']], 
            'best performance by an actress in a television series - comedy or musical': ['person', 'television',['actress','television','series','comedy/musical']], 
            'best performance by an actor in a television series - comedy or musical': ['person', 'television',['actor','television','series','comedy/musical']], 
            'best mini-series or motion picture made for television': ['film', 'television',['motion picture','television']], 
            'best performance by an actress in a mini-series or motion picture made for television': ['person', 'television',['actress','motion picture','television']], 
            'best performance by an actor in a mini-series or motion picture made for television': ['person', 'television',['actor','motion picture','television']], 
            'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': ['person', 'television',['actress','supporting','television']], 
            'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': ['person', 'television',['actor','supporting','television']]
        }

    def is_valid_award(self, award, tweet):
        for words in self.award_types[award][2]:
            if words not in tweet.lower():
                return False
        if self.award_types[award][0] is 'person':
            person = False
            for word in self.person_keywords:
                if word in tweet.lower():
                    person = True
            if not person:
                return False
            
            television = False
            for word in self.television_keywords:
                if word in tweet.lower():
                    television = True
            if self.award_types[award][1] is 'television':
                return television
            else:
                return not television
            return television
        
        else:
            person = False
            for word in self.person_keywords:
                if word in tweet.lower():
                    person = True
            if person:
                return False
            
            television = False
            for word in self.television_keywords:
                if word in tweet.lower():
                    television = True
            if self.award_types[award][1] is 'television':
                return television
            else:
                return not television
            return television