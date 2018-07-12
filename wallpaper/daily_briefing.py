# coding: utf-8

# ------------------------------------------------
#    功能：抓取每日简报
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

today = datetime.date.today().strftime("%Y-%m-%d")
today_m = datetime.date.today().strftime("%m")
today_d = datetime.date.today().strftime("%d")

title = '''
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <img class="" data-ratio="0.11875" data-src="https://mmbiz.qpic.cn/mmbiz_png/ULGBRicThgZu6e70gUKLbh6mHCCuACuynDQkvFSICRRuK9RlicP8q9kG1Sed5AGVnO0Q2y5hNH8bMAZKnzAPYxYQ/640?wx_fmt=png" data-type="png" data-w="640" title="https://image.ipaiban.com/upload-ueditor-image-20180706-1530852278672076937.png" src="https://image.ipaiban.com/upload-ueditor-image-20180709-1531110149086024850.jpg" data-fail="0" style="margin: 0px; padding: 0px; height: auto !important; width: auto !important; visibility: visible !important;"/>
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
                <span style="margin: 0px; padding: 0px; font-size: 20px;"><strong style="margin: 0px; padding: 0px;">英文科技简报</strong></span>
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
    <br style="margin: 0px; padding: 0px;"/>
</p>
<section class="" style="margin: 0px; padding: 0px; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <section class="" style="margin: 0px; padding: 1em 0.8em; font-size: 14px; letter-spacing: 1.5px; line-height: 1.75em; color: rgb(70, 70, 72); border-width: 1px; border-style: dotted; border-color: rgb(198, 198, 199);">
        <p style="margin-top: 0px; margin-bottom: 10px; padding: 0px; clear: both; min-height: 1em; letter-spacing: 0.5px; line-height: 1.75em;">
            <span style="margin: 0px; padding: 0px; font-size: 15px;"></span>{con}
        </p>
    </section>
</section>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 5px 5px 5px 10px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255); line-height: 0.6em; font-family: 微软雅黑; border-left: 3px solid rgb(255, 129, 36);">
    <strong style="margin: 0px; padding: 0px;">重点词汇</strong>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>'''
sentence = '''
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <span style="margin: 0px; padding: 0px; color: rgb(0, 112, 192);">{vocabulary_en}&nbsp;</span><span style="margin: 0px; padding: 0px; color: rgb(67, 149, 255);">&nbsp;</span>{translate_cn}
</p>
'''
con_line = '''
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
'''

con_end = '''
<p style="margin-top: 0px; margin-bottom: 10px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <img class="" data-ratio="0.015625" data-src="https://mmbiz.qpic.cn/mmbiz_png/ULGBRicThgZu6e70gUKLbh6mHCCuACuynvb0WTjFqNEU64aJicxjBEkmbic7wibuoNIInlnqONMVaV5ENgJDycyDvw/640?wx_fmt=png" data-type="png" data-w="640" title="https://image.ipaiban.com/upload-ueditor-image-20180706-1530852410133037157.png" src="https://image.ipaiban.com/upload-ueditor-image-20180709-1531110149297015569.png" data-fail="0" style="margin: 0px; padding: 0px; height: auto !important; width: auto !important; visibility: visible !important;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 10px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; white-space: normal; background-color: rgb(255, 255, 255); text-align: center;">
    <span style="margin: 0px; padding: 0px; font-family: Optima-Regular, PingFangTC-light;"><span style="margin: 0px; padding: 0px; font-size: 15px; letter-spacing: 0.544px;">有些事，只能一个人做</span></span>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; white-space: normal; background-color: rgb(255, 255, 255); text-align: center;">
    <span style="margin: 0px; padding: 0px; font-family: Optima-Regular, PingFangTC-light;"><span style="margin: 0px; padding: 0px; font-size: 15px; letter-spacing: 0.544px;">有些路，只能一个人走</span></span>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; white-space: normal; background-color: rgb(255, 255, 255); text-align: center;">
    <span style="margin: 0px; padding: 0px; font-family: Optima-Regular, PingFangTC-light;"><span style="margin: 0px; padding: 0px; font-size: 15px; letter-spacing: 0.544px;">发现找到英语的乐趣让</span></span>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; white-space: normal; background-color: rgb(255, 255, 255); text-align: center;">
    <span style="margin: 0px; padding: 0px; font-family: Optima-Regular, PingFangTC-light;"><span style="margin: 0px; padding: 0px; font-size: 15px; letter-spacing: 0.544px;">学习英语成为一种习惯</span></span>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; white-space: normal; background-color: rgb(255, 255, 255); text-align: center;">
    <span style="margin: 0px; padding: 0px; font-family: Optima-Regular, PingFangTC-light;"><span style="margin: 0px; padding: 0px; font-size: 15px; letter-spacing: 0.544px;"><br style="margin: 0px; padding: 0px;"/></span></span>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<section style="margin: 0px; padding: 0px; color: rgb(51, 51, 51); font-family: -apple-system-font, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: 17px; letter-spacing: 0.544px; text-align: justify; white-space: normal; background-color: rgb(255, 255, 255);">
    <section data-role="outer" label="Powered by 135editor.com" style="margin: 0px; padding: 0px;">
        <section class="" style="margin: 0px; padding: 0px; border-width: 0px; border-style: none; border-color: initial;">
            <section data-width="100%" style="margin: 0px; padding: 0px; width: 668px;">
                <section style="margin: 10px auto; padding: 0px; width: 300px;">
                    <section style="margin: 0px; padding: 0px; display: -webkit-flex;">
                        <section style="margin: 0px; padding: 0px; width: 185px;">
                            <section style="margin: 0px; padding: 0px; width: 185px;">
                                <img class="__bg_gif " data-ratio="0.5975" data-src="https://mmbiz.qpic.cn/mmbiz_gif/ULGBRicThgZu6e70gUKLbh6mHCCuACuyncG1Zr8dib8zydxE22PQ0fjn7XibwfvECKTyApqVgYcMQkBfibSc2gSJ2g/640?wx_fmt=gif" data-type="gif" data-w="400" data-width="100%" width="100%" _width="185px" src="https://image.ipaiban.com/upload-ueditor-image-20180709-1531110149356032051.gif" data-order="0" data-fail="0" style="margin: 0px; padding: 0px; display: block; height: auto !important; visibility: visible !important; width: 185px !important;"/>
                            </section>
                        </section>
                        <section style="margin: 0px 0px 0px 5px; padding: 0px; width: 110px;">
                            <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; width: 110px;">
                                <img class="" data-copyright="0" data-cropselx1="0" data-cropselx2="110" data-cropsely1="0" data-cropsely2="110" data-ratio="1" data-src="https://mmbiz.qpic.cn/mmbiz_jpg/ULGBRicThgZu6e70gUKLbh6mHCCuACuynLiahuFNzicDo2bicWfoAJdb1zT8cJEYH7eBXSrU1XicTTFaIbLTJQFky0g/640?wx_fmt=jpeg" data-type="jpeg" data-w="258" data-width="100%" title="https://image.ipaiban.com/upload-ueditor-image-20180706-1530852509371082537.jpg" width="110px" _width="110px" src="https://image.ipaiban.com/upload-ueditor-image-20180709-1531110149439091019.jpg" data-fail="0" style="margin: 0px; padding: 0px; display: block; height: auto !important; visibility: visible !important; width: 110px !important;"/>
                            </p>
                        </section>
                    </section>
                </section>
            </section>
        </section>
    </section>
</section>
<p></p>
'''
# 图片数组
img_arr = []

# 抓取简报
def crawl_article():

    url = 'https://technode.com/daily-briefing/'

    res = requests.get(url)

    if res.status_code == 200:

        res.close()
        res.encoding = 'utf-8'

        # print res.text
        soup = BeautifulSoup(res.text, 'lxml')

        html = soup.select(".main")[0]

        # print html

        name = html.select(".post-title")[0].get_text();
        date = html.select(".post-content > h2")[0].get_text();

        title_a = html.select(".post-content p")[0].get_text();
        content_a = html.select(".post-content p")[1].get_text();

        title_b = html.select(".post-content p")[3].get_text();
        content_b = html.select(".post-content p")[4].get_text();

        title_c = html.select(".post-content p")[6].get_text();
        content_c = html.select(".post-content p")[7].get_text();

        title_d = html.select(".post-content p")[9].get_text();
        content_d = html.select(".post-content p")[10].get_text();

        # print name
        # print date
        #
        # print title_a
        # print content_a
        #
        # print title_b
        # print content_b
        #
        # print title_c
        # print content_c
        #
        #
        #
        # print title_d
        # print content_d

        data = []
        sub_ary = (name,date,title_a+"\n\n"+content_a,title_b+"\n\n"+content_b,title_c+"\n\n"+content_c,title_d+"\n\n"+content_d)

        data.append(sub_ary)

        return data

# 翻译
def translate(con):

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

def main():

    # dir = os.path.abspath('.')
    # work_path = os.path.join(dir, 'Python-2.7.5.tar.bz2')

    # print dir
    # print work_path

    data = crawl_article()

    # print data

    i = 0
    content_read = ""
    content_vocabulary = [];word_arr = []
    article_con = ""
    for info in data[0]:

        # print i

        # print info

        if i > 1:

            result = translate(info)

            if result['errno'] == 0:

                # print info
                # print result['trans'][0]
                content_read = content_read + "\n\n" + str(i-1) + "." + info + "\n\n" + result['trans'][0]['dst'] + "\n\n" + result['trans'][1]['dst'] + "\n\n[相关词汇]\n\n"
                article_con = article_con + con.replace("{num}",str(i-1)).replace("{title}",result['trans'][0]['src']).replace("{con}",result['trans'][1]['src'])

                for wd in result['keywords']:

                    # print wd
                    content_read = content_read + wd['word'] + " " + ','.join(wd['means']) + "\n"
                    article_con = article_con + sentence.replace("{vocabulary_en}",wd['word']).replace("{translate_cn}",".".join(wd['means']))

                    cur.execute("select `word` from english_important_vocabulary where `word` = '"+wd['word']+"'")
                    get_info = cur.fetchone()

                    # print "select `word` from english_important_vocabulary where `word` = '%s'" % wd['word']
                    #
                    # print get_info

                    if get_info is None and not wd['word'] in word_arr:

                        sub_ary = (wd['word'],','.join(wd['means']))
                        content_vocabulary.append(sub_ary)
                        word_arr.append(wd['word'])

                article_con = article_con + con_line

        else:

            content_read = content_read + info + "\n\n"


        i = i+1
        # print result

    # print content_read

    # print content_vocabulary
    # 文章
    rowcount = cur.execute(
        'INSERT INTO english_science_read (`content`) values(%s)', content_read)
    conn.commit()

    # 词汇
    rowcount = cur.executemany(
        'INSERT INTO english_important_vocabulary (`word`,`interpret`) values(%s,%s)', content_vocabulary)
    conn.commit()

    # 写入文件
    txt_name = 'daily_briefing_' + today + ".txt"
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