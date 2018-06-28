# coding: utf-8
# ------------------------------------------------
#    作用：获取百度翻译接口
#    日期：2018-03-25
#    作者：呆呆
#    微信：zhixuez
# ------------------------------------------------


from selenium import webdriver
import requests
import pymysql
from bs4 import BeautifulSoup
import lxml
import htmllib
import os
import re
import json
import sys

driver = webdriver.PhantomJS(executable_path="C:/Python27/phantomjs-2.1.1-windows/bin/phantomjs.exe")

reload(sys)

sys.setdefaultencoding('utf-8')

HOSTNAME = '127.0.0.1'
USERNAME = 'root'
PASSWORD = ''
DATABASE = 'pydata'

conn = pymysql.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE, charset="utf8")
cur = conn.cursor()

cookie = {
    'POST':'transapi HTTP/1.1',
    'Host':'fanyi.baidu.com',
    'Connection':'keep-alive',
    'Content-Length':'44',
    'Accept':'*/*',
    'Origin':'http://fanyi.baidu.com',
    'X-Requested-With':'XMLHttpRequest',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer':'http://fanyi.baidu.com/',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9'
}

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

siteurl = 'http://fanyi.sogou.com/?fr=websearch_submit&pid=&keyword=i%20am%20sure%20you%20can%20do%20well#auto/zh-CHS/i%20am%20sure%20you%20can%20do%20well'

# 列表
def baidu():

    word = "空调"

    res = requests.get(siteurl, headers=headers)
    print res.status_code
    # print res.text

    print res.url
    if res.status_code == 200:
        res.close()
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')

        print soup


def get_word():

    # pass
    source = driver.get(siteurl)
    #
    # # print source
    #
    #
    print driver.page_source


# baidu()

get_word()