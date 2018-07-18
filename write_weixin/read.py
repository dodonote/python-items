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
import datetime

reload(sys)

sys.setdefaultencoding('utf-8')

HOSTNAME = '127.0.0.1'
USERNAME = 'root'
PASSWORD = ''
DATABASE = 'pydata'

conn = pymysql.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE, charset="utf8")
cur = conn.cursor()

today = datetime.date.today().strftime("%Y-%m-%d")
today_ymd = datetime.date.today().strftime("%Y%m%d")

data_begin = '''
<section class="_editor" style="margin: 0px; padding: 0px; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <section style="margin: 20px auto 0px; padding: 6px; width: 300px; background-color: rgb(0, 96, 149);">
        <img src="https://image.ipaiban.com/upload-ueditor-image-20180612-1528778102053098075.png" data-type="png" class="" data-ratio="0.2610062893081761" data-w="318" style="margin: 0px auto; padding: 0px; display: block; vertical-align: top; height: auto !important; width: 170px !important; visibility: visible !important;"/>
        <section style="margin: 0px auto; padding: 0px; text-align: center;">
            <section style="margin: 3px 0px 10px; padding: 5px 0px 0px; display: inline-block; border-bottom: 4px solid white; font-size: 20px;">
                <section style="margin: 0px 0px 3px; padding: 5px 2px 0px; display: inline-block; border-bottom: 2px solid white;">
                    <section style="margin: -10px 0px 5px; padding: 0px; display: inline-block;">
                        <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; color: rgb(255, 255, 255); font-size: 18px; min-width: 1px;">
                            &nbsp;学习英语，开阔眼界&nbsp;
                        </p>
                    </section>
                </section>
            </section>
        </section>
    </section>
</section>
<p>
    <br/>
</p>
'''

data_vocabulary = '''
<section style="margin: 10px 0px 0px; padding: 16px; text-align: left; border: 1px dashed rgb(71, 193, 168); border-radius: 10px; line-height: 1.4;">
  <span style="color: rgb(12, 12, 12);"><strong style=";padding: 0px"><span style="padding: 0px; font-size: 18px; letter-spacing: 0.544px;">{{0}}&nbsp;</span></strong></span><span style="padding: 0px; font-size: 20px; color: rgb(0, 176, 240);">{{1}} </span><span style="padding: 0px; font-size: 20px; color: rgb(165, 165, 165);">{{2}}</span>
</section>
<p>
</p>
<p style="margin-top: 0px;margin-bottom: 0px;padding: 0px;clear: both;min-height: 1em">
    <span style=";padding: 0px;color: rgb(136, 136, 136)">【释义】{{3}}</span>
</p>
<p style="margin-top: 0px;margin-bottom: 0px;padding: 0px;clear: both;min-height: 1em">
    <span style=";padding: 0px;color: rgb(136, 136, 136)">【例句】{{4}}</span><br style=";padding: 0px"/>
</p>
<p style="margin-top: 0px;margin-bottom: 0px;padding: 0px;clear: both;min-height: 1em">
    <span style=";padding: 0px;color: rgb(136, 136, 136)">&nbsp; {{5}}</span>
</p>
<p>
</p>
'''

data_sentence = '''
<span style="margin: 0px; padding: 0px; color: rgb(136, 136, 136);">{{0}}</span><br style="margin: 0px; padding: 0px; color: rgb(136, 136, 136);"/>
'''

data_sentence_title = '''
<p>
    <br/>
</p>
<section style="margin: 0px; padding: 0px; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <section label="Copyright 2018 iPaiban All Rights Reserved （本样式已做版权保护，未经正式授权不允许任何第三方编辑器、企业、个人使用，违者必纠）" donone="shifuMouseDownPayStyle(&#39;shifu_imi_002&#39;)" style="margin: 0.5rem auto; padding: 0px; width: 24rem; border-width: initial; border-color: initial; border-style: none;">
        <section style="margin: 0px; padding: 0px; width: 384px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <section class="ipaiban-bg" style="margin: 0px; padding: 0.5rem 1rem; font-size: 1rem; background-color: rgb(134, 162, 223); border-radius: 8px; color: rgb(255, 255, 255); letter-spacing: 2px; font-weight: bolder;">
                <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both;">
                    <span style="margin: 0px; padding: 0px; font-family: 黑体; font-size: 18.6667px; text-align: center;">英语日常用语900句</span>
                </p>
            </section>
            <section class="ipaiban-btc" style="margin: auto; padding: 0px; width: 0px; border-top: 0.8em solid rgb(134, 162, 223); border-left: 0.8em solid transparent !important; border-right: 0.8em solid transparent !important;">
                <br style="margin: 0px; padding: 0px;"/>
            </section>
        </section>
    </section>
</section>
'''

data_end = '''
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; min-height: 1em; white-space: pre-wrap; font-size: 18px; font-style: italic;">
    <em style="margin: 0px; padding: 0px;"><strong style="margin: 0px; padding: 0px;"><img class="" data-ratio="1" src="https://image.ipaiban.com/upload-ueditor-image-20180612-1528778153975015710.gif" data-type="gif" data-w="128" style="margin: 0px; padding: 0px; height: 20px; width: 20px;"/></strong></em><span style="margin: 0px; padding: 0px;"><em style="margin: 0px; padding: 0px;"><strong style="margin: 0px; padding: 0px;">翻译：成功在于勤奋.</strong></em></span><br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; min-height: 1em; white-space: pre-wrap; font-size: 18px; font-style: italic;">
    <span style="margin: 0px; padding: 0px; font-size: 16px; color: rgb(255, 41, 65);"> &nbsp; &nbsp;回复：fy，获取翻译答案 </span>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; min-height: 1em; white-space: pre-wrap; font-size: 18px; font-style: italic;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; min-height: 1em; white-space: pre-wrap; font-size: 18px; font-style: italic;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <strong style="margin: 0px; padding: 0px;">推荐阅读：</strong>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483686&idx=1&sn=3e8c333a3975142c07751f5f6c2e3e19&chksm=fcde924fcba91b59aac3641474e76ccedcb03d6e3d7f520f2556f35840962fc26448c968585f&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【词汇】英语四级必备词汇 第1课</a>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483697&idx=1&sn=2209a5aeadb4a26b6d5d3607fc419cdb&chksm=fcde9258cba91b4e7d3a6fecbfd784a470ced0f85226904aae25af4ebdcd4ef54170a5606378&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【英语】为什么我们要学习英语？</a>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483661&idx=1&sn=44213e9fcd9d19ba54843bbff3f8e720&chksm=fcde9264cba91b72ce573929626d597407b1f466d9dd18faf148bd4dee42c6a4f03fa263939a&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【英语】如何学英语，看看这位同学的总结</a>
</p>
<p></p>
<section style="margin: 0.5rem auto; padding: 0px; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; width: 24rem; border-width: initial; border-color: initial; border-style: none;">
    <section style="margin: 0px; padding: 0px; width: 384px;">
        <section style="margin: 10px 0px; padding: 0px 5px; display: inline-block; vertical-align: middle;">
            <section style="margin: 10px 0px; padding: 0px;">
                <section class="ipaiban-blc" style="margin: 0px 0px -0.9em 0.5em; padding: 0px; height: 1.4em; border-left: 1px solid rgb(134, 162, 223);"></section>
                <section class="ipaiban-btc" style="margin: 0px; padding: 0px; width: 2.5em; border-top: 1px solid rgb(134, 162, 223);"></section>
                <section style="margin: 0px; padding: 0px 0.5em;">
                    <section style="margin: 0px; padding: 10px;">
                        <section style="margin: 0px; padding: 0px; text-align: center; font-size: 14px;">
                            <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; text-align: justify;">
                                <span style="margin: 0px; padding: 0px; color: rgb(178, 178, 178);">{sentence_en}<br style="margin: 0px; padding: 0px;"/>{sentence_cn}</span>
                            </p>
                        </section>
                    </section>
                </section>
                <section style="margin: 0px 0px 0px auto; padding: 0px; width: 2.5em;">
                    <section class="ipaiban-btc" style="margin: 0px; padding: 0px; width: 2.5em; border-top: 1px solid rgb(134, 162, 223);"></section>
                    <section class="ipaiban-blc" style="margin: -0.9em 0px 0px 2em; padding: 0px; height: 1.4em; border-left: 1px solid rgb(134, 162, 223);">
                        <br style="margin: 0px; padding: 0px;"/>
                    </section>
                </section>
            </section>
        </section>
    </section>
</section>
<p></p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <img class="" data-copyright="0" data-ratio="0.5109489051094891" src="https://image.ipaiban.com/upload-ueditor-image-20180613-1528865709491075593.jpg" data-type="gif" data-w="685" data-backw="558" data-backh="285" data-before-oversubscription-url="https://mmbiz.qpic.cn/mmbiz_png/ULGBRicThgZvQ8jYm3SalNFjeLAEhCDs0D7jaNNTswkKBdeTdEctECR0u1mNSWMZBWoPPrIpXaicXbBQL0DyHWqg/640?wx_fmt=gif" style="margin: 0px; padding: 0px; height: auto; width: 558px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51); text-align: center;">
    <span style="margin: 0px; padding: 0px; color: rgb(178, 178, 178); font-size: 12px;">✬如果你喜欢这篇文章，欢迎分享到朋友圈✬</span><br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51); text-align: center;">
    <span style="margin: 0px; padding: 0px; font-size: 12px; color: rgb(178, 178, 178);">评论功能现已开启，我们接受一切形式的吐槽和赞美</span>
</p>
'''

txt_name = 'english_weixin_' + today + ".txt"
f = open(txt_name, "a+")
f.truncate()

translate_sentence = ''

# 列表
def read_vocabulary():

    cur.execute("select * from english_vocabulary where `status` = 0 order by id asc limit 10")
    data = cur.fetchall()

    global translate_sentence
    item = ''
    for i,info in enumerate(data):

        # print i,info[0]

        # if i == 0:
        #     f.write('<p><br/></p>')

        i = i + 1

        if i < 10:
            i = '0' + str(i)

        item = data_vocabulary.replace('{{0}}', str(i))
        item = item.replace('{{1}}', info[2])
        item = item.replace('{{2}}', info[3])
        item = item.replace('{{3}}', info[4])
        item = item.replace('{{4}}', info[5])
        item = item.replace('{{5}}', info[6])

        if not translate_sentence and info[7]:

            translate_sentence = info[7]

        cur.execute("update english_vocabulary set `status` = 1 where `id` = %s", (info[0]))
        conn.commit()

        # print item
        f.write(item)

        # print i

# 读取日常英语 900 句
def read_sentence():

    cur.execute("select * from english_daily where `status` = 0 order by id asc limit 10")
    data = cur.fetchall()

    item = ''
    for i,info in enumerate(data):

        if i == 0:

            f.write('''
            <section label="Copyright © 2014 playhudong All Rights Reserved." donone="shifuMouseDownCard(&#39;shifu_c_014&#39;)" style="margin: 10px 0px 0px; padding: 16px; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; white-space: normal; border-width: 1px; border-style: dashed; border-color: rgb(183, 184, 184); border-radius: 10px; line-height: 1.4;">
            <p>
                <strong><span style="margin: 0px; padding: 0px; color: rgb(136, 136, 136);">九、Talking About Time 叙述时间</span></strong>
            </p>
            <p>
                <strong><span style="margin: 0px; padding: 0px; color: rgb(136, 136, 136);"><br/></span></strong>
            </p>''')

        item = data_sentence.replace('{{0}}', info[2])

        # print item
        f.write(item)

        cur.execute("update english_daily set `status` = 1 where `id` = %s", (info[0]))
        conn.commit()

        if i == 9:

            f.write('''
            </section>
            ''')

# 每日一句
def getSentence():

    f = open(u"read_day.txt")
    line = f.readline()

    i= 0
    data = []

    while line:

        if not line.strip():
            line = f.readline()
            continue

        if line.strip() == today:

            i = 1
            line = f.readline()
            continue

        if line.strip().isdigit():

            i = 0
            line = f.readline()
            continue

        if i == 0:

            line = f.readline()
            continue

        print line.strip()
        sub_arg = (line.strip())
        data.append(sub_arg)

        line = f.readline()

    return data

    f.close()

def main():

    # 开始
    f.write(data_begin)

    # 词汇
    read_vocabulary()

    # 日常英语 title
    f.write(data_sentence_title)

    # 日常英语
    read_sentence()

    sentence = getSentence()

    global  data_end
    # 结束
    # data_end = data_end.replace("{reply_password}", today_ymd)
    # data_end = data_end.replace("{translate_sentence}", translate_sentence)
    data_end = data_end.replace("{sentence_en}", sentence[0]).replace("{sentence_cn}", sentence[1])
    f.write(data_end)

    print 'SUCESS'

if __name__ == '__main__':

    main()