#-*- coding:utf-8 -*-

import urllib
from urllib2 import urlopen
# import urllib.request
# import urllib.parse
import requests
import json
content=0
while True:
        # content=input("请输入需要翻译的内容:")
        content="hello"
        if content!='quit':
                url="http://fanyi.baidu.com/v2transapi"
                data={}
                data['from']='zh'
                data['to']='en'
                data['query']=content
                data['transtype']='translang'
                data['simple_means_flag']='3'
                data=urllib.urlencode(data).encode("utf-8")
                print data
                response=requests.get(url,data)
                print response.url
                print response.text
                # html=response.read().decode("utf-8")
                # target=json.loads(html)
                # tgt=target['trans_result']['data'][0]['dst']
                # print("翻译的结果是：%s"% tgt)
        else:
                break