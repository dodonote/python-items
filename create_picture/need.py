# -*- coding: utf-8 -*-

from PIL import Image,ImageDraw,ImageFont
from xlrd import open_workbook
import datetime

today = datetime.date.today().strftime("%Y-%m-%d")
print today
filename = '%s.xlsx' % today
wb = open_workbook(filename)
ttfont = ImageFont.truetype("wryh.ttf",40)

for s in wb.sheets():
	for row in range(2,s.nrows-3):
		values = []
		for col in range(s.ncols):
			values.append(s.cell(row,col).value)
		print values
		im = Image.open("template.jpg")  
		draw = ImageDraw.Draw(im)
		draw.text((161,350),values[5], fill=(0,0,0),font=ttfont)
		draw.text((161,635),values[2], fill=(0,0,0),font=ttfont)
		draw.text((161,835),values[7], fill=(0,0,0),font=ttfont)
		draw.text((880,1600),values[0], fill=(0,0,0),font=ttfont)
		save_filename = u'%s-%s.jpg' % (values[2],values[0])
		im.save(save_filename)
		values = []