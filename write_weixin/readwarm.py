# coding: utf-8
# ------------------------------------------------
#    作用：从数据库读取公众号信息 阅读
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

data_begin = '''
<section class="color" style="margin: 0px; padding: 0px; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <img class="" data-copyright="0" data-ratio="0.75" src="https://image.ipaiban.com/upload-ueditor-image-20180619-1529341445238095226.gif" data-type="gif" data-w="700" style="margin: 0px; padding: 0px; height: auto !important;"/><br style="margin: 0px; padding: 0px;"/>
</section>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p>
    <br/>
</p>
<section class="output_wrapper" style="margin: 0px; padding: 0px; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; letter-spacing: 0px; white-space: normal; color: rgb(62, 62, 62); line-height: 1.6;">
    <section class="" style="margin: 0px; padding: 0px; font-size: inherit; line-height: inherit; display: inline-block; vertical-align: top; width: 72.5313px; border-style: solid; border-width: 1px; border-radius: 0px; border-color: rgb(178, 178, 178); color: rgb(178, 178, 178);">
        <section class="Powered-by-XIUMI V5" powered-by="xiumi.us" style="margin: 0px; padding: 0px; font-size: inherit; color: inherit; line-height: inherit;">
            <section class="" style="margin: 0px; padding: 0px; font-size: inherit; color: inherit; line-height: inherit;">
                <section class="" style="margin: 0px; padding: 0px; font-size: inherit; color: inherit; text-align: center; line-height: 18px;">
                    <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-size: inherit; color: inherit; line-height: inherit;">
                        15
                    </p>
                    <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-size: inherit; color: inherit; line-height: inherit;">
                        ／
                    </p>
                    <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-size: inherit; color: inherit; line-height: inherit;">
                        06
                    </p>
                </section>
            </section>
        </section>
    </section>
    <section class="" style="margin: 0px; padding: 0px 0px 0px 10px; font-size: inherit; color: inherit; line-height: inherit; display: inline-block; vertical-align: top;">
        <section class="Powered-by-XIUMI V5" powered-by="xiumi.us" style="margin: 0px; padding: 0px; font-size: inherit; color: inherit; line-height: inherit;">
            <section class="" style="margin: 0px; padding: 0px; font-size: inherit; color: inherit; line-height: inherit;">
                <section class="" style="margin: 0px; padding: 0px; color: inherit; font-size: 15px; line-height: 26px;">
                    <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-size: inherit; color: inherit; line-height: inherit;">
                        <span style="margin: 0px; padding: 0px; font-size: inherit; line-height: inherit; color: rgb(178, 178, 178);">Visit</span><span style="margin: 0px; padding: 0px; font-size: inherit; line-height: inherit; color: rgb(178, 178, 178);">&nbsp;to Australia</span>
                    </p>
                    <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-size: inherit; color: inherit; line-height: inherit;">
                        <span style="margin: 0px; padding: 0px; font-size: inherit; line-height: inherit; color: rgb(178, 178, 178);">访</span><span style="margin: 0px; padding: 0px; font-size: inherit; line-height: inherit; color: rgb(178, 178, 178);">问澳大利亚</span>
                    </p>
                </section>
            </section>
        </section>
    </section>
</section>
<p>
    <br/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
'''

data_end = '''
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <span style="margin: 0px; padding: 0px; color: rgb(255, 169, 0);">未完待续.....<br style="margin: 0px; padding: 0px;"/></span>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p>
    <br/>
</p>
<section class="" data-tools="" data-id="91558" style="margin: 0px; padding: 0px; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; color: rgb(51, 51, 51);">
    <section data-role="paragraph" class="" style="margin: 0px; padding: 0px; border-width: 0px; border-style: none; border-color: initial;">
        <section style="margin: 0px; padding: 10px;">
            <section style="margin: 0px; padding: 8px; border-width: 1px; border-style: solid; border-color: rgb(100, 98, 97);">
                <section style="margin: 0px; padding: 10px; border-width: 1px; border-style: solid; border-color: rgb(85, 80, 77);">
                    <section class="" data-brushtype="text" style="margin: 0px; padding: 0px 20px; display: inline-block; width: auto; background-color: rgb(64, 67, 66); color: rgb(254, 254, 254); line-height: 30px;">
                        <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em;">
                            热文推荐
                        </p>
                    </section>
                    <section class="" style="margin: 20px auto; padding: 0px;">
                        <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em;">
                            <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483733&idx=1&sn=c7f3ef7de3320862fa776892e091c7f0&chksm=fcde923ccba91b2afb83ed0524202049783f58a8ff3241cddc66aa42bc84c6d91b51bdb4b27b&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【词汇】英语四级必备词汇 第3课</a><br style="margin: 0px; padding: 0px;"/>
                        </p>
                        <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em;">
                            <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483733&idx=2&sn=69f639b4bd45bc97fce202c047de99c4&chksm=fcde923ccba91b2af2186b614fa9a5c5592e7fb66132ae6898728096a60f47f7e279fbfbcbe5&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【阅读】Visit to Australia / 访问澳大利亚</a>&nbsp;第一章<br style="margin: 0px; padding: 0px;"/>
                        </p>
                        <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em;">
                            <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483697&idx=1&sn=2209a5aeadb4a26b6d5d3607fc419cdb&chksm=fcde9258cba91b4e7d3a6fecbfd784a470ced0f85226904aae25af4ebdcd4ef54170a5606378&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">【英语】为什么我们要学习英语？</a><br style="margin: 0px; padding: 0px;"/>
                        </p>
                        <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; min-height: 1em;">
                            <a href="http://mp.weixin.qq.com/s?__biz=MzU3MTQ1OTA3OA==&mid=2247483661&idx=1&sn=44213e9fcd9d19ba54843bbff3f8e720&chksm=fcde9264cba91b72ce573929626d597407b1f466d9dd18faf148bd4dee42c6a4f03fa263939a&scene=21#wechat_redirect" target="_blank" style="margin: 0px; padding: 0px; color: rgb(96, 127, 166); text-decoration-line: none;">如何学英语，看看这位同学的总结</a><br style="margin: 0px; padding: 0px;"/>
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
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em;">
    <img class="" data-backh="285" data-backw="558" data-before-oversubscription-url="https://mmbiz.qpic.cn/mmbiz_png/ULGBRicThgZvQ8jYm3SalNFjeLAEhCDs0D7jaNNTswkKBdeTdEctECR0u1mNSWMZBWoPPrIpXaicXbBQL0DyHWqg/0?wx_fmt=gif" data-copyright="0" data-ratio="0.5109489051094891" src="https://image.ipaiban.com/upload-ueditor-image-20180619-1529341446099077380.jpg" data-type="gif" data-w="685" width="100%" style="margin: 0px; padding: 0px; width: 668px; height: auto !important; visibility: visible !important;"/>
</p>
<p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal; min-height: 1em;">
    <br style="margin: 0px; padding: 0px;"/>
</p>
<p>
    <br/>
</p>
<section data-role="outer" label="Powered by 135editor.com" style="margin: 0px; padding: 0px; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; white-space: normal;">
    <section data-role="outer" label="Powered by 135editor.com" style="margin: 0px; padding: 0px;">
        <section class="" data-tools="" data-id="91435" style="margin: 0px; padding: 0px; border-width: 0px; border-style: none; border-color: initial;">
            <section data-role="paragraph" class="" style="margin: 0px; padding: 0px; border-width: 0px; border-style: none; border-color: initial;">
                <section data-width="100%" style="margin: 0px; padding: 0px; width: 668px; display: -webkit-flex; justify-content: center; align-items: center;">
                    <section style="margin: 0px; padding: 0px; display: inline-block; width: auto;">
                        <section class="" data-brushtype="text" style="margin: 0px; padding: 5px 10px; font-size: 14px; color: rgb(136, 136, 136); border-bottom: 0.1em solid rgb(130, 130, 130); border-top: 0.1em solid rgb(130, 130, 130); line-height: 35px;">
                            <span style="margin: 0px; padding: 0px; color: rgb(178, 178, 178);">↓↓↓你的每一个点赞，都是对我爱的鼓励！</span>
                        </section>
                        <p>
                            <span style="margin: 0px; padding: 0px; color: rgb(178, 178, 178);"><br/></span>
                        </p>
                    </section>
                </section>
            </section>
        </section>
    </section>
</section>
'''

txt_name = 'book_warm_' + today + ".txt"
f = open(txt_name, "a+")
f.truncate()

# 列表
def read_bookwarm():

    cur.execute("select * from english_bookworm where `status` = 0 order by id asc limit 1")
    data = cur.fetchall()

    item = ''
    for i,info in enumerate(data):

        txt_name = info[1]
        txt_sumary = info[2]
        txt_en = info[3]
        txt_cn = info[4]

        cur.execute("update english_bookworm set `status` = 1 where `id` = %s", (info[0]))
        conn.commit()

        # print item
        f.write(item)

    # 分析 内容
    txt_en_arr = txt_en.split("\n")
    txt_cn_arr = txt_cn.split("\n")

    for i,info in enumerate(txt_en_arr):

        # print info.strip()
        f.write('''
            <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
                '''+ info.strip() +'''
            </p>
            <p></p>
        ''')
        for y,item in enumerate(txt_cn_arr):

            if i == y:

                # print item.strip()
                f.write('''
                    <p style="margin-top: 0px; margin-bottom: 0px; padding: 0px; clear: both; font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; font-size: medium; white-space: normal;">
                        <span style="margin: 0px; padding: 0px; color: rgb(178, 178, 178);">'''+ item.strip() +'''</span>
                    </p>
                    <p></p>
                ''')
                break

        # print i

def main():

    # 开始
    f.write(data_begin)

    # 句子
    read_bookwarm()

    # 结束
    f.write(data_end)

    print 'SUCESS'

if __name__ == '__main__':

    main()