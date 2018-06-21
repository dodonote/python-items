# coding: utf-8
# ------------------------------------------------
#    作用：抓取英语四级、六级、考研词汇
#    日期：2018-03-25
#    作者：呆呆
#    微信：zhixuez
# ------------------------------------------------


import requests
import pymysql
from bs4 import BeautifulSoup
import lxml
import htmllib
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

siteurl = 'http://word.iciba.com/?action=words&class=81&course={}'

# 列表
def crawl_vocabulary(page):

    res = requests.get(siteurl.format(page))
    # print res.status_code
    # print res.text

    print res.url
    if res.status_code == 200:
        res.close()
        soup = BeautifulSoup(res.text, 'lxml')

        # for letter in soup.find_all(class_="cartree-letter"):
        #     print letter.get_text()

        data = []
        title = soup.select(".word_h2 p")[0].get_text();
        for letter in soup.select(".word_main_list li"):

            # print letter
            w = letter.select(".word_main_list_w span")[0].get_text();
            y = letter.select(".word_main_list_y strong")[0].get_text();
            s = letter.select(".word_main_list_s span")[0].get_text();

            # print w,y,s
            sub_arg = (title.strip(),w.strip(),y.strip(),s.strip())
            data.append(sub_arg)

            # print data
            # for li in letter.find_next():
            #     args = li.find("a")
            #     sub_arg = (letter.get_text(),args['href'],re.findall(u".*\(", args.get_text())[0].replace("(",""),re.findall(u"\d+\.?\d*", args.find("em").get_text())[0])
            #     data.append(sub_arg)

                # print li


            print data
        rowcount = cur.executemany('INSERT INTO english_vocabulary_job (`course`,`word`,`symbol`,`interpret`) values(%s,%s,%s,%s)', data)
        conn.commit()

        # cur.close()
        # conn.close()

        if(page < 12):
            page = page + 1
            crawl_vocabulary(page)
        # print data

        # return data

# 更新句子
def update_sentence():

    cur.execute("select id, word from english_vocabulary_job where `sentence` = ''")
    word_data = cur.fetchall()
    # print headers

    for info in word_data:

        siteurl = 'http://www.youdao.com/w/eng/{}/#keyfrom=dict2.index'
        res = requests.get(siteurl.format(info[1]))

        print res.url
        # print res.status_code
        # print res.content

        # print res.url
        if res.status_code == 200:
            res.close()
            soup = BeautifulSoup(res.text, 'lxml')

            # for letter in soup.find_all(class_="cartree-letter"):
            #     print letter.get_text()

            data = []

            # html = soup.select("#examplesToggle")[0]

            # print html
            get_html = soup.select("#examplesToggle #bilingual ul > li p");
            if not get_html:
                continue

            try:
                en = soup.select("#examplesToggle #bilingual ul > li p")[0].get_text();
                cn = soup.select("#examplesToggle #bilingual ul > li p")[1].get_text();

                sub_arg = (en.strip(), cn.strip(), info[0])
                data.append(sub_arg)

                print en,cn

                    # print data
                rowcount = cur.executemany('update english_vocabulary_job set `sentence` = %s, `cn_sentence` = %s where id = %s', data)
                conn.commit()

                # cur.close()
                # conn.close()
            except ValueError as e:
                continue

def main():

    # page = 1
    # crawl_vocabulary(page)

    # 添加句子
    update_sentence()

if __name__ == '__main__':

    main()