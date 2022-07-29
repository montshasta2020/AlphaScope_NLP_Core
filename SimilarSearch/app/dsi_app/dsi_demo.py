#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, session

import cPickle as pickle
import pandas as pd
import numpy as np
from DistanceGenerator import DistanceGenerator 
from time import time
from gensim.models import Word2Vec, KeyedVectors

import math
#from utilities import get_cars_names'

app = Flask(__name__)
app.secret_key = 'not a secret'

num = 5

#with open('pkl/lsi_dictionary.pkl') as f:
#    dictionary = pickle.load(f)

global more_start
global more_ret
global more_title
global curr_idx
global aG
global df
global model

df = pd.read_csv("data/dsi_web_slim_v2-3.csv")
model = KeyedVectors.load_word2vec_format('data/dsi_model_format_v3.bin')

more_start = 0
more_ret = None
more_title = None
curr_idx = np.zeros(5)

def deserialize(x):
    #print x
    ret = []
    s = x.strip('[]')
    vals = s.split(',')
    cnt = 0
    for val in vals:
        #print cnt, val
        #print '-----'
        cnt += 1
        ret.append(float(val))
    return np.asarray(ret)

df['w2v_centroid'] = df.w2v_centroid_s.map(lambda x: deserialize(x))

def get_cosine2(vec1, vec2):
    
    sum1 = np.sum([vec1**2])
    sum2 = np.sum([vec2**2])
    numerator = np.sum([a*b for a,b in zip(vec1,vec2)])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

# home page
@app.route('/')
def index():
    global more_start
    global more_ret
    global more_title
    global curr_idx

    more_title = None
    more_start = 0
    
    return render_template('index.html')

@app.route('/', methods=['POST'])
def input_form_post():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df
        
    text = None
    
    k = -1
    if request.method == 'POST':
        if 'query_1' in  request.form:
            k = -2
            text = request.form['query_input']
            #print 'get input-----', text
        elif 'query_0' in  request.form:
            more_start += 5  
            #print more_start, len(more_ret)
        elif 'similar_0' in request.form:
            k = 0
        elif 'similar_1' in request.form:
            k = 1
        elif 'similar_2' in request.form:
            k = 2
        elif 'similar_3' in request.form:
            k = 3
        elif 'similar_4' in request.form:
            k = 4

    #try to use existing query results.
    if text != None:
        check_txt = text.lower()
        if check_txt == 'data science':
            print 'coming -----'
            return dsi_ds()
        elif check_txt in ['data science jobs', 'data science job', 'jobs', 'job', 'employment', 'data science employment']: 
            return dsi_jobs()
        elif check_txt in ['data science news', 'news']: 
            return dsi_news()
        elif check_txt == 'big data':
            return dsi_bd()
        elif check_txt == 'machine learning':
            return dsi_ml()
        elif check_txt == 'data mining':
            return dsi_dm()
        elif check_txt == 'analytics' or 'analysis' in check_txt:
            return dsi_an()

    
    tot = 5
    urls = []
    titles = []
    summary = []
    start = 1
    end = tot+1

    if k >= 0 or k == -2: 
        t0 = time()
        print 'start query---'
        if k != -2:
            j =  int(curr_idx[k])
            text = df.iloc[j]['title'].decode('utf-8')
            more_title = text
            print 'before signature---', k, j, curr_idx[k]
            sign = df.iloc[j]['signature']
        elif len(text) > 0:
            more_title = text
            text = text.lower()
            words = text.split()
            
            vec = None
            cnt = 0
            for word in words:
                if word in model.vocab:
                    if vec == None:
                        vec = model[word] 
                    else:
                        vec += model[word] 
                    cnt += 1
            vec *= 1.0/cnt
            if vec != None:      
                df['check_sim'] = df.w2v_centroid.map(lambda x: get_cosine2(vec, x))
                ret = df['check_sim'].values.argsort()[::-1]
                #print 'sign -------', sign
                start = 0
                end = 5
                
        more_start = 0
        more_ret = ret
    else:
        if more_start > 0:
            text = more_title
        if more_start + 5 < len(more_ret):
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end
        else:
            more_start -= 5
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end

            
    cnt = 0
    for i in ret[start:end]:
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    if k >= 0:
        more_title = text
        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return render_template('listtopic.html', title = more_title, urls_out = urls, titles_out = titles, summary_out=summary, k=5) 


        

@app.route('/dsi_ds/')
def dsi_ds():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df

    more_title = None
    more_start = 0
    
    ret = df['dsi_w2v_sim'].values.argsort()[::-1]
    more_ret = ret
    
    tot = 5
    urls = []
    titles = []
    summary = []

    cnt = 0
    for i in ret[:tot]:
        print '-------idx =', cnt, i
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1    
    return render_template('listtopic.html', title = u'Data Science', urls_out = urls, titles_out = titles, summary_out=summary, k=5) 

@app.route('/dsi_ds/', methods=['POST'])
def dsi_ds_more():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df

    
    k = -1
    if request.method == 'POST':
        if 'query_0' in  request.form:
            more_start += 5  
            #print more_start, len(more_ret)
        elif 'similar_0' in request.form:
            k = 0
        elif 'similar_1' in request.form:
            k = 1
        elif 'similar_2' in request.form:
            k = 2
        elif 'similar_3' in request.form:
            k = 3
        elif 'similar_4' in request.form:
            k = 4

    tot = 5
    urls = []
    titles = []
    summary = []
    start = 1
    end = tot+1

    if k >= 0:        
        j =  int(curr_idx[k])
        text = df.iloc[j]['title'].decode('utf-8')
        more_title = text
        print 'before signature---', k, j, curr_idx[k]
        sign = df.iloc[j]['signature']
        print 'after signature---'
        ret = aG.get_max_distances_idx(sign)
        print 'after distance---'
        more_start = 0
        more_ret = ret
    else:
        if more_title == None:
            text = 'Data Science'
        else:
            text = more_title
        if more_start + 5 < len(more_ret):
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end
        else:
            more_start -= 5
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end

    cnt = 0
    for i in ret[start:end]:
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    if k >= 0 or more_title != None:
        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return render_template('listtopic.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary, k=5) 


@app.route('/dsi_bd/')
def dsi_bd():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df

    more_title = None
    more_start = 0
    
    ret = df['bd_w2v_sim'].values.argsort()[::-1]
    more_ret = ret
    
    tot = 5
    urls = []
    titles = []
    summary = []

    cnt = 0
    for i in ret[:tot]:
        print '-------idx =', cnt, i
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    return render_template('listtopic.html', title = u'Big Data', urls_out = urls, titles_out = titles, summary_out=summary, k=5) 

@app.route('/dsi_bd/', methods=['POST'])
def dsi_bd_more():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df

    
    k = -1
    if request.method == 'POST':
        if 'query_0' in  request.form:
            more_start += 5  
            #print more_start, len(more_ret)
        elif 'similar_0' in request.form:
            k = 0
        elif 'similar_1' in request.form:
            k = 1
        elif 'similar_2' in request.form:
            k = 2
        elif 'similar_3' in request.form:
            k = 3
        elif 'similar_4' in request.form:
            k = 4

    tot = 5
    urls = []
    titles = []
    summary = []
    start = 1
    end = tot+1

    if k >= 0:        
        j =  int(curr_idx[k])
        text = df.iloc[j]['title'].decode('utf-8')
        more_title = text
        print 'before signature---', k, j, curr_idx[k]
        sign = df.iloc[j]['signature']
        print 'after signature---'
        ret = aG.get_max_distances_idx(sign)
        print 'after distance---'
        more_start = 0
        more_ret = ret
    else:
        if more_title == None:
            text = 'Big Data'
        else:
            text = more_title
        if more_start + 5 < len(more_ret):
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end
        else:
            more_start -= 5
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end

    cnt = 0
    for i in ret[start:end]:
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    if k >= 0 or more_title != None:
        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return render_template('listtopic.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary, k=5) 



@app.route('/dsi_news/')
def dsi_news():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df

    more_title = None
    more_start = 0
    
    ret = df['dsn_w2v_sim'].values.argsort()[::-1]
    more_ret = ret
    
    tot = 5
    urls = []
    titles = []
    summary = []

    cnt = 0
    for i in ret[:tot]:
        print '-------idx =', cnt, i
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    return render_template('listtopic.html', title = u'Data Science News', urls_out = urls, titles_out = titles, summary_out=summary, k=5) 

@app.route('/dsi_news/', methods=['POST'])
def dsi_news_more():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df

    
    k = -1
    if request.method == 'POST':
        if 'query_0' in  request.form:
            more_start += 5  
            #print more_start, len(more_ret)
        elif 'similar_0' in request.form:
            k = 0
        elif 'similar_1' in request.form:
            k = 1
        elif 'similar_2' in request.form:
            k = 2
        elif 'similar_3' in request.form:
            k = 3
        elif 'similar_4' in request.form:
            k = 4

    tot = 5
    urls = []
    titles = []
    summary = []
    start = 1
    end = tot+1

    if k >= 0:        
        j =  int(curr_idx[k])
        text = df.iloc[j]['title'].decode('utf-8')
        more_title = text
        print 'before signature---', k, j, curr_idx[k]
        sign = df.iloc[j]['signature']
        print 'after signature---'
        ret = aG.get_max_distances_idx(sign)
        print 'after distance---'
        more_start = 0
        more_ret = ret
    else:
        if more_title == None:
            text = 'Data Science News'
        else:
            text = more_title
        if more_start + 5 < len(more_ret):
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end
        else:
            more_start -= 5
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end

    cnt = 0
    for i in ret[start:end]:
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    if k >= 0 or more_title != None:
        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return render_template('listtopic.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary, k=5) 

    
@app.route('/dsi_ml/')
def dsi_ml():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df


    more_title = None
    more_start = 0
    
    ret = df['ml_w2v_sim'].values.argsort()[::-1]
    more_ret = ret
    
    tot = 5
    urls = []
    titles = []
    summary = []

    cnt = 0
    for i in ret[:tot]:
        print '-------idx =', cnt, i
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    return render_template('listtopic.html', title = u'Machine Learning', urls_out = urls, titles_out = titles, summary_out=summary, k=5) 

@app.route('/dsi_ml/', methods=['POST'])
def dsi_ml_more():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df

    
    k = -1
    if request.method == 'POST':
        if 'query_0' in  request.form:
            more_start += 5  
            #print more_start, len(more_ret)
        elif 'similar_0' in request.form:
            k = 0
        elif 'similar_1' in request.form:
            k = 1
        elif 'similar_2' in request.form:
            k = 2
        elif 'similar_3' in request.form:
            k = 3
        elif 'similar_4' in request.form:
            k = 4

    tot = 5
    urls = []
    titles = []
    summary = []
    start = 1
    end = tot+1

    if k >= 0:        
        j =  int(curr_idx[k])
        text = df.iloc[j]['title'].decode('utf-8')
        more_title = text
        print 'before signature---', k, j, curr_idx[k]
        sign = df.iloc[j]['signature']
        print 'after signature---'
        ret = aG.get_max_distances_idx(sign)
        print 'after distance---'
        more_start = 0
        more_ret = ret
    else:
        if more_title == None:
            text = 'Machine Learning'
        else:
            text = more_title
        if more_start + 5 < len(more_ret):
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end
        else:
            more_start -= 5
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end

    cnt = 0
    for i in ret[start:end]:
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    if k >= 0 or more_title != None:
        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return render_template('listtopic.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary,k=5) 


@app.route('/dsi_dm/')
def dsi_dm():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df

    more_title = None
    more_start = 0
    
    ret = df['dm_w2v_sim'].values.argsort()[::-1]
    more_ret = ret
    
    tot = 5
    urls = []
    titles = []
    summary = []

    cnt = 0
    for i in ret[:tot]:
        print '-------idx =', cnt, i
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    return render_template('listtopic.html', title = u'Data Mining', urls_out = urls, titles_out = titles, summary_out=summary,k=5) 

@app.route('/dsi_dm/', methods=['POST'])
def dsi_dm_more():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df

    
    k = -1
    if request.method == 'POST':
        if 'query_0' in  request.form:
            more_start += 5  
            #print more_start, len(more_ret)
        elif 'similar_0' in request.form:
            k = 0
        elif 'similar_1' in request.form:
            k = 1
        elif 'similar_2' in request.form:
            k = 2
        elif 'similar_3' in request.form:
            k = 3
        elif 'similar_4' in request.form:
            k = 4

    tot = 5
    urls = []
    titles = []
    summary = []
    start = 1
    end = tot+1

    if k >= 0:        
        j =  int(curr_idx[k])
        text = df.iloc[j]['title'].decode('utf-8')
        more_title = text
        print 'before signature---', k, j, curr_idx[k]
        sign = df.iloc[j]['signature']
        print 'after signature---'
        ret = aG.get_max_distances_idx(sign)
        print 'after distance---'
        more_start = 0
        more_ret = ret
    else:
        if more_title == None:
            text = 'Deep Mining'
        else:
            text = more_title
        if more_start + 5 < len(more_ret):
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end
        else:
            more_start -= 5
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end

    cnt = 0
    for i in ret[start:end]:
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    if k >= 0 or more_title != None:
        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return render_template('listtopic.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary, k=5) 


@app.route('/dsi_an/')
def dsi_an():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df


    more_title = None
    more_start = 0
    
    ret = df['an_w2v_sim'].values.argsort()[::-1]
    more_ret = ret
    
    tot = 5
    urls = []
    titles = []
    summary = []

    cnt = 0
    for i in ret[:tot]:
        print '-------idx =', cnt, i
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    return render_template('listtopic.html', title = u'Analytics', urls_out = urls, titles_out = titles, summary_out=summary, k=5) 

@app.route('/dsi_an/', methods=['POST'])
def dsi_an_more():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df

    
    k = -1
    if request.method == 'POST':
        if 'query_0' in  request.form:
            more_start += 5  
            #print more_start, len(more_ret)
        elif 'similar_0' in request.form:
            k = 0
        elif 'similar_1' in request.form:
            k = 1
        elif 'similar_2' in request.form:
            k = 2
        elif 'similar_3' in request.form:
            k = 3
        elif 'similar_4' in request.form:
            k = 4

    tot = 5
    urls = []
    titles = []
    summary = []
    start = 1
    end = tot+1

    if k >= 0:        
        j =  int(curr_idx[k])
        text = df.iloc[j]['title'].decode('utf-8')
        more_title = text
        print 'before signature---', k, j, curr_idx[k]
        sign = df.iloc[j]['signature']
        print 'after signature---'
        ret = aG.get_max_distances_idx(sign)
        print 'after distance---'
        more_start = 0
        more_ret = ret
    else:
        if more_title == None:
            text = 'Analytics'
        else:
            text = more_title
        if more_start + 5 < len(more_ret):
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end
        else:
            more_start -= 5
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end

    cnt = 0
    for i in ret[start:end]:
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    if k >= 0 or more_title != None:
        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return render_template('listtopic.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary, k=5) 


@app.route('/dsi_jobs/')
def dsi_jobs():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df


    more_title = None
    more_start = 0
    
    ret = df['dsj_w2v_sim'].values.argsort()[::-1]
    more_ret = ret
    
    tot = 5
    urls = []
    titles = []
    summary = []

    cnt = 0
    for i in ret[:tot]:
        print '-------idx =', cnt, i
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    return render_template('listtopic.html', title = u'Employment', urls_out = urls, titles_out = titles, summary_out=summary, k=5) 

@app.route('/dsi_jobs/', methods=['POST'])
def dsi_jobs_more():
    global more_start
    global more_ret
    global more_title
    global curr_idx
    global aG
    global df
    
    k = -1
    if request.method == 'POST':
        if 'query_0' in  request.form:
            more_start += 5  
            #print more_start, len(more_ret)
        elif 'similar_0' in request.form:
            k = 0
        elif 'similar_1' in request.form:
            k = 1
        elif 'similar_2' in request.form:
            k = 2
        elif 'similar_3' in request.form:
            k = 3
        elif 'similar_4' in request.form:
            k = 4

    tot = 5
    urls = []
    titles = []
    summary = []
    start = 1
    end = tot+1

    if k >= 0:        
        j =  int(curr_idx[k])
        text = df.iloc[j]['title'].decode('utf-8')
        more_title = text
        print 'before signature---', k, j, curr_idx[k]
        sign = df.iloc[j]['signature']
        print 'after signature---'
        ret = aG.get_max_distances_idx(sign)
        print 'after distance---'
        more_start = 0
        more_ret = ret
    else:
        if more_title == None:
            text = 'Employment'
        else:
            text = more_title
        if more_start + 5 < len(more_ret):
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end
        else:
            more_start -= 5
            ret = more_ret[more_start:]
            start = more_start
            end = more_start + tot
            more_start = end

    cnt = 0
    for i in ret[start:end]:
        curr_idx[cnt] = i
        urls.append(df.iloc[i]['url'])
        titles.append(df.iloc[i]['title'].decode('utf-8'))
        summary.append(df.iloc[i]['heading'].decode('utf-8'))
        cnt += 1

    if k >= 0 or more_title != None:
        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return render_template('listtopic.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary, k=5) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
