#!/usr/bin/env python
# coding=utf-8

from PIL import Image, ImageDraw, ImageFont

image = Image.new('RGBA',(600,900),'#FFFFFF')
draw_table = ImageDraw.Draw(im=image)
draw_table.text(xy=(0, 0), text=u'仰起脸笑得像满月', fill='#008B8B', font=ImageFont.truetype('SimHei.ttf', 50))

image.show()  # 直接显示图片
image.save(u'满月.png', 'PNG')  # 保存在当前路径下，格式为PNG
image.close()

# 通常使用RGB模式就可以了
newIm= Image.new('RGB', (100, 100), 'red')
newIm.save(r'C:\Users\Administrator\Desktop\1.png')

# 也可以用RGBA模式，还有其他模式查文档吧
blcakIm = Image.new('RGB',(200, 100), 'red')
blcakIm.save(r'C:\Users\Administrator\Desktop\2.png')
# 十六进制颜色
blcakIm = Image.new('RGBA',(200, 100), '#FF0000')
blcakIm.save(r'C:\Users\Administrator\Desktop\3.png')
# 传入元组形式的RGBA值或者RGB值
# 在RGB模式下，第四个参数失效，默认255，在RGBA模式下，也可只传入前三个值，A值默认255
blcakIm = Image.new('RGB',(200, 100), (255, 255, 0, 120))
blcakIm.save(r'C:\Users\Administrator\Desktop\4.png')