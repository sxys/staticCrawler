from selenium import webdriver
from PIL import Image
import time

from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('log-level=3')

#  打开一个谷歌浏览器的实例
b = webdriver.Chrome(chrome_options=chrome_options)
b.get("http://www.zhaobiao.cn/")
b.maximize_window() #  最大化浏览器
time.sleep(2)
# 获取元素的尺寸
size =  b.find_element_by_xpath("//*[@id=\"randimg\"]").size
print(size)
# 获取元素的坐标
location  =  b.find_element_by_xpath("//*[@id=\"randimg\"]").location
print(location)
# 截取全屏
b.save_screenshot('1.png')
# 设置好图片的位置
left = location['x']
upper = location['y']
right = size['width'] + location['x']
lower = size['height'] + location['y']
# 打开全屏，进行验证码截取
img = Image.open('1.png')
#  将图片的位置作为一个元祖传入
im = img.crop((left, upper, right, lower))
# 最后保存图片
im.save('img.png')