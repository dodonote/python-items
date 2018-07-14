# coding: utf-8
# ------------------------------------------------
#    作用：创建每日壁纸 手机版
#    日期：2018-03-25
#    作者：呆呆
#    微信：zhixuez
# ------------------------------------------------

import requests
from bs4 import BeautifulSoup
import lxml
import htmllib
import urllib
import pymysql
import datetime
from PIL import Image, ImageFont, ImageDraw
import weather

HOSTNAME = '127.0.0.1'
USERNAME = 'root'
PASSWORD = ''
DATABASE = 'pydata'

conn = pymysql.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE, charset="utf8")
cur = conn.cursor()

today = datetime.date.today().strftime("%Y-%m-%d")
# print today
filename = 'weather-%s.png' % today

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

# 列表
def read_vocabulary():

    cur.execute("select * from english_vocabulary where `status` = 0 order by id asc limit 1")
    data = cur.fetchall()

    item = ''
    ary = []
    for i,info in enumerate(data):

        print i,info[2],info[3],info[4],info[5],info[6]

        sub_ary = (info[2],info[3],info[4],info[5],info[6])
        ary.append(sub_ary)

        # if i == 0:
        #     f.write('<p><br/></p>')

        return ary

# 计算天数
def count():

    f = open(u"count.txt")

    line = f.read()
    # print line

    # line = int(line)

    line = int(line)
    # print type(line)
    line = line + 1
    # print line

    f2 = open(u"count.txt", "w")
    data = str(line)
    f2.write(data)

    f.close()
    f2.close()
    return line

weather_data = weather.getWeather()

#加载底图
base_img = Image.new('RGB',(1080,1920),'#FFFFFF')
# 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
# print base_img.size, base_img.mode
box = (0, 0, 1080, 1920)  # 底图上需要P掉的区域

#加载需要P上去的图片 背景图
tmp_img = Image.open(ur'img/wangluo/7.jpg')
#这里可以选择一块区域或者整张图片
# region = tmp_img.crop((0,0,600,600)) #选择一块区域
#或者使用整张图片
region = tmp_img

#使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
# 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
#提前将图片进行缩放，以适应box区域大小
# region = region.rotate(180) #对图片进行旋转
print box[2]-box[0]
print box[3]-box[1]
region = region.resize((box[2] - box[0], box[3] - box[1] + 50))
region = region.crop((0,0,1080,1920))
base_img.paste(region, box)

draw = ImageDraw.Draw(base_img)
draw.rectangle((0,1300,1080,1920),fill = '#FFFFFF') # DA70D6 淡紫色 # FF8000 橘黄 # ED9121 萝卜黄

# 添加天气图片
box = (20, 30, 60, 60)
weather_img = Image.open(filename)
# print weather_img.mode
# print weather_img.size

weather_img = weather_img.convert("RGBA")

# 分离通道
# r,g,b,a = weather_img.split()

weather_img = weather_img.resize((box[2] - box[0], box[3] - box[1]))

# weather_img.show()
base_img.paste(weather_img, box, mask=weather_img.split()[3])

# 头像
user_img = Image.open(ur"user/ree.jpg")
print user_img.mode,user_img.size
user_box = (20, 1315, 120,1410)
user_img = user_img.convert('RGBA')
user_img = user_img.resize((user_box[2] - user_box[0], user_box[3] - user_box[1]))
base_img.paste(user_img, user_box)

# 二维码
user_img = Image.open(ur"user/mtsgyy.jpg")
print user_img.mode,user_img.size
user_box = (460, 1750, 610, 1900)
user_img = user_img.convert('RGBA')
user_img = user_img.resize((user_box[2] - user_box[0], user_box[3] - user_box[1]))
base_img.paste(user_img, user_box)

# 添加文字
sign_text1 = u'版权声明：本文为博主原创，未经允许不得转载。'
sign_text2 = u'博主地址：http://www.www.www'
# 字体必须大于等于19才可以输出汉字，过小可能该库渲染不起来，具体原因不清楚。
font = ImageFont.truetype('../simhei.ttf', 30)
# img = Image.open(qq_screencapture_file)
# 获得图片长和宽,将文字写到最底下.
width, height = base_img.size
# img = Image.new("RGBA",(300,200),(0,0,0))
draw = ImageDraw.Draw(base_img)
# draw.text( (0,50), u'你好,世界!', font=font)
# draw.text( (0,50), unicode(txt,'UTF-8'))
# draw.text((width / 2 - 150, 100), sign_text1, fill='#ff0000', font=font)
# draw.text((width / 2 - 150, 150), sign_text2, fill='#ff0000', font=font)

# 添加天气
# print weather_data[0][0]
sign_text3 = weather_data[0][4]
weather = weather_data[0][5].replace(u"空气质量：","")
draw.text((65, 30), sign_text3, fill='#FFFFFF', font=font)

print len(sign_text3)
if len(sign_text3) > 10:
    draw.text((335, 30), weather, fill='#badc00', font=font)
else:
    draw.text((275, 30), weather, fill='#badc00', font=font)

# 添加每日一句
# sentence = getSentence()
#
# draw.text((50, 600), sentence[0], fill = '#FFFFFF', font=font)
#
# if len(sentence) == 3:
#     aa = sentence[2]
#     aa = aa.decode('utf-8')
#     draw.text((50, 620), sentence[1], fill = '#FFFFFF', font=font)
#     draw.text((50, 640), aa, fill = '#FFFFFF', font=font)
# else:
#     aa = sentence[1]
#     aa = aa.decode('utf-8')
#     draw.text((50, 630), aa, fill = '#FFFFFF', font=font)

# 词汇
vocabulary = read_vocabulary()[0]

import unicodedata
v1 = vocabulary[1]
v1a = unicodedata.normalize('NFKD', v1).encode('ascii','ignore') # unicode 转 str

v1a = v1a.replace("","")

# print unicode(vocabulary[1], "UTF-8")

# exit();

draw.text((200, 1450),  vocabulary[0], fill= "#333", font=font)
draw.text((350, 1450),   v1a, fill= "#999", font=font)
draw.text((200, 1500),  vocabulary[2], fill= "#333", font=font)
draw.text((200, 1590),  vocabulary[3], fill= "#333", font=font)
draw.text((200, 1640),  vocabulary[4], fill= "#333", font=font)

# 作者
day_count = count()
print day_count

draw.text((130, 1325),  u"Tony", fill= "#333", font=font)
draw.text((130, 1365),  today, fill= "#333", font=font)
draw.text((930, 1325),  str(day_count), fill= "#333", font=ImageFont.truetype('../simhei.ttf', 36))
draw.text((880, 1365),  u"累计练习(天)", fill= "#333", font=font)

# draw.text((260, 850),  u"学英语不能死记硬背\n找到学习的兴趣\n快乐的学习", fill= "#FFF", font=font)

del draw
base_img.show() # 查看合成的图片
base_img.save('./img_result/vocabulary_day_%s.jpg' % today) #保存图片