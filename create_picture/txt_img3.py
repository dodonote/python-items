# -*- coding:utf-8 -*-

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# from get_png import getpng


def transparent(infile):
    # open png,covert it into 'RGBA mode',resize it,get data then make a datalist
    datalist = list(Image.open(infile, 'r').convert('RGBA').resize((1000, 1000), Image.BILINEAR).getdata())
    # color(0,0,0,0) is transparent
    newim = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    for x in range(1000):
        for y in range(1000):
            # color(255,255,255,255) is 'white'
            if datalist[1000 * y + x] == (255, 255, 255, 255):
                newim.putpixel((x, y), (255, 255, 255, 255))
            else:
                pass
    newim.save("1000_1000.png")
    return "1000_1000.png"

#增加水印.直接写入文件.
def watermask(qq_screencapture_file):
    print(qq_screencapture_file)
    #写入两行文件.
    sign_text1 = u'版权声明：本文为博主原创，未经允许不得转载。'
    sign_text2 = u'博主地址：http://www.www.www'
    #字体必须大于等于19才可以输出汉字，过小可能该库渲染不起来，具体原因不清楚。
    font = ImageFont.truetype('simhei.ttf',19)
    img = Image.open(qq_screencapture_file)
    #获得图片长和宽,将文字写到最底下.
    width,height = img.size
    #img = Image.new("RGBA",(300,200),(0,0,0))
    draw = ImageDraw.Draw(img)
    #draw.text( (0,50), u'你好,世界!', font=font)
    # draw.text( (0,50), unicode(txt,'UTF-8'))
    draw.text((20,height-50),sign_text1,fill='#ff0000', font=font)
    draw.text((20,height-30),sign_text2,fill='#ff0000', font=font)
    del draw
    #正好qq图片是png的.
    img.save(qq_screencapture_file, "PNG")
    print("finish.")

# transparent("12345.png")




watermask("img/m.jpg")
