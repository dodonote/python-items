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
import unicodedata
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
sentence_fanyi = '''
<section class="" style="margin: 0px; padding: 0px 10px; font-size: 14px; color: rgb(249, 110, 87); line-height: 1.8;">
    <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em; text-align: center;">
        （点击下面空白处 查看翻译）
    </p>
</section>
<section label="Copyright © 2017 playhudong All Rights Reserved." style="
border-width: 1px; border-style: dotted; border-color: rgb(198, 198, 199);
margin:0rem auto;height:50px;line-height:35px;overflow:auto;" id="shifu_flo_001" donone="shifuMouseDownPayStyle(&#39;shifu_flo_001&#39;)">
    <section style="
overflow:hidden;">
        <section style="width:100%;
text-align: left;
padding: 0rem 1rem;
box-sizing: border-box;
font-size: 0.875rem;
line-height: 1.5;
height:auto;
overflow:hidden;
color: #000;">
            <p style="margin:0">
                {fanyi_content}
            </p>
        </section>
        <svg style="width:100%;
height:40rem;
margin-top:-40rem;
" data-ipaiban-svg="style中的height、margin-top和rect标签中的height的高度保持一致">
            <rect style="width:100%;
height:40rem;
fill: #fff;">
                <animate attributename="opacity" begin="click" data-ipaiban-begin="begin可以写0s（秒数）或者click（点击触发）" dur="3s" data-ipaiban-dur="dur写几秒，动画就持续执行几秒" from="1" data-ipaiban-from="from写0~1，透明度就是从几开始" to="0" data-ipaiban-to="to写0~1，0为完全透明" fill="freeze" data-ipaiban-fill="fill指是否还原初始状态，freeze为不恢复"></animate>
            </rect>
        </svg>
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
</p>
'''
con_end = '''
<p style="margin-top: 0px; margin-bottom: 0px; padding: 5px 5px 5px 10px; clear: both; white-space: normal; min-height: 1em; color: rgb(51, 51, 51); font-size: 17px; letter-spacing: 0.544px; text-align: justify; background-color: rgb(255, 255, 255); line-height: 0.6em; font-family: 微软雅黑; border-left: 3px solid rgb(255, 129, 36);">
    <strong style="margin: 0px; padding: 0px;">精选阅读</strong>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483852&idx=1&sn=5e91555bbc075738ca2b675309431f84&chksm=fcde92a5cba91bb3a3839a50daf70e052ab5f45a61903f930a080cbd942d51c2a76c76aa50e6&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【简报】陌陌入局短视频，“谁说”究竟剑指何方？ —Pingwest</a><br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483852&idx=2&sn=e601334576e1b0306df8e2bae7f859cb&chksm=fcde92a5cba91bb31b52a4d8676021a94cda76ec4db632bd9f32dec58b99f50f103b9c16168f&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【词汇】英语四六级/考研词汇第十六课</a><br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483852&idx=3&sn=13a41253e2c8894359117ca0e43aae9e&chksm=fcde92a5cba91bb3b8809e0ee92479fb991adb4ea684c4c36ef4dbb880b5bb545921e30ffed8&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【阅读】A FAMILY OF WITCHES &nbsp;巫师之家</a><br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483819&idx=4&sn=d8a869c37694def2f10b0c70b1ea0629&chksm=fcde92c2cba91bd4d6a84c62ba75a13034f8e0c466baf7989ae95055ac6bfa0366ee19279a7a&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(87, 107, 149); text-decoration-line: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);">【福利】20的多个实用小工具 快速提升你的工作效率</a>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483697&idx=1&sn=2209a5aeadb4a26b6d5d3607fc419cdb&chksm=fcde9258cba91b4e7d3a6fecbfd784a470ced0f85226904aae25af4ebdcd4ef54170a5606378&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(87, 107, 149); text-decoration-line: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);">【英语】为什么我们要学习英语？</a>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483661&idx=1&sn=44213e9fcd9d19ba54843bbff3f8e720&chksm=fcde9264cba91b72ce573929626d597407b1f466d9dd18faf148bd4dee42c6a4f03fa263939a&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(87, 107, 149); text-decoration-line: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);">【英语】如何学英语，看看这位同学的总结</a>
</p>
<p style="margin-top: 0px; margin-bottom: 10px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 10px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em; color: rgb(51, 51, 51);">
    <img class="" data-ratio="0.015625" src="https://image.ipaiban.com/upload-ueditor-image-20180717-1531843096238046776.png" data-type="png" data-w="640" title="https://image.ipaiban.com/upload-ueditor-image-20180706-1530852410133037157.png" style="margin: 0px; padding: 0px; height: auto !important; width: auto !important; visibility: visible !important;"/>
</p>
<p></p>
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
def crawl_article():

    url = 'https://technode.com/daily-briefing/'

    res = requests.get(url)

    if res.status_code == 200:

        res.close()
        res.encoding = 'utf-8'

        # print res.text
        soup = BeautifulSoup(res.text, 'lxml')

        html = soup.select(".qodef-page-content-holder")[0]

        # print html

        name = "daily briefing";
        date = html.select("h2")[0].get_text();

        title_a = html.select("p")[0].get_text();
        content_a = html.select("p")[1].get_text();

        title_b = html.select("p")[3].get_text();
        content_b = html.select("p")[4].get_text();

        title_c = html.select("p")[6].get_text();
        content_c = html.select("p")[7].get_text();

        title_d = html.select("p")[9].get_text();
        content_d = html.select("p")[10].get_text();

        title_e = html.select("p")[12].get_text();
        content_e = html.select("p")[13].get_text();

        title_f = html.select("p")[15].get_text();
        content_f = html.select("p")[16].get_text();

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
        sub_ary = (name,date,title_a+"\n\n"+content_a,title_b+"\n\n"+content_b,title_c+"\n\n"+content_c,title_d+"\n\n"+content_d,title_e+"\n\n"+content_e,title_f+"\n\n"+content_f)

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

        if i > 1 and info:

            result = translate(info)

            if result['errno'] == 0:

                # print info
                # print result['trans'][0]
                content_read = content_read + "\n\n" + str(i-1) + "." + info + "\n\n" + result['trans'][0]['dst'] + "\n\n" + result['trans'][1]['dst'] + "\n\n[相关词汇]\n\n"
                article_con = article_con + con.replace("{num}",str(i-1)).replace("{title}",result['trans'][0]['src']).replace("{con}",result['trans'][1]['src'])

                #句子翻译
                article_con = article_con + sentence_fanyi.replace("{fanyi_content}",result['trans'][0]['dst']+"<br/>"+result['trans'][1]['dst']);

                for wd in result['keywords']:

                    #查询是不是已经存在
                    cur.execute("select `word`,`interpret` from english_important_vocabulary where `word` = '"+wd['word']+"'")
                    get_info = cur.fetchone()

                    if get_info is None and not wd['word'] in word_arr:

                        sub_ary = (wd['word'],','.join(wd['means']))
                        content_vocabulary.append(sub_ary)
                        word_arr.append(wd['word'])

                        #新翻译词汇
                        content_read = content_read + wd['word'] + " " + ','.join(wd['means']) + "\n"
                        article_con = article_con + sentence.replace("{vocabulary_en}",wd['word']).replace("{translate_cn}",".".join(wd['means']))

                    else:

                        #存在，则读取数据库中的内容
                        interpret = get_info[1];
                        interpret_str = unicodedata.normalize('NFKD', interpret).encode('ascii','ignore') # unicode 转 str
                        # print interpret
                        # print type(interpret_str)
                        # print interpret_str
                        # wd['means'] = interpret_str.split(",")

                        # print wd
                        content_read = content_read + wd['word'] + " " + interpret + "\n"
                        article_con = article_con + sentence.replace("{vocabulary_en}",wd['word']).replace("{translate_cn}",interpret)

                    # print "select `word` from english_important_vocabulary where `word` = '%s'" % wd['word']
                    #
                    # print get_info

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