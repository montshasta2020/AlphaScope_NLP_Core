#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, session
from gensim import corpora, models, similarities
from gensim.similarities import MatrixSimilarity

import cPickle as pickle
import pandas as pd
import numpy as np
#import math
#from utilities import get_cars_names'

app = Flask(__name__)
app.secret_key = 'not a secret'

with open('pkl/lsi_model.pkl') as f:
    lsi = pickle.load(f)
with open('pkl/lsi_index.pkl') as f:
    lsi_index = pickle.load(f)
with open('pkl/lsi_dictionary.pkl') as f:
    dictionary = pickle.load(f)

df = pd.read_csv("data/huizhou_web_content_slim_v2.csv")

global selected_title

# home page
@app.route('/')
def index():
    selected_title = 'empty'
    session['price'] = None
    return render_template('index.html')

@app.route('/', methods=['POST'])
def input_form_post():
    if request.method == 'POST':
        if 'query_0' in  request.form:    
            text = request.form['query_input']
            print text
            start = 0
            end = 5
        elif 'similar_0' in request.form:
            text = request.form['similar_input0']
            print text
            start = 1
            end = 6
        elif 'similar_1' in request.form:
            text = request.form['similar_input1']
            start = 1
            end = 6
        elif 'similar_2' in request.form:
            text = request.form['similar_input2']
            start = 1
            end = 6
        elif 'similar_3' in request.form:
            text = request.form['similar_input3']
            start = 1
            end = 6
        elif 'similar_4' in request.form:
            text = request.form['similar_input4']
            start = 1
            end = 6

    text_list = list(text)
    ml_bow = dictionary.doc2bow(text_list)  
    ml_lsi = lsi[ml_bow]
    print len(ml_lsi)
    sims = lsi_index[ml_lsi]  
    sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    tot = 6
    labels, sim_values = zip(*sort_sims[0:tot])

    urls = []
    titles = []
    summary = []
    
    #more_title = u'"' + text + u'" ' + u"相关文章" 
    for i in range(start, end):
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
    if request.method == 'POST':
        if 'similar_0' in request.form:
            text = request.form['similar_input0']
        elif 'similar_1' in request.form:
            text = request.form['similar_input1']
        elif 'similar_2' in request.form:
            text = request.form['similar_input2']
        elif 'similar_3' in request.form:
            text = request.form['similar_input3']
        elif 'similar_4' in request.form:
            text = request.form['similar_input4']

    if (len(text) > 0):
        text_list = list(text)
        ml_bow = dictionary.doc2bow(text_list)  
        ml_lsi = lsi[ml_bow]
        print len(ml_lsi)
        sims = lsi_index[ml_lsi]  
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tot = 6
        labels, sim_values = zip(*sort_sims[0:tot])

        urls = []
        titles = []
        summary = []
        for i in range(1, tot):
            urls.append(df.iloc[labels[i]]['url'])
            titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
            summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return querybytopic1()

@app.route('/querybytopic2/', methods=['POST'])
def querybysimilar2():
    if request.method == 'POST':
        if 'similar_0' in request.form:
            text = request.form['similar_input0']
        elif 'similar_1' in request.form:
            text = request.form['similar_input1']
        elif 'similar_2' in request.form:
            text = request.form['similar_input2']
        elif 'similar_3' in request.form:
            text = request.form['similar_input3']
        elif 'similar_4' in request.form:
            text = request.form['similar_input4']

    if (len(text) > 0):
        text_list = list(text)
        ml_bow = dictionary.doc2bow(text_list)  
        ml_lsi = lsi[ml_bow]
        print len(ml_lsi)
        sims = lsi_index[ml_lsi]  
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tot = 6
        labels, sim_values = zip(*sort_sims[0:tot])

        urls = []
        titles = []
        summary = []
        for i in range(1, tot):
            urls.append(df.iloc[labels[i]]['url'])
            titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
            summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return querybytopic2()

@app.route('/querybytopic3/', methods=['POST'])
def querybysimilar3():
    if request.method == 'POST':
        if 'similar_0' in request.form:
            text = request.form['similar_input0']
        elif 'similar_1' in request.form:
            text = request.form['similar_input1']
        elif 'similar_2' in request.form:
            text = request.form['similar_input2']
        elif 'similar_3' in request.form:
            text = request.form['similar_input3']
        elif 'similar_4' in request.form:
            text = request.form['similar_input4']

    if (len(text) > 0):
        text_list = list(text)
        ml_bow = dictionary.doc2bow(text_list)  
        ml_lsi = lsi[ml_bow]
        print len(ml_lsi)
        sims = lsi_index[ml_lsi]  
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tot = 6
        labels, sim_values = zip(*sort_sims[0:tot])

        urls = []
        titles = []
        summary = []
        for i in range(1, tot):
            urls.append(df.iloc[labels[i]]['url'])
            titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
            summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return querybytopic3()
    
@app.route('/querybytopic4/', methods=['POST'])
def querybysimilar4():
    if request.method == 'POST':
        if 'similar_0' in request.form:
            text = request.form['similar_input0']
        elif 'similar_1' in request.form:
            text = request.form['similar_input1']
        elif 'similar_2' in request.form:
            text = request.form['similar_input2']
        elif 'similar_3' in request.form:
            text = request.form['similar_input3']
        elif 'similar_4' in request.form:
            text = request.form['similar_input4']

    if (len(text) > 0):
        text_list = list(text)
        ml_bow = dictionary.doc2bow(text_list)  
        ml_lsi = lsi[ml_bow]
        print len(ml_lsi)
        sims = lsi_index[ml_lsi]  
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tot = 6
        labels, sim_values = zip(*sort_sims[0:tot])

        urls = []
        titles = []
        summary = []
        for i in range(1, tot):
            urls.append(df.iloc[labels[i]]['url'])
            titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
            summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return querybytopic4()
    
@app.route('/querybytopic5/', methods=['POST'])
def querybysimilar5():
    if request.method == 'POST':
        if 'similar_0' in request.form:
            text = request.form['similar_input0']
        elif 'similar_1' in request.form:
            text = request.form['similar_input1']
        elif 'similar_2' in request.form:
            text = request.form['similar_input2']
        elif 'similar_3' in request.form:
            text = request.form['similar_input3']
        elif 'similar_4' in request.form:
            text = request.form['similar_input4']

    if (len(text) > 0):
        text_list = list(text)
        ml_bow = dictionary.doc2bow(text_list)  
        ml_lsi = lsi[ml_bow]
        print len(ml_lsi)
        sims = lsi_index[ml_lsi]  
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tot = 6
        labels, sim_values = zip(*sort_sims[0:tot])

        urls = []
        titles = []
        summary = []
        for i in range(1, tot):
            urls.append(df.iloc[labels[i]]['url'])
            titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
            summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return querybytopic5()    
    
@app.route('/querybytopic6/', methods=['POST'])
def querybysimilar6():
    if request.method == 'POST':
        if 'similar_0' in request.form:
            text = request.form['similar_input0']
        elif 'similar_1' in request.form:
            text = request.form['similar_input1']
        elif 'similar_2' in request.form:
            text = request.form['similar_input2']
        elif 'similar_3' in request.form:
            text = request.form['similar_input3']
        elif 'similar_4' in request.form:
            text = request.form['similar_input4']

    if (len(text) > 0):
        text_list = list(text)
        ml_bow = dictionary.doc2bow(text_list)  
        ml_lsi = lsi[ml_bow]
        print len(ml_lsi)
        sims = lsi_index[ml_lsi]  
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tot = 6
        labels, sim_values = zip(*sort_sims[0:tot])

        urls = []
        titles = []
        summary = []
        for i in range(1, tot):
            urls.append(df.iloc[labels[i]]['url'])
            titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
            summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return querybytopic6()    

@app.route('/querybytopic7/', methods=['POST'])
def querybysimilar7():
    if request.method == 'POST':
        if 'similar_0' in request.form:
            text = request.form['similar_input0']
        elif 'similar_1' in request.form:
            text = request.form['similar_input1']
        elif 'similar_2' in request.form:
            text = request.form['similar_input2']
        elif 'similar_3' in request.form:
            text = request.form['similar_input3']
        elif 'similar_4' in request.form:
            text = request.form['similar_input4']

    if (len(text) > 0):
        text_list = list(text)
        ml_bow = dictionary.doc2bow(text_list)  
        ml_lsi = lsi[ml_bow]
        print len(ml_lsi)
        sims = lsi_index[ml_lsi]  
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tot = 6
        labels, sim_values = zip(*sort_sims[0:tot])

        urls = []
        titles = []
        summary = []
        for i in range(1, tot):
            urls.append(df.iloc[labels[i]]['url'])
            titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
            summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return querybytopic7()    

@app.route('/querybytopic8/', methods=['POST'])
def querybysimilar8():
    if request.method == 'POST':
        if 'similar_0' in request.form:
            text = request.form['similar_input0']
        elif 'similar_1' in request.form:
            text = request.form['similar_input1']
        elif 'similar_2' in request.form:
            text = request.form['similar_input2']
        elif 'similar_3' in request.form:
            text = request.form['similar_input3']
        elif 'similar_4' in request.form:
            text = request.form['similar_input4']

    if (len(text) > 0):
        text_list = list(text)
        ml_bow = dictionary.doc2bow(text_list)  
        ml_lsi = lsi[ml_bow]
        print len(ml_lsi)
        sims = lsi_index[ml_lsi]  
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tot = 6
        labels, sim_values = zip(*sort_sims[0:tot])

        urls = []
        titles = []
        summary = []
        for i in range(1, tot):
            urls.append(df.iloc[labels[i]]['url'])
            titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
            summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return querybytopic8()    

@app.route('/querybytopic9/', methods=['POST'])
def querybysimilar9():
    if request.method == 'POST':
        if 'similar_0' in request.form:
            text = request.form['similar_input0']
        elif 'similar_1' in request.form:
            text = request.form['similar_input1']
        elif 'similar_2' in request.form:
            text = request.form['similar_input2']
        elif 'similar_3' in request.form:
            text = request.form['similar_input3']
        elif 'similar_4' in request.form:
            text = request.form['similar_input4']

    if (len(text) > 0):
        text_list = list(text)
        ml_bow = dictionary.doc2bow(text_list)  
        ml_lsi = lsi[ml_bow]
        print len(ml_lsi)
        sims = lsi_index[ml_lsi]  
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tot = 6
        labels, sim_values = zip(*sort_sims[0:tot])

        urls = []
        titles = []
        summary = []
        for i in range(1, tot):
            urls.append(df.iloc[labels[i]]['url'])
            titles.append(df.iloc[labels[i]]['title'].decode('utf-8'))
            summary.append(df.iloc[labels[i]]['summary'].decode('utf-8'))

        return render_template('query_result.html', title = text, urls_out = urls, titles_out = titles, summary_out=summary)  
    else:
        return querybytopic9()    
    
    
@app.route('/querybytopic1/')
def querybytopic1():
    topic_df = df.ix[(df['topic'] == 3) | (df['topic'] == 4) | (df['topic'] == 8) | (df['topic'] == 10) | (df['topic'] == 11) | (df['topic'] == 13) | (df['topic'] == 18)]
    #    topic_df = df.ix[(df['topic'] == 18)]
    s_df = topic_df.sample(n=10)

    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    summary = s_df['summary'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽州文化', urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/querybytopic2/')
def querybytopic2():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 2)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    summary = s_df['summary'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽派建筑', urls_out = urls, titles_out = titles, summary_out=summary)


@app.route('/querybytopic3/')
def querybytopic3():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 0) | (df['topic'] == 14)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    summary = s_df['summary'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'遗产传承', urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/querybytopic4/')
def querybytopic4():
    topic_df = df.ix[(df['topic'] == 16)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    summary = s_df['summary'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽州雕刻', urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/querybytopic5/')
def querybytopic5():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 6)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    summary = s_df['summary'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽派艺术', urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/querybytopic6/')
def querybytopic6():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 17)]
    s_df = topic_df.sample(n=10)
      
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    summary = s_df['summary'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽剧徽班', urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/querybytopic7/')
def querybytopic7():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 5)]
    s_df = topic_df.sample(n=10)
     
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    summary = s_df['summary'].str.decode('utf-8').values
   
    return render_template('listtopic.html', title = u'徽商', urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/querybytopic8/')
def querybytopic8():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 7)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    summary = s_df['summary'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'新安理学', urls_out = urls, titles_out = titles, summary_out=summary)

@app.route('/querybytopic9/')
def querybytopic9():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 15)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    summary = s_df['summary'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽学园地', urls_out = urls, titles_out = titles, summary_out=summary)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
