import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('log-level=3')
browser = webdriver.Chrome(chrome_options=chrome_options)


url = 'http://zhaobiao.cn/'
browser.get(url)
browser.implicitly_wait(5)

# topLoginUserId = browser.find_element_by_id('topLoginUserId')
# topLoginPassword = browser.find_element_by_id('topLoginPassword')
# topLoginRand = browser.find_element_by_id('topLoginRand')

# topLoginUserId.clear()
# topLoginUserId.send_keys('gulinxing123')

# time.sleep(2)

# topLoginPassword.clear()
# topLoginPassword.send_keys('Ltkj2019')
# browser.execute_script("document.getElementById('randimg').src='http://www.zhaobiao.cn/common/img.jsp?n=l&ms=0.5615986593613058'")

# time.sleep(2)
# topLoginRand.clear()
# topLoginRand.send_keys('mufu')



# browser.find_element_by_class_name('top-login').click()

# browser.implicitly_wait(5)

cookies = browser.get_cookies()

print(cookies)
# filehandler = open("cookies.obj","wb")
# pickle.dump(cookies,filehandler)
