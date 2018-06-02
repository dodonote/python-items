# coding: utf-8
# ------------------------------------------------
#    作用：抓取英语4级词汇
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

siteurl = 'http://word.iciba.com/?action=words&class=11&course={}'

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
        rowcount = cur.executemany('INSERT INTO english_vocabulary (`course`,`word`,`symbol`,`interpret`) values(%s,%s,%s,%s)', data)
        conn.commit()

        # cur.close()
        # conn.close()

        if(page < 227):
            page = page + 1
            crawl_vocabulary(page)
        # print data

        # return data

# 卡片
def crawl_card():

    siteurl = 'http://word.iciba.com/?action=card'
    res = requests.get(siteurl)
    print res.status_code
    print res.text
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
            sub_arg = (title, w, y, s)
            data.append(sub_arg)

            # print data
            # for li in letter.find_next():
            #     args = li.find("a")
            #     sub_arg = (letter.get_text(),args['href'],re.findall(u".*\(", args.get_text())[0].replace("(",""),re.findall(u"\d+\.?\d*", args.find("em").get_text())[0])
            #     data.append(sub_arg)

            # print li


            print data
        rowcount = cur.executemany('INSERT INTO english_vocabulary (`course`, `word`,`symbol`,`interpret`) values(%s,%s,%s,%s)',data)
        conn.commit()

        # cur.close()
        # conn.close()

        # print data

        return data

# 更新句子
def update_sentence(q):

    # siteurl = 'http://m.youdao.com/dict?le=eng&q={}'
    # headers = {
    #     'Host': 'm.youdao.com',
    #     'Connection': 'keep-alive',
    #     'Cache-Control': 'max-age=0',
    #     'Upgrade-Insecure-Requests': '1',
    #     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Language': 'zh-CN,zh;q=0.9',
    #     "Referer": "http://m.youdao.com/",
    #     'Cookie': 'OUTFOX_SEARCH_USER_ID=-1626789928@111.193.0.93; OUTFOX_SEARCH_USER_ID_NCOO=2052153861.2079623; _ga=GA1.2.1758753673.1526546698; UM_distinctid=163863ce381174-089fc7dbd9bee4-b353461-1fa400-163863ce382336; P_INFO=boom180@163.com|1526965644|0|search|11&18|null&null&null#bej&null#10#0#0|&0||boom180@163.com; JSESSIONID=abcM--lB0PRTE8RAlNiow; DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; JSESSIONID=abcqmx6VN8hZ_9hClNiow; ___rl__test__cookies=1527007818922'
    # }

    # headers = {
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding":"gzip, deflate",
    #     "Accept-Language": "zh-CN,zh;q=0.9",
    #     "Connection":"keep-alive",
    #     "Host":"beta.17.com",
    #     "Referer":"http://beta.17.com/fsmanager/home/index/",
    #     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    # }
    # headers = {'user-agent': 'my-app/0.0.1'}


    cur.execute("select id, word from english_vocabulary where `sentence` = ''")
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
                # for letter in soup.select(".word_main_list li"):
                #
                #     # print letter
                #     w = letter.select(".word_main_list_w span")[0].get_text();
                #     y = letter.select(".word_main_list_y strong")[0].get_text();
                #     s = letter.select(".word_main_list_s span")[0].get_text();
                #
                #     # print w,y,s
                #     sub_arg = (title,w,y,s)
                #     data.append(sub_arg)

                    # print data
                    # for li in letter.find_next():
                    #     args = li.find("a")
                    #     sub_arg = (letter.get_text(),args['href'],re.findall(u".*\(", args.get_text())[0].replace("(",""),re.findall(u"\d+\.?\d*", args.find("em").get_text())[0])
                    #     data.append(sub_arg)

                        # print li


                    # print data
                rowcount = cur.executemany('update english_vocabulary set `sentence` = %s, `cn_sentence` = %s where id = %s', data)
                conn.commit()

                # cur.close()
                # conn.close()
            except ValueError as e:
                continue

# 日常英语
def daily_english():

    siteurl = 'http://www.cnpctest.com/rcyy900.htm'

    res = requests.get(siteurl)
    # print res.status_code
    # print res.text

    print res.url
    if res.status_code == 200:
        res.close()
        res.encoding = 'gb2312'
        soup = BeautifulSoup(res.text, 'lxml')

        # for letter in soup.find_all(class_="cartree-letter"):
        #     print letter.get_text()

        # data = []
        data = soup.select(".MsoNormal > font > span")[0].get_text();

        category = "";

        arr = data.split("\n")
        # print arr
        i = 1
        ci = 0
        for yy,item in enumerate(arr):

            result = []
            item = item.strip()

            # if i >= 10:
            #     break

            if ci == 1:
                ci = 0
                continue

            if not item:
                continue

            if item and not item[:1].isdigit():

                category = item

            print "aaa" + item
            print "bbb" + arr[yy]
            print "ccc" + arr[yy+1]
            print yy
            print "\n==============\n"

            if item and item[:1].isdigit():

                sub_ary = (category, item)
                result.append(sub_ary)

                # print i
                # rowcount = cur.executemany('insert into english_daily (cat_name,sentence) values (%s, %s)', result)
                # conn.commit()
                #
                # print arr[i]
                if item[:1] and not arr[yy+1].strip()[:1].isdigit():

                    print "\nqqqqqqqqqqqqqqqqqqqqqqqqqq\n"
                    print item
                    print item[:1]
                    print yy
                    print arr[yy]
                    print arr[yy+1]
                    print arr[yy+1][:1]
                    print "endqqqqqqqqqqqqqqqqqqqqq\n"

                    result = []
                    item = item + arr[yy+1].strip()
                    sub_ary = (category, item)
                    result.append(sub_ary)

                    # print "=========================="
                    # print item
                    # print "\n"
                    rowcount = cur.executemany('insert into english_daily (cat_name,sentence) values (%s, %s)', result)
                    conn.commit()

                    ci = 1
                else:

                    # print result + "\n"
                    rowcount = cur.executemany('insert into english_daily (cat_name,sentence) values (%s, %s)', result)
                    conn.commit()
                    ci = 0

            i = i + 1
                    # print item[0]
        # print data

# 阅读理解 故事
def readStory():

    '''
    读取文档 写入数据库
    :return:
    '''

    f = open(u"F:/学习文档\英语/书虫/牛津书虫文本_分册txt/1A_01.爱情与金钱.txt")
    line = f.readline()


    i = 0
    ii = ""
    y = 0
    yy = ""
    while line:

        if not line.strip():

            line = f.readline()
            continue

        #英文
        # print line.strip()[2:]
        if line.strip()[2:] == 'Chapter':

            print ii
            if ii and yy:

                print ii,yy
                rowcount = cur.execute("insert into english_bookworm (`en`, `cn`) values (%s, %s)", (ii, yy))
                conn.commit()

            ii = ""
            yy = ""
            ii = line.strip()
            i = 1
            y = 0

            line = f.readline()
            continue

        # 汉字
        if line.strip().isdigit():

            yy = line.strip()
            i = 0
            y = 1

            line = f.readline()
            continue

        if i >= 1:

            ii = ii + line.strip()

            i = i + 1
            line = f.readline()
            continue

        if y >= 1:

            yy = yy + line.strip()

            y = y + 1
            line = f.readline()
            continue



        # print line
        line = f.readline()

    f.close()

# 每日一句
def wordOfDay():

    siteurl = 'http://news.iciba.com/views/dailysentence/daily.html#!/detail/title/2018-05-18'

    res = requests.get(siteurl)
    # print res.status_code
    # print res.text

    print res.url
    if res.status_code == 200:
        res.close()
        res.encoding = 'UTF-8'
        soup = BeautifulSoup(res.text, 'lxml')

        print res.text



def main():

    page = 1
    # crawl_vocabulary(page)
    # crawl_card()
    q = 'comment'
    # update_sentence(q)
    # daily_english()
    # readStory()
    wordOfDay()

if __name__ == '__main__':

    main()