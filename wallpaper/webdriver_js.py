# coding: utf-8

from selenium import webdriver
import urllib
from bs4 import BeautifulSoup
import sys
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

driver = webdriver.PhantomJS(executable_path="C:/Python27/phantomjs-2.1.1-windows/bin/phantomjs.exe")
# driver.get("http://www.17.com")
# data = driver.title
# print (data)

# driver.get("http://item.jd.com/2914823.html")
#
# print (driver.page_source)
# fo = open("aaaa1.txt", "wb")
# fo.write(driver.page_source.encode())
# fo.close()
# driver.quit()
#
# from selenium import webdriver
# driver=webdriver.PhantomJS(executable_path="phantomjs.exe")
# driver.get("http://www.csdn.net")
# data = driver.title
# driver.save_screenshot('csdn.png')
# print(data)

# from selenium import webdriver

# driver = webdriver.PhantomJS()
# driver.set_page_load_timeout(5)
# driver.get('http://www.baidu.com')
try:
    source = driver.get('http://news.iciba.com/views/dailysentence/daily.html#!/detail/title/2018-05-25')
    # driver.find_element_by_id('kw')  # 通过ID定位
    # driver.find_element_by_class_name('s_ipt')  # 通过class属性定位
    # driver.find_element_by_name('wd')  # 通过标签name属性定位
    # driver.find_element_by_tag_name('input')  # 通过标签属性定位
    # driver.find_element_by_css_selector('#kw')  # 通过css方式定位
    # driver.find_element_by_xpath("//input[@id='kw']")  # 通过xpath方式定位
    # driver.find_element_by_link_text("贴吧")  # 通过xpath方式定位
    # print(driver.find_element_by_id('kw').tag_name)  # 获取标签的类型
    # print driver.page_source
    en = driver.find_elements_by_class_name('sentence-en')[0].text
    ch = driver.find_elements_by_class_name('sentence-ch')[0].text

    img_src = driver.find_elements_by_xpath('//div[@class="sentence-banner"]/a/img')[0].get_attribute("src")
    # photos = driver.find_element_by_xpath('//div[@class="sentence-banner"]//a/img')
    # images_all = driver.find_elements_by_xpath('//div[@id="mm-photoimg-area"]/a/img')
    # print img_src.get_attribute("src")
    today = datetime.date.today().strftime("%Y-%m-%d")
    print today
    filename = 'img/pic_day/img-day-%s.jpg' % today
    urllib.urlretrieve(img_src, filename)

    now = datetime.datetime.now()
    # print now
    # print now.hour
    # print now.year
    # print now.month
    # print now.day

    # print datetime.datetime.today()

    # print now.strftime("%Y-%m-%d %H:%M:%S")
    f = open("read_day.txt","a+")
    f.write(now.strftime("%Y-%m-%d"))
    f.write("\n")
    f.write(en)
    f.write("\n")
    f.write(ch)
    f.write("\n")
    f.write("\n")

    # 解析网页，获取下载图片的网址
    # soup = BeautifulSoup(source, 'lxml')
    # print soup
    # image = soup.find_all('img')
    # print image
    # url = image.get('src')
    # print url
    # # 下载图片
    # urllib.request.urlretrieve(url, "img-day.jpg")
    print("Download picture successfully!")
except Exception as e:
    print(e)
driver.quit()
