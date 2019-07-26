from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('log-level=3')

 
driver = webdriver.Chrome(chrome_options=chrome_options)

url="http://www.zhaobiao.cn"
driver.get(url)
# 获取cookie列表
cookie_list=driver.get_cookies()
# print(cookie_list)
# 格式化打印cookie
cookie_dict = {}
for cookie in cookie_list:
    cookie_dict[cookie['name']]=cookie['value']
print(cookie_dict)