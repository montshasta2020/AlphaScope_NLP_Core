#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, session
from gensim import corpora, models, similarities
from gensim.similarities import MatrixSimilarity
from gensim.models import Word2Vec, KeyedVectors

import cPickle as pickle
import pandas as pd
import numpy as np
from time import time
import math
from ToolBox import Toolbox

global selected_title
global aT
global df
global s_sim
global get_more
global curr_txt
global labels
global start_idx

get_more = 0
s_sim = None
curr_txt = None
start_idx = 0

app = Flask(__name__)
app.secret_key = 'not a secret'

aT = Toolbox()

df = pd.read_csv("data/huizhou-web-slim_v3.csv")
model = KeyedVectors.load_word2vec_format('data/huizhou_model_format_v1.bin', binary=False)

#print 'unseralize ...'
#df['s_vec'] = df.s_vec.map(lambda x: aT.unserialized(x))
#print 'done!'

global selected_title

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
    selected_title = 'empty'
    session['price'] = None
    return render_template('index.html')

@app.route('/', methods=['POST'])
def input_form_post():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    k = -1
    if request.method == 'POST':
        
        if 'more_click' in  request.form:    
            k = -2
            get_more += 1
            start_idx = 0
        elif 'query_0' in  request.form:    
            text = request.form['query_input']
            print text
            get_more = 0
            start_idx = 1
    
    if(k != -2):
        curr_txt = text

        if (len(text) > 0):
            more_title = text
            words = text #text.split()
            
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
        
        if k >= 0:
            labels = ret[start_idx: 5+start_idx]
        else:
            labels = ret[:5]     
    else:
        text = curr_txt
        labels = ret[start_idx + get_more*5:(get_more+1)*5 + start_idx]
    
    urls = []
    titles = []
    summary = []
    
    #more_title = u'"' + text + u'" ' + u"相关文章" 
    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))
    
    #print text
    return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/huiwenhua/')
def huiwenhua():
    return render_template('huiwenhua.html')

@app.route('/huizhou_shenghuo/')
def huizhou_shenghuo():
    return render_template('huizhou_shenghuo.html')

@app.route('/huixue_yanjiu/')
def huixue_yanjiu():
    return render_template('huixue_yanjiu.html')

@app.route('/querybytopic1/', methods=['POST'])
def querybysimilar1():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    if request.method == 'POST':
        if 'more_click' in  request.form:    
            k = -2
            get_more += 1
            start_idx = 0        

    if(k != -2):
        curr_txt = text
        
        i = labels[k]
        #centroid_vec = df.iloc[i]['s_vec']
    
        #df['check_sim'] = df.s_vec.map(lambda x: aT.get_sim(x, centroid_vec))
        s_sim = df['hzwh_w2v_sim'].values.argsort()[::-1]
        
        labels = s_sim[start_idx: 5+start_idx]
    else:
        text = curr_txt
        labels = s_sim[start_idx + get_more*5:(get_more+1)*5 + start_idx]
    
    urls = []
    titles = []
    summary = []

    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

    return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  

@app.route('/querybytopic2/', methods=['POST'])
def querybysimilar2():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    if request.method == 'POST':
        if 'more_click' in  request.form:    
            k = -2
            get_more += 1
            start_idx = 0        

    if(k != -2):
        curr_txt = text
        
        s_sim = df['hzjz_w2v_sim'].values.argsort()[::-1]
        
        labels = s_sim[start_idx: 5+start_idx]
    else:
        text = curr_txt
        labels = s_sim[start_idx + get_more*5:(get_more+1)*5 + start_idx]
    
    urls = []
    titles = []
    summary = []

    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

    return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary) 

@app.route('/querybytopic3/', methods=['POST'])
def querybysimilar3():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    if request.method == 'POST':
        if 'more_click' in  request.form:    
            k = -2
            get_more += 1
            start_idx = 0        

    if(k != -2):
        curr_txt = text
            
        s_sim = df['ycjc_w2v_sim'].values.argsort()[::-1]
        
        labels = s_sim[start_idx: 5+start_idx]
    else:
        text = curr_txt
        labels = s_sim[start_idx + get_more*5:(get_more+1)*5 + start_idx]
    
    urls = []
    titles = []
    summary = []

    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

    return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary) 
    
@app.route('/querybytopic4/', methods=['POST'])
def querybysimilar4():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    if request.method == 'POST':
        if 'more_click' in  request.form:    
            k = -2
            get_more += 1
            start_idx = 0        

    if(k != -2):
        curr_txt = text
        
        s_sim = df['hzdk_w2v_sim'].values.argsort()[::-1]
        
        labels = s_sim[start_idx: 5+start_idx]
    else:
        text = curr_txt
        labels = s_sim[start_idx + get_more*5:(get_more+1)*5 + start_idx]
    
    urls = []
    titles = []
    summary = []

    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

    return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary) 
    
@app.route('/querybytopic5/', methods=['POST'])
def querybysimilar5():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    if request.method == 'POST':
        if 'more_click' in  request.form:    
            k = -2
            get_more += 1
            start_idx = 0        

    if(k != -2):
        curr_txt = text
        
        s_sim = df['hpys_w2v_sim'].values.argsort()[::-1]
        
        labels = s_sim[start_idx: 5+start_idx]
    else:
        text = curr_txt
        labels = s_sim[start_idx + get_more*5:(get_more+1)*5 + start_idx]
    
    urls = []
    titles = []
    summary = []

    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

    return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary) 
    
@app.route('/querybytopic6/', methods=['POST'])
def querybysimilar6():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    if request.method == 'POST':
        if 'more_click' in  request.form:    
            k = -2
            get_more += 1
            start_idx = 0        

    if(k != -2):
        curr_txt = text
        
        s_sim = df['hjhc_w2v_sim'].values.argsort()[::-1]
        
        labels = s_sim[start_idx: 5+start_idx]
    else:
        text = curr_txt
        labels = s_sim[start_idx + get_more*5:(get_more+1)*5 + start_idx]
    
    urls = []
    titles = []
    summary = []

    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

    return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)   

@app.route('/querybytopic7/', methods=['POST'])
def querybysimilar7():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    if request.method == 'POST':
        if 'more_click' in  request.form:    
            k = -2
            get_more += 1
            start_idx = 0        

    if(k != -2):
        curr_txt = text
        
        s_sim = df['hs_w2v_sim'].values.argsort()[::-1]
        
        labels = s_sim[start_idx: 5+start_idx]
    else:
        text = curr_txt
        labels = s_sim[start_idx + get_more*5:(get_more+1)*5 + start_idx]
    
    urls = []
    titles = []
    summary = []

    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

    return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)    

@app.route('/querybytopic8/', methods=['POST'])
def querybysimilar8():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    if request.method == 'POST':
        if 'more_click' in  request.form:    
            k = -2
            get_more += 1
            start_idx = 0        

    if(k != -2):
        curr_txt = text
        
        s_sim = df['xalx_w2v_sim'].values.argsort()[::-1]
        
        labels = s_sim[start_idx: 5+start_idx]
    else:
        text = curr_txt
        labels = s_sim[start_idx + get_more*5:(get_more+1)*5 + start_idx]
    
    urls = []
    titles = []
    summary = []

    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

    return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary) 


@app.route('/querybytopic9/', methods=['POST'])
def querybysimilar9():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    if request.method == 'POST':
        if 'more_click' in  request.form:    
            k = -2
            get_more += 1
            start_idx = 0        

    if(k != -2):
        curr_txt = text
        
        s_sim = df['hxyj_w2v_sim'].values.argsort()[::-1]
        
        labels = s_sim[start_idx: 5+start_idx]
    else:
        text = curr_txt
        labels = s_sim[start_idx + get_more*5:(get_more+1)*5 + start_idx]
    
    urls = []
    titles = []
    summary = []

    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

    return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)    
    
    
@app.route('/querybytopic1/')
def querybytopic1():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    global aT
    
    get_more = 0
        
    s_sim = df['hzwh_w2v_sim'].values.argsort()[::-1]
    labels = s_sim[:5]

    urls = []
    titles = []
    summary = []
        
    curr_txt = u'徽州文化'
    
    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))
    
    return render_template('query_result.html', title = curr_txt, urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/querybytopic2/')
def querybytopic2():
    
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    get_more = 0
    
    s_sim = df['hzjz_w2v_sim'].values.argsort()[::-1]
    labels = s_sim[:5]

    urls = []
    titles = []
    summary = []
        
    curr_txt = u'徽派建筑'
    
    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))
    
    return render_template('query_result.html', title = curr_txt, urls_out = urls, titles_out = titles, summary_out=summary)


@app.route('/querybytopic3/')
def querybytopic3():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    get_more = 0
    
    s_sim = df['ycjc_w2v_sim'].values.argsort()[::-1]
    labels = s_sim[:5]

    urls = []
    titles = []
    summary = []
        
    curr_txt = u'遗产继承'
    
    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))
    
    return render_template('query_result.html', title = curr_txt, urls_out = urls, titles_out = titles, summary_out=summary)


    
@app.route('/querybytopic4/')
def querybytopic4():
    
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    get_more = 0
    
    s_sim = df['hzdk_w2v_sim'].values.argsort()[::-1]
    labels = s_sim[:5]

    urls = []
    titles = []
    summary = []
        
    curr_txt = u'徽州雕刻'
    
    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))
    
    return render_template('query_result.html', title = curr_txt, urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/querybytopic5/')
def querybytopic5():
    
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    get_more = 0
    
    s_sim = df['hpys_w2v_sim'].values.argsort()[::-1]
    labels = s_sim[:5]

    urls = []
    titles = []
    summary = []
        
    curr_txt = u'徽派艺术'
    
    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))
    
    return render_template('query_result.html', title = curr_txt, urls_out = urls, titles_out = titles, summary_out=summary)


@app.route('/querybytopic6/')
def querybytopic6():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    get_more = 0
    
    s_sim = df['hjhc_w2v_sim'].values.argsort()[::-1]
    labels = s_sim[:5]

    urls = []
    titles = []
    summary = []
        
    curr_txt = u'徽剧徽菜'
    
    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))
    
    return render_template('query_result.html', title = curr_txt, urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/querybytopic7/')
def querybytopic7():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    get_more = 0
    
    s_sim = df['hs_w2v_sim'].values.argsort()[::-1]
    labels = s_sim[:5]

    urls = []
    titles = []
    summary = []
        
    curr_txt = u'徽商'
    
    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))
    
    return render_template('query_result.html', title = curr_txt, urls_out = urls, titles_out = titles, summary_out=summary)


@app.route('/querybytopic8/')
def querybytopic8():
    
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    get_more = 0
    
    s_sim = df['xalx_w2v_sim'].values.argsort()[::-1]
    labels = s_sim[:5]

    urls = []
    titles = []
    summary = []
        
    curr_txt = u'新安理学'
    
    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))
    
    return render_template('query_result.html', title = curr_txt, urls_out = urls, titles_out = titles, summary_out=summary)


@app.route('/querybytopic9/')
def querybytopic9():
    global s_sim
    global get_more
    global df
    global curr_txt
    global labels
    global start_idx
    
    get_more = 0
    
    s_sim = df['hxyj_w2v_sim'].values.argsort()[::-1]
    labels = s_sim[:5]

    urls = []
    titles = []
    summary = []
        
    curr_txt = u'徽学园地'
    
    for i in range(0, 5):
        urls.append(df.iloc[labels[i]]['url'])
        titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
        summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))
    
    return render_template('query_result.html', title = curr_txt, urls_out = urls, titles_out = titles, summary_out=summary)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
