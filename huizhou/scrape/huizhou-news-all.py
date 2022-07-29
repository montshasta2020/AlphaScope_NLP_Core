
# coding: utf-8

import pandas as pd
from selenium import webdriver 
from bs4 import BeautifulSoup
import time

from datetime import date, timedelta, datetime
import os.path

t0 =  date.today()

#中安在线 	http://cul.anhuinews.com/
#徽州文化网	http://www.hzwh.com/
#徽州户外网	http://www.97hzhw.com/default.php
#古徽州大论坛 	http://517huizhou.com/forum.php
#故园徽州	http://www.99huizhou.com/
#徽州网	http://www.517huizhou.com/
#徽州吧	http://tieba.baidu.com/f?kw=%E5%BE%BD%E5%B7%9E&ie=utf-8
#安徽文化网	http://www.ahage.net/
#新黄山网	http://www.xinhs.cn/

