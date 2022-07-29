#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, session
import cPickle as pickle
import pandas as pd
import numpy as np
import math
#from utilities import get_cars_names'


app = Flask(__name__)
app.secret_key = 'not a secret'

#with open('pkl/model_gd_toyota.pkl') as f:
#    model_gd_toyota = pickle.load(f)

#with open('pkl/models_gd-8.pkl') as f:
#    model_gd = pickle.load(f)

df = pd.read_csv("data/typics_classifications.csv")

# home page
@app.route('/')
def index():
    session['price'] = None
    return render_template('index.html')

@app.route('/huiwenhua/')
def huiwenhua():
    return render_template('huiwenhua.html')


@app.route('/huizhou_shenghuo/')
def huizhou_shenghuo():
    return render_template('huizhou_shenghuo.html')

@app.route('/huixue_yanjiu/')
def huixue_yanjiu():
    return render_template('huixue_yanjiu.html')


@app.route('/more/')
def more():
    return render_template('used-car-deal.html')

@app.route('/price/', methods=['POST'])
def price():
    return render_template('used-car-sell.html')

@app.route('/sell/', methods=['GET', 'POST'])
def sell():
    print 'sell'
    # car_years = request.args.get('car_years')
    # car_models = request.args.get('car_models')
    # test = request.args.get('test6')
    # print car_years

    price = None
    #return render_template('used-car-sell.html', years = years, car_names=car_names, makers = makers, models=models, conditions=conditions, mileages=mileages, city_names=city_names, price=None)
    return render_template('used-car-sell.html')

    
@app.route('/querybytopic1/')
def querybytopic1():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽州人文', urls_out = urls, titles_out = titles)

@app.route('/querybytopic2/')
def querybytopic2():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 17)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽州建筑和雕刻', urls_out = urls, titles_out = titles)


@app.route('/querybytopic3/')
def querybytopic3():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 7) | (df['topic'] == 8) ]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽州历史', urls_out = urls, titles_out = titles)

@app.route('/querybytopic4/')
def querybytopic4():
    topic_df = df.ix[(df['topic'] == 6)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽菜', urls_out = urls, titles_out = titles)

@app.route('/querybytopic5/')
def querybytopic5():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 19)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽州民居', urls_out = urls, titles_out = titles)

@app.route('/querybytopic6/')
def querybytopic6():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 10) | (df['topic'] == 15)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽州风光', urls_out = urls, titles_out = titles)

@app.route('/querybytopic7/')
def querybytopic7():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 2) | (df['topic'] == 18)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'徽商，徽剧', urls_out = urls, titles_out = titles)

@app.route('/querybytopic8/')
def querybytopic8():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 0) | (df['topic'] == 1)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'祠堂文化与传统 ', urls_out = urls, titles_out = titles)

@app.route('/querybytopic9/')
def querybytopic9():
#    topic_df = df.ix[(df['topic'] == 5) | (df['topic'] == 11) | (df['topic'] == 16) | (df['topic'] == 18)]
    topic_df = df.ix[(df['topic'] == 4) | (df['topic'] == 12)]
    s_df = topic_df.sample(n=10)
        
    urls = s_df['url'].values
    titles = s_df['title'].str.decode('utf-8').values
    
    return render_template('listtopic.html', title = u'理学，新安学派', urls_out = urls, titles_out = titles)



@app.route('/querybyprice/', methods=['POST'])
def querybyprice():
    return render_template('used-car-buy.html')

@app.route('/buy/')
def buy():
    print 'buy'
    return render_template('used-car-buy.html')

@app.route('/explore/')
def explore():
    return render_template('index2.html')

@app.route('/price_old/', methods=['GET', 'POST'])
def price_old():
    return redirect(url_for('sell'))

@app.route('/showprice/')
def show_price():
    # {% for item in request.args.get('forward_list', '').split(',') %}
    #     {{ item }}
    # {% endfor %}
    return render_template('used-car-explore.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
