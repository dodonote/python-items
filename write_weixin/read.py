# coding: utf-8
# ------------------------------------------------
#    作用：从数据库读取公众号信息
#    日期：2018-03-25
#    作者：呆呆
#    微信：zhixuez
# ------------------------------------------------


import requests
import pymysql
from bs4 import BeautifulSoup
import lxml
import htmllib
import re
import json
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

HOSTNAME = '127.0.0.1'
USERNAME = 'root'
PASSWORD = ''
DATABASE = 'pydata'

conn = pymysql.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE, charset="utf8")
cur = conn.cursor()

# 列表
def read_vocabulary(page):

    pass



def main():

    page = 1
    # crawl_vocabulary(page)
    # crawl_card()
    q = 'comment'
    # update_sentence(q)
    # daily_english()
    # readStory()
    read_vocabulary()

if __name__ == '__main__':

    main()