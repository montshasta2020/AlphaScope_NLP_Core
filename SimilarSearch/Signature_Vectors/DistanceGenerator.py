import pandas as pd
from collections import Counter
import re
import math
from sklearn.feature_extraction import stop_words

dsi_stop_words = ['the', 'blog', 'i', 'in', 'new', 'use', 'a', 'how', 'it', 'like', 'need', 'sign', 'for', 
                  'rss', 'videos', 'view', 'using', 'interview', 'follow', 'read', 'make', 'video',
                  'post', 'comment', 'comments', 'subscribe', 'things', 'just', 'add', 'wise', 'know', 'upcoming', 
                  'people', 'practitioner', 'used', 'developers', 'events', 'companies', 'better', 'terms', 'time',
                  'customer', 'conference']

class DistanceGenerator (object):
    def __init__(self, df):
        self.df = df
    
    def calculate_distance (self, v1, v2):
        #print type(v1), type(v2)        
        if type(v1) == dict and type(v2) == dict:
            vec1 = v1
            vec2 = v2
        else:
            vec1 = eval(v1)
            vec2 = eval(v2)

        #print type(vec1), type(vec2)
        #print vec2.keys()
        #print vec1.keys()
        intersection = set(vec1.keys()) & set(vec2.keys())
        #print intersection
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator
    
    def get_max_distances_idx(self, vec):
        self.df['check_distances'] =  self.df.signature.map(lambda x: self.calculate_distance(vec, x))
        dist = self.df['check_distances'].values.argsort()[::-1]
        return dist
    
    def dsi_title_letters_removal(self, x):
        s = re.sub('[^a-zA-Z]+', '', x)
        if(len(s) > 0):
            s = s.strip().lower()
            if s not in stop_words.ENGLISH_STOP_WORDS and s not in dsi_stop_words:
                return s
            else:
                return None
        return None

    def calculate_signature(self, docs):
        if len(docs) == 1:
            words = docs.split()
            flatten = [dsi_title_letters_removal(item) for item in words \
                       if dsi_title_letters_removal(item) != None]

        else:
            docs_split = [item.split() for item in docs]
            flatten = [self.dsi_title_letters_removal(item) for sublist in docs_split for item in sublist \
                       if self.dsi_title_letters_removal(item) != None]

        count = Counter(flatten)
        top_50 = count.most_common(50)
        words, cnt = zip(*top_50)
        tot = sum(cnt)
        fq = [float(i)*1.0/tot for i in cnt]
        sign = dict(zip(words, fq))
        return sign   
    
    def get_clustering_per_query(self, s, threshold):
        print 'coming ---', s, len(self.df)
        words = s.lower().split()
        dsj_dict = dict()
        fq = [1.0/len(words) for item in words]
        init_sign = dict(zip(words, fq))
        #self.df.info()
        self.df['calculate_sim'] =  self.df.signature.map(lambda x: self.calculate_distance(init_sign, x))

        tmp = self.df[self.df['calculate_sim'] > threshold]
        return tmp

