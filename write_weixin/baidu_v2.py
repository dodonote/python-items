#!/usr/bin/python3
# * coding:utf-8 *
# 用户 ： Hu
# Time : 2018/6/26 0026  10:03

# 百度翻译
import urllib
import urllib2
import requests

# 手机版百度翻译
url = 'http://fanyi.baidu.com/basetrans'

headers = {
# 手机浏览器的UA
    "User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"
}

# 构造post请求的data
# word = input('请输入您要查询的单词：')
data = {
    'from': 'en',
    'to': 'zh',
    'query': 'What happened: Ofo said it has managed to lower operating cost to RMB 0.2 per day from early 2017’s RMB 1.5 per bike. In early May, CEO Dai Wei said the company is launching a program called “Victory”, which will help the company profit. According to the company’s operating officer, Ofo is using IoT big data platform to help maintain its bikes.',
}
data = urllib.urlencode(data).encode('utf-8')

req = urllib2.Request(url=url, headers=headers, data=data)

response = urllib2.urlopen(req)
print(response.read().decode('utf-8'))