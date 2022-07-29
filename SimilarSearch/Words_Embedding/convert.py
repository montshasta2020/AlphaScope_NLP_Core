import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pandas as pd

from langconv import *

df_whole = pd.read_csv('../data/huizhou-huaxia-v2-s.csv')

#df = df_whole[df_whole['domain'] == 'huaxia.com']
df = df_whole

def convert_traditional2simplified(x):
    return Converter('zh-hans').convert(x.decode('utf-8'))

#df['content'] = df.content.map(lambda x: convert_traditional2simplified(x))
df['title'] = df.title.map(lambda x: convert_traditional2simplified(x))


df.to_csv('../data/huizhou-huaxia-v2-s-1.csv', encoding='utf-8', index=False)