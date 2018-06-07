# coding: utf-8

import requests
from bs4 import BeautifulSoup
import lxml
import htmllib
import urllib
import datetime
from PIL import Image, ImageFont, ImageDraw

today = datetime.date.today().strftime("%Y-%m-%d")
# print today
filename = 'weather-%s.png' % today

# 获取天气
def getWeather():

    res = requests.get('https://www.tianqi.com/beijing/')

    if res.status_code == 200:
        res.close()

        # print res.text
        soup = BeautifulSoup(res.text, 'lxml')
        weather_info = soup.select(".weather_info")[0]
        # print weather_info
        city = weather_info.select(".name > h2")[0].get_text()
        date = weather_info.select(".week")[0].get_text()
        weather = weather_info.select(".weather p")[0].get_text()
        weather_img = weather_info.select(".weather i img")[0]['src']
        temperature = weather_info.select(".weather span")[0].get_text()
        air = weather_info.select(".kongqi h5")[0].get_text()

        urllib.urlretrieve(weather_img, filename)

        data = []
        sub_arg = (city,date,weather,weather_img,temperature,air)
        data.append(sub_arg)

        # print city,date
        # print weather
        # print weather_img
        # print temperature
        # print air

        return data

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

#加载底图
base_img = Image.open(ur'img/img_english.jpg')
# 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
print base_img.size, base_img.mode
box = (0, 0, 1078, 1300)  # 底图上需要P掉的区域

#加载需要P上去的图片
tmp_img = Image.open(ur'img/richu.jpeg')
#这里可以选择一块区域或者整张图片
#region = tmp_img.crop((0,0,304,546)) #选择一块区域
#或者使用整张图片
region = tmp_img

#使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
# 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
#提前将图片进行缩放，以适应box区域大小
# region = region.rotate(180) #对图片进行旋转
print box[2]-box[0]
print box[3]-box[1]
region = region.resize((box[2] - box[0], box[3] - box[1]))
base_img.paste(region, box)

# 添加天气图片
box = (100, 100, 210, 210)
weather_img = Image.open(filename)
print weather_img.mode
print weather_img.size

weather_img = weather_img.convert("RGBA")

#分离通道
# r,g,b,a = weather_img.split()

weather_img = weather_img.resize((box[2] - box[0], box[3] - box[1]))

# weather_img.show()
base_img.paste(weather_img, box, mask=weather_img.split()[3])

# 添加文字
sign_text1 = u'版权声明：本文为博主原创，未经允许不得转载。'
sign_text2 = u'博主地址：http://www.www.www'
# 字体必须大于等于19才可以输出汉字，过小可能该库渲染不起来，具体原因不清楚。
font = ImageFont.truetype('simhei.ttf', 19)
# img = Image.open(qq_screencapture_file)
# 获得图片长和宽,将文字写到最底下.
width, height = base_img.size
# img = Image.new("RGBA",(300,200),(0,0,0))
draw = ImageDraw.Draw(base_img)
# draw.text( (0,50), u'你好,世界!', font=font)
# draw.text( (0,50), unicode(txt,'UTF-8'))
draw.text((width / 2 - 150, 100), sign_text1, fill='#ff0000', font=font)
draw.text((width / 2 - 150, 150), sign_text2, fill='#ff0000', font=font)

# 添加天气
data = getWeather()
# print data
# print data[0][0]
sign_text3 = data[0][0]+data[0][1]+data[0][2]
weather = data[0][4]+data[0][5]
draw.text((width / 2 - 150, 200), sign_text3, fill='#FFFFFF', font=font)
draw.text((width / 2 - 150, 230), weather, fill='#FFFFFF', font=font)

# 添加每日一句
sentence = getSentence()

draw.text((50, 250), sentence[0], fill = '#FFFFFF', font=font)

if sentence[2]:
    aa = sentence[2]
    aa = aa.decode('utf-8')
    draw.text((50, 270), sentence[1], fill = '#FFFFFF', font=font)
    draw.text((50, 290), aa, fill = '#FFFFFF', font=font)
else:
    aa = sentence[1]
    aa = aa.decode('utf-8')
    draw.text((50, 270), aa, fill = '#FFFFFF', font=font)

del draw
base_img.show() # 查看合成的图片
base_img.save('./img/english_day_%s.jpg' % today) #保存图片