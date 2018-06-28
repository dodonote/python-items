#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
import os
import json  # 导入json模块
import urllib  # 导入urllib模块
import urllib2
import requests
import HTMLParser
import urlparse
import hashlib
import datetime
from lxml import etree


def translate(cnValue, target):
    key = '0nCPSNMzkoqLMY8H4o7h'
    appId = '20170919000083757'
    salt = datetime.datetime.now().strftime('%m%d%H%M%S')

    quoteStr = urllib.quote(cnValue)

    md5 = hashlib.md5()
    md5.update((appId + cnValue + salt + key).encode())
    sign = md5.hexdigest()
    url = 'http://fanyi-api.baidu.com/api/trans/vip/translate?q=' + quoteStr + \
        '&from=auto&to=' + target + '&appid=' + \
        appId + '&salt=' + salt + '&sign=' + sign
    try:
        resultPage = requests.get(url)  # 调用百度翻译API进行批量翻译

        print resultPage.text
    except urllib2.HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        return cnValue
    except urllib2.URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        return cnValue
    except Exception as e:
        print('translate error.')
        print(e)
        return cnValue

    # 取得翻译的结果，翻译的结果是json格式
    # resultJason = resultPage.read().decode('utf-8')
    # js = None
    # try:
    #     # 将json格式的结果转换成Python的字典结构
    #     js = json.loads(resultJason)
    #     print(js)
    # except Exception as e:
    #     print('loads Json error.')
    #     print(e)
    #     return cnValue

    key = u"trans_result"
    #
    # if key in js:
    #     dst = js["trans_result"][0]["dst"]  # 取得翻译后的文本结果
    #     return dst
    # else:
    #     return cnValue  # 如果翻译出错，则输出原来的文本

def iteratorElem(elememt):
    for sub in elememt:
        try:
            cnValue = sub.attrib['value3']
            print(sub.attrib['value5'])
            #sub.attrib['value4'] = translate(cnValue,'cht')
            #sub.attrib['value5'] = translate(cnValue,'ara')
            #sub.attrib['value6'] = translate(cnValue,'fra')
        except KeyError as e:
            pass
        finally:
            iteratorElem(sub)


if __name__ == '__main__':
    # 通过获得命令行参数获得输入输出文件名
    # for rt, dirs, files in os.walk(os.getcwd() + os.sep):
    #     for f in files:
    #         if(not os.path.exists(os.getcwd() + os.sep + f)):
    #             continue
    #         fname = os.path.splitext(f)
    #         if fname[1].lower() == ".xml":
    #             tree = etree.parse(f)
    #             root = tree.getroot()
    #             iteratorElem(root)
    #             # tree.write(f,encoding="UTF-8");

    translate("An Australian think-tank has disclosed that Huawei is the biggest corporate sponsor of overseas travel for Australian politicians. Huawei paid for 12 trips to Shenzhen for federal politicians. Huawei has responded that the company was not doing anything improper by inviting media, business, think tanks and politicians to visit them","fra")
