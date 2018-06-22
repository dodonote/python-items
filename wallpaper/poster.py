# coding: utf-8

# ------------------------------------------------
#    功能：生成 手机 壁纸
#    日期：2018-03-25
#    作者：呆呆
#    微信：zhixuez
# ------------------------------------------------

import requests
import pymysql
from bs4 import BeautifulSoup
import lxml
import htmllib
import urllib
import datetime
import os
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

# 图片数组
img_arr = []

# 抓取美图
def crawl_pic(next_url):

    if not next_url:

        url = 'http://www.3gbizhi.com/wallMV/3091.html'
    else:
        url = next_url

    res = requests.get(url)

    if res.status_code == 200:

        res.close()
        res.encoding = 'utf-8'

        # print res.text
        soup = BeautifulSoup(res.text, 'lxml')

        html = soup.select(".photo")[0]

        img = html.select(".binimg")[0]['src']
        desc = html.select(".binimg")[0]['alt']

        next_url = html.select(".next")[0]['href']

        url_arr = res.url.split("/")
        print url_arr

        dir = os.path.abspath(".")
        filename = os.path.join(dir,"img/"+url_arr[3]+"/"+url_arr[4])
        filename = filename.replace(".html",".jpg")

        print filename

        urllib.urlretrieve(img, filename)

        print img
        print desc
        print next_url
        print img_arr

        print (img not in img_arr)

        print "----------------------------------"
        # 循环逻辑
        if next_url and img not in img_arr:

            img_arr.append(img)
            crawl_pic(next_url)

def main():

    # dir = os.path.abspath('.')
    # work_path = os.path.join(dir, 'Python-2.7.5.tar.bz2')

    # print dir
    # print work_path

    crawl_pic('')

if __name__ == '__main__':

    main()