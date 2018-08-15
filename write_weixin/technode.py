# coding: utf-8

# ------------------------------------------------
#    功能：抓取每日简报、资讯
#    地址：https://technode.com/tag/news/
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
import urllib2
import datetime
import os
import re
import unicodedata
import json
import sys
import unicodedata

reload(sys)

sys.setdefaultencoding('utf-8')

HOSTNAME = '127.0.0.1'
USERNAME = 'root'
PASSWORD = ''
DATABASE = 'pydata'

conn = pymysql.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE, charset="utf8")
cur = conn.cursor()

today = datetime.date.today().strftime("%Y-%m-%d")
today_m = datetime.date.today().strftime("%m")
today_d = datetime.date.today().strftime("%d")
today_str = datetime.date.today().strftime("%Y/%m/%d")
# today_str = "2018/08/01";
#昨天
yesterday=(datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y/%m/%d")
# print yesterday.strftime("%Y/%m/%d")

title = '''
<p style="text-align:center">
    <img class="" data-ratio="0.11875" data-src="https://mmbiz.qpic.cn/mmbiz_jpg/ULGBRicThgZvPDhSic2eliclib6tNzP3zNKIIgIq4mShd7e0gKcYVibcenbEYfgGqoD7xw8oq7d8g9b9rqHFujiaQzuw/640?wx_fmt=jpeg&amp;tp=webp&amp;wxfrom=5&amp;wx_lazy=1" data-type="png" data-w="640" title="https://mmbiz.qpic.cn/mmbiz_jpg/ULGBRicThgZvPDhSic2eliclib6tNzP3zNKIIgIq4mShd7e0gKcYVibcenbEYfgGqoD7xw8oq7d8g9b9rqHFujiaQzuw/640?wx_fmt=jpeg&amp;tp=webp&amp;wxfrom=5&amp;wx_lazy=1" src="https://mmbiz.qpic.cn/mmbiz_jpg/ULGBRicThgZvPDhSic2eliclib6tNzP3zNKIIgIq4mShd7e0gKcYVibcenbEYfgGqoD7xw8oq7d8g9b9rqHFujiaQzuw/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1" data-fail="0" style="margin: 0px; padding: 0px; height: auto !important; width: auto !important; visibility: visible !important;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<section class="" style="margin: 0px; padding: 0px; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <section style="margin: 0px; padding: 0px; width: 670px; display: -webkit-flex; justify-content: center;">
        <section style="margin: 0px; padding: 0px; width: 30px;">
            <section style="margin: 0px; padding: 0px; width: 30px; background-color: rgb(225, 133, 1);">
                <img class="" data-ratio="0.9814814814814815" data-src="https://mmbiz.qpic.cn/mmbiz_png/ULGBRicThgZu6e70gUKLbh6mHCCuACuynp8thxwG3mrgUibwuAKkO1sYsTHfENibR8kfuwV3FZOmSMoib20KaI5FAw/640?wx_fmt=png" data-type="png" data-w="54" width="100%" _width="30px" src="https://image.ipaiban.com/upload-ueditor-image-20180709-1531110149158074891.png" data-fail="0" style="margin: 0px; padding: 0px; display: block; height: auto !important; visibility: visible !important; width: 30px !important;"/>
            </section>
        </section>
        <section style="margin: 0px 5px; padding: 0px;">
            <section style="margin: 0px; padding: 0px 15px; line-height: 30px; color: rgb(255, 255, 255); background-color: rgb(225, 133, 1);">
                <span style="margin: 0px; padding: 0px; font-size: 20px;"><strong style="margin: 0px; padding: 0px;">英文简报</strong></span>
            </section>
        </section>
        <section style="margin: 0px; padding: 0px; width: 30px;">
            <section style="margin: 0px; padding: 0px; width: 30px; background-color: rgb(225, 133, 1);">
                <img class="" data-ratio="0.9814814814814815" data-src="https://mmbiz.qpic.cn/mmbiz_png/ULGBRicThgZu6e70gUKLbh6mHCCuACuynicN2ZebSp2DQn93icSiaiavLf88SdM08Lre7Bd6BNzyTUfkUoIxiczrO1gA/640?wx_fmt=png" data-type="png" data-w="54" width="100%" _width="30px" src="https://image.ipaiban.com/upload-ueditor-image-20180709-1531110149230026104.png" data-fail="0" style="margin: 0px; padding: 0px; display: block; height: auto !important; visibility: visible !important; width: 30px !important;"/>
            </section>
        </section>
    </section>
</section>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br/>
</p>
<section class="" style="margin: 0px; padding: 0px; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <section data-by="96weixin" style="margin: 0px; padding: 0px;">
        <section style="margin: 10px 0px; padding: 0px; text-align: center;">
            <section style="margin: 0px; padding: 2px 6px 6px; color: rgb(255, 255, 255); display: inline-block; vertical-align: top; min-width: 4.5em; border-radius: 0.6em; background-color: rgb(255, 129, 36);">
                '''+today_m+'''月
                <section style="margin: 0px; padding: 0px; border-radius: 0.3em; font-size: 28px; line-height: 1.3em; color: rgb(255, 129, 36); background-color: rgb(255, 255, 255);">
                    '''+today_d+'''
                </section>
            </section>
        </section>
    </section>
</section>
<section class="" data-tools="135编辑器" data-id="85640" data-color="#ff8124" data-custom="#ff8124" style="margin: 0px; padding: 0px; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <p style="margin-top: 0px; margin-bottom: 0px; padding: 2px 0px 0px 40px; clear: both; min-height: 1em; line-height: normal;">
        <br/>
    </p>
</section>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
'''

#句子
con = '''
<section class="" data-color="#ff8124" data-custom="#ff8124" style="margin: 0px; padding: 0px; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <section style="margin: 0px; padding: 0px; display: inline-block; float: left; color: rgb(255, 255, 255); border-color: rgb(255, 129, 36); background-color: rgb(255, 129, 36);">
        <section style="margin: 0px; padding: 5px 8px; display: inline-block; vertical-align: middle; color: inherit;">
            <section style="margin: 0px; padding: 0px; color: inherit;">
                <strong style="margin: 0px; padding: 0px; color: inherit;">{num}</strong>
            </section>
        </section>
    </section>
    <section style="margin: 8px 0px 0px; padding: 0px; border-left: 8px solid rgb(255, 129, 36); border-right-width: 0px; border-right-color: rgb(255, 129, 36); display: inline-block; float: left; color: inherit; border-bottom: 8px solid transparent !important; border-top: 8px solid transparent !important;"></section>
    <section style="margin: 0px; padding: 2px 0px 0px 40px; font-size: 18px;">
        <span style="margin: 0px; padding: 0px; font-family: 微软雅黑; color: rgb(62, 62, 62); font-size: 16px;">{title}</span>
    </section>
</section>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <span style="font-size: 14px; color: rgb(216, 216, 216);">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<em>{con}</em></span>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>'''

#重点词汇
sentence = '''
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <span style="margin: 0px; padding: 0px; color: rgb(0, 112, 192);">{vocabulary_en}&nbsp;</span><span style="margin: 0px; padding: 0px; color: rgb(67, 149, 255);">&nbsp;</span>{translate_cn}
</p>
'''

#空格
con_line = '''
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
'''

#词汇
sentence_fanyi = '''
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 5px 5px 5px 10px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255); line-height: 0.6em; font-family: 微软雅黑; border-left: 3px solid rgb(255, 129, 36);">
    <strong style="margin: 0px; padding: 0px;">重点词汇</strong>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
'''

today_news = '''
<section style="width:98%;
border:none;
border-style:none;
margin:0rem auto;" id="shifu_qmi_005" donone="shifuMouseDownPayStyle(&#39;shifu_qmi_005&#39;)">
    <section style="padding: 0.625rem 0px; text-align: center;">
        <section style="
display:inline-block;">
            <section style="text-align: center; letter-spacing: 1.5px; line-height: 1.75em; padding: 0px 6px 0px 12px;">
                <p style="">
                    <span style="color:#262626"><span style="font-size: 18px;"><strong>今日动态/News today</strong></span></span>
                </p>
            </section>
            <section style="
display:flex;
justify-content:center;align-items:center;
margin-top:-6px;">
                <section style="width: 8px; height: 8px; border-radius: 100%; border: 1px solid rgb(225, 133, 1);"></section>
                <section style="width:100%;">
                    <section class="ipaiban-bg" style="width:100%;
height:1px;
background:rgb(225, 133, 1);"></section>
                </section>
                <section style="width: 8px; height: 8px; border-radius: 100%; border: 1px solid rgb(225, 133, 1);" class="ipaiban-bc">
                    <br/>
                </section>
            </section>
        </section>
    </section>
</section>
'''

yesterday_news = '''
<section style="width:98%;
border:none;
border-style:none;
margin:0rem auto;" id="shifu_qmi_005" donone="shifuMouseDownPayStyle(&#39;shifu_qmi_005&#39;)">
    <section style="padding: 0.625rem 0px; text-align: center;">
        <section style="
display:inline-block;">
            <section style="letter-spacing: 1.5px; line-height: 1.75em; padding: 0px 6px 0px 12px;">
                <p>
                    <span style="color:#262626"><span style="font-size: 18px;"><strong>昨日动态/News yesterday</strong></span></span>
                </p>
            </section>
            <section style="
display:flex;
justify-content:center;align-items:center;
margin-top:-6px;">
                <section style="width: 8px; height: 8px; border-radius: 100%; border: 1px solid rgb(225, 133, 1);"></section>
                <section style="width:100%;">
                    <section class="ipaiban-bg" style="width:100%;
height:1px;
background:rgb(225, 133, 1);"></section>
                </section>
                <section style="width: 8px; height: 8px; border-radius: 100%; border: 1px solid rgb(225, 133, 1);" class="ipaiban-bc">
                    <br/>
                </section>
            </section>
        </section>
    </section>
</section>
'''

con_end = '''
<p style="margin-top: 0px; margin-bottom: 0px; padding: 5px 5px 5px 10px; clear: both; white-space: normal; min-height: 1em; color: rgb(51, 51, 51); font-size: 17px; letter-spacing: 0.544px; text-align: justify; background-color: rgb(255, 255, 255); line-height: 0.6em; font-family: 微软雅黑; border-left: 3px solid rgb(255, 129, 36);">
    <strong style="margin: 0px; padding: 0px;">精选阅读</strong>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483852&idx=1&sn=5e91555bbc075738ca2b675309431f84&chksm=fcde92a5cba91bb3a3839a50daf70e052ab5f45a61903f930a080cbd942d51c2a76c76aa50e6&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;"></a>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483897&idx=2&sn=558dac52bb6ff59656c76a96973ef4c5&chksm=fcde9290cba91b863d86c3d41efb17699cf1fe4a2a94a895b9ce9bd188ba24679231866f06eb&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【词汇】英语词汇第22课</a><br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483811&idx=4&sn=1ce07da4a5c6a5fceadf35c401b520ee&chksm=fcde92cacba91bdcc54b1c5360ce2caa40e39e36d309cca76b80c7fa432b1efb5c41c8f218e0&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【福利】更新《剑指offer秋招笔记》资料直接下载</a><br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483801&idx=4&sn=f67da2b252d54d9619c4b9e7d57296b4&chksm=fcde92f0cba91be6dd505ed27e1f672e3d281aacd457be4695b8cee442d34d086beb15e31e96&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【福利】资料 | 一份收藏量超过两万多的计算机科学学习笔记</a><br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483819&idx=4&sn=d8a869c37694def2f10b0c70b1ea0629&chksm=fcde92c2cba91bd4d6a84c62ba75a13034f8e0c466baf7989ae95055ac6bfa0366ee19279a7a&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(87, 107, 149); text-decoration-line: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);">【福利】20的多个实用小工具 快速提升你的工作效率</a>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483783&idx=4&sn=20d9f2eca2ceb1be374786ec381f8044&chksm=fcde92eecba91bf8228fa112188b5bef4c0fb3c0ba748ad15d7a8cd0452aba329ce144ad28cd&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【福利】英语视频教程免费发放</a>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483697&idx=1&sn=2209a5aeadb4a26b6d5d3607fc419cdb&chksm=fcde9258cba91b4e7d3a6fecbfd784a470ced0f85226904aae25af4ebdcd4ef54170a5606378&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(87, 107, 149); text-decoration-line: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);">【英语】为什么我们要学习英语？</a>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483661&idx=1&sn=44213e9fcd9d19ba54843bbff3f8e720&chksm=fcde9264cba91b72ce573929626d597407b1f466d9dd18faf148bd4dee42c6a4f03fa263939a&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(87, 107, 149); text-decoration-line: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);">【英语】如何学英语，看看这位同学的总结</a>
</p>
<p style="margin-top: 0px; margin-bottom: 10px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <br/>
</p>
<p style="margin-top: 0px; margin-bottom: 10px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <img class="" data-ratio="0.015625" src="https://image.ipaiban.com/upload-ueditor-image-20180717-1531843096238046776.png" data-type="png" data-w="640" title="https://image.ipaiban.com/upload-ueditor-image-20180706-1530852410133037157.png" style="margin: 0px; padding: 0px; height: auto !important; width: auto !important; visibility: visible !important;"/>
</p>
<section label="Copyright Reserved by PLAYHUDONG." donone="shifuMouseDownCard(&#39;shifu_c_007&#39;)" style="margin: 1em auto; padding: 0px; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; border-style: none;">
    <section style="margin: 0px; padding: 16px; line-height: 2.4;">
        <span class="color" style="margin: 0px 5px 0px 0px; padding: 0px; font-size: 3em; line-height: 1em; font-weight: bolder; vertical-align: middle; text-align: center;">“</span>认知决定你的人生格局，处事决定你的人生高度。提高认知，从认知的漏斗里爬出来，不做观天于井的青蛙，而是迎着命运，接受自我，于智慧的巅峰，看大千纷纭，观落英缤纷，美丽的世界，源自于美丽的人生，源自于豁达通明的认知，源自于不懈向上的娴静心境。<span class="color" style="margin: 0px 0px 0px 5px; padding: 0px; font-size: 3em; line-height: 1em; font-weight: bolder; vertical-align: middle; text-align: center;">”</span>
    </section>
    <section style="margin: 0px; padding: 5px; border-width: 1px; border-style: dashed; border-color: rgb(121, 121, 121);">
        <section label="Copyright © 2016 playhudong All Rights Reserved." donone="shifuMouseDownPayStyle(&#39;shifu_sig_025&#39;)" style="margin: 0px auto; padding: 0px; border-width: initial; border-style: none; border-color: initial; width: 20em;">
            <section style="margin: 0px; padding: 0px; width: 320px; text-align: center; font-size: 1em; line-height: 1.5em;">
                <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both;">
                    想了解更多最新信息？
                </p>
            </section>
            <section style="margin: 1em 0px; padding: 0px; width: 320px; text-align: center;">
                <img class="lazy" data-copyright="0" data-cropselx1="0" data-cropselx2="160" data-cropsely1="0" data-cropsely2="160" data-ratio="1" src="https://image.ipaiban.com/upload-ueditor-image-20180717-1531843096403063706.jpg" data-type="jpeg" data-w="344" style="margin: 0px; padding: 0px; height: 160px; width: 160px; display: inline;"/>
            </section>
            <section class="ipaiban" style="margin: 0px; padding: 0px; width: 320px; border-top: 2px solid rgb(253, 208, 39); text-align: center;">
                <section class="xhr" style="margin: 0px; padding: 0px; display: inline-block; background: rgb(253, 208, 39);">
                    <section style="margin: 0px 0.5em 0px 0px; padding: 0px; width: 0px; height: 0px; float: left; display: inline-block; border-top: 1.6em solid transparent; border-left: 0.5em solid rgb(255, 255, 255);"></section>
                    <section style="margin: 0px; padding: 0px; width: auto; font-size: 0.875em; line-height: 1em; color: rgb(255, 255, 255); display: inline-block;">
                        <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both;">
                            长按二维码 关注我们
                        </p>
                    </section>
                    <section style="margin: 0px 0px 0px 0.5em; padding: 0px; width: 0px; height: 0px; float: right; display: inline-block; border-top: 1.6em solid transparent; border-right: 0.5em solid rgb(255, 255, 255);"></section>
                </section>
            </section>
            <section style="margin: 1em 0px 0px; padding: 0px; width: 320px; text-align: center; font-size: 1em; line-height: 1.5em;">
                <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both;">
                    有问题请联系小编<br style="margin: 0px; padding: 0px;"/>微信ID：<br style="margin: 0px; padding: 0px;"/>hailuotoutiao
                </p>
            </section>
        </section>
    </section>
    <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); text-align: center;">
        <span style="margin: 0px; padding: 0px; color: rgb(178, 178, 178); font-size: 12px;">✬如果你喜欢这篇文章，欢迎分享到朋友圈✬</span><br style="margin: 0px; padding: 0px;"/>
    </p>
    <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); text-align: center;">
        <span style="margin: 0px; padding: 0px; font-size: 12px; color: rgb(178, 178, 178);">评论功能现已开启，我们接受一切形式的吐槽和赞美</span>
    </p>
</section>
'''
# 图片数组
img_arr = []

# 抓取简报
def crawl_article(url):

    if not url:
        url = 'https://technode.com/tag/news/'

    res = requests.get(url)

    if res.status_code == 200:

        res.close()
        res.encoding = 'utf-8'

        # print res.text

        soup = BeautifulSoup(res.text, 'lxml')

        html = soup.select(".isotope-container")[0]

        # print html

        sub_data = [];
        sub_data_yesterday = [];
        # name = "DAILY BRIEFING";
        # date = today;
        # sub_ary = (name, date);
        # sub_data.append(sub_ary);
        title = "";excerpt = "";url = "";

        data = html.select(".tmb-post");

        for info in data:

            # print info
            # print info.find("h2").find("a")['href']

            url = info.select(".t-entry h3")[0].find("a")["href"]

            if today_str in url:
                title = info.select(".t-entry .t-entry-title a")[0].get_text()
                # excerpt = info.select(".post-excerpt")[0].get_text()

                sub_ary = (title)
                sub_data.append(sub_ary)
                # print sub_data

            # print title
            # print url

            if yesterday in url:
                title = info.select(".t-entry .t-entry-title a")[0].get_text()
                # excerpt = info.select(".post-excerpt")[0].get_text()

                sub_ary = (title)
                sub_data_yesterday.append(sub_ary)


        # print sub_data
        # exit()

        return sub_data,sub_data_yesterday

# 翻译
def translate(con):

    if not con:

        return

    # 手机版百度翻译
    url = 'http://fanyi.baidu.com/basetrans'

    headers = {
        # 手机浏览器的UA
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"
    }

    # 构造post请求的data
    # word = input('请输入您要查询的单词：')
    data = {
        'from': 'en',
        'to': 'zh',
        'query': con,
    }
    data = urllib.urlencode(data).encode('utf-8')

    req = urllib2.Request(url=url, headers=headers, data=data)

    response = urllib2.urlopen(req)
    # print(response.read().decode('utf-8'))

    result = json.loads(response.read())

    # print result['errno']
    #
    # print result['trans'][0]['dst']

    # print result.json()

    # print result
    return result

# 生成文章
def generate():

    #定义
    i = 1;
    num = ""; title = ""; title_cn = ""
    article_con = ""

    article_con = today_news

    cur.execute("select * from english_technode where `create_date` = %s", today)
    data = cur.fetchall();

    cur.execute("select * from english_technode where `create_date` < %s order by id desc limit 10", today)
    data2 = cur.fetchall();

    cur.execute("select * from english_important_vocabulary where `addtime` >= %s limit 15", today)
    data3 = cur.fetchall();

    # today news
    for info in data:

        num = i
        num = str(num)
        title = info[1]
        title = unicodedata.normalize('NFKD', title).encode('ascii','ignore')
        title_cn = info[2]
        # title_cn = unicodedata.normalize('NFKD', title_cn).encode('ascii', 'ignore')
        # print title_cn

        article_con = article_con + con.replace("{num}",num).replace("{title}",title).replace("{con}", title_cn);

        i = i + 1

    article_con = article_con + yesterday_news

    # yesterday news
    i = 1
    for info in data2:

        num = i
        num = str(num)
        title = info[1]
        title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')
        title_cn = info[2]
        # title_cn = unicodedata.normalize('NFKD', title_cn).encode('ascii', 'ignore')
        # print title_cn

        article_con = article_con + con.replace("{num}", num).replace("{title}", title).replace("{con}", title_cn);

        i = i + 1

    article_con = article_con + sentence_fanyi

    # important vocabulary
    i = 1
    for info in data3:

        num = i
        num = str(num)
        title = info[1]
        title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')
        title_cn = info[2]
        # title_cn = unicodedata.normalize('NFKD', title_cn).encode('ascii', 'ignore')
        # print title_cn

        article_con = article_con + sentence.replace("{vocabulary_en}",title).replace("{translate_cn}",title_cn)

        i = i + 1

    article_con = article_con + con_line

    return article_con

def main():

    # dir = os.path.abspath('.')
    # work_path = os.path.join(dir, 'Python-2.7.5.tar.bz2')

    # print dir
    # print work_path

    data_new,data_new_yesterday = crawl_article('')
    data_brief,data_brief_yesterday = crawl_article("https://technode.com/tag/daily-briefing/")

    data = data_new + data_brief
    data_yesterday = data_new_yesterday + data_brief_yesterday

    # print data
    # print data_yesterday
    #
    # exit()

    i = 1
    sub_read = ""
    content_read = []
    content_vocabulary = [];word_arr = []
    article_con = ""
    for info in data:

        # print i

        # print info

        if info:

            # print info
            # info = info.replace("\n\n","")

            result = translate(info)

            if result['errno'] == 0:


                # print info
                # print result['trans'][0]

                # 查询是不是已经存在
                cur.execute("select * from english_technode where `en` = %s", info)
                get_read = cur.fetchone()

                if get_read is None:

                    sub_read = (info, result['trans'][0]['dst'], today)
                    content_read.append(sub_read)
                # content_read = content_read + "\n\n" + str(i) + "." + info + "\n\n" + result['trans'][0]['dst'] + "\n\n" + result['trans'][1]['dst'] + "\n\n[相关词汇]\n\n"
                # article_con = article_con + con.replace("{num}",str(i)).replace("{title}",result['trans'][0]['src']).replace("{con}",result['trans'][1]['src'])

                #句子翻译
                # article_con = article_con + sentence_fanyi.replace("{fanyi_content}",result['trans'][0]['dst']+"<br/>"+result['trans'][1]['dst']);

                for wd in result['keywords']:

                    #查询是不是已经存在
                    cur.execute("select `word`,`interpret` from english_important_vocabulary where `word` = '"+wd['word']+"'")
                    get_info = cur.fetchone()

                    if get_info is None and not wd['word'] in word_arr:

                        sub_ary = (wd['word'],','.join(wd['means']))
                        content_vocabulary.append(sub_ary)
                        word_arr.append(wd['word'])

                        # #新翻译词汇
                        # content_read = content_read + wd['word'] + " " + ','.join(wd['means']) + "\n"
                        # article_con = article_con + sentence.replace("{vocabulary_en}",wd['word']).replace("{translate_cn}",".".join(wd['means']))

                    # else:

                        #存在，则读取数据库中的内容
                        # interpret = get_info[1];
                        # interpret_str = unicodedata.normalize('NFKD', interpret).encode('ascii','ignore') # unicode 转 str
                        # print interpret
                        # print type(interpret_str)
                        # print interpret_str
                        # wd['means'] = interpret_str.split(",")

                        # print wd
                        # content_read = content_read + wd['word'] + " " + interpret + "\n"
                        # article_con = article_con + sentence.replace("{vocabulary_en}",wd['word']).replace("{translate_cn}",interpret)

                    # print "select `word` from english_important_vocabulary where `word` = '%s'" % wd['word']
                    #
                    # print get_info

                # article_con = article_con + con_line

        # print result

    # print content_read

    # print content_vocabulary
    # 文章
    # print content_read
    rowcount = cur.executemany(
        'INSERT INTO english_technode (`en`,`cn`,`create_date`) values(%s,%s,%s)', content_read)
    conn.commit()

    # 词汇
    # print content_vocabulary
    rowcount = cur.executemany(
        'INSERT INTO english_important_vocabulary (`word`,`interpret`) values(%s,%s)', content_vocabulary)
    conn.commit()

    #调用数据
    article_con = generate()

    # 写入文件
    txt_name = 'daily_technode_' + today + ".txt"
    f = open(txt_name, "a+")
    f.truncate()

    f.write(title)

    f.write(article_con)

    f.write(con_end)

    f.close()

    print "SUCCESS"

    cur.close()
    conn.close()

if __name__ == '__main__':

    main()