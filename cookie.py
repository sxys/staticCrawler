import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
from requests.cookies import RequestsCookieJar




# 建立浏览器对象 ，通过Phantomjs
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('log-level=3')
# chrome_options.add_argument('user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
# chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"')
# chrome_options.add_argument('cookie="JSESSIONID=50FB14CB3812424E04991841BD4B9259"')
browser = webdriver.Chrome(chrome_options=chrome_options)


url = 'http://s.zhaobiao.cn/s?searchtype=sj&queryword=%D6%B4%B7%A8%B0%EC%B0%B8%D0%C5%CF%A2%B2%C9%BC%AF'
browser.get(url)

browser.add_cookie({'name': 'JSESSIONID', 'value': '272E0A1B7D2CF5452172349B6CCA0869', 'domain':'s.zhaobiao.cn', 'path': '/', 'expires': None})
# browser.add_cookie({'name': '__jsl_clearance', 'value': '1563259172.576|0|zfb7Ro94pbltZ7r5%2FRmwI%2FDfAjI%3D', 'domain':'s.zhaobiao.cn', 'path': '/', 'expires': None})
browser.add_cookie({'name': '__jsluid_h', 'value': '66fbd5c758d186e9c087c1e3e838d5e7', 'domain':'s.zhaobiao.cn', 'path': '/', 'expires': None})
browser.add_cookie({'name': 'bdshare_firstime', 'value': '1563499443215', 'domain':'s.zhaobiao.cn', 'path': '/', 'expires': None})
browser.add_cookie({'name': 'reg_referer', 'value': 'aHR0cDovL3Muemhhb2JpYW8uY24vcz9zZWFyY2h0eXBlPXNqJmZpZWxkPXN1cGVyJnF1ZXJ5d29yZD0lQjklQUIlQjAlQjIlQkUlRDY=', 'domain':'s.zhaobiao.cn', 'path': '/', 'expires': None})
browser.add_cookie({'name': '__jsluid_h', 'value': '40c64893f7a208e687700ecade273def', 'domain':'user.zhaobiao.cn', 'path': '/', 'expires': None})
browser.add_cookie({'name': 'JSESSIONID', 'value': 'E1B1EBBA05CC876EDDC7798285A8AC4D', 'domain':'www.zhaobiao.cn', 'path': '/', 'expires': None})
browser.get(url)
# 等待一定时间，让js脚本加载完毕
browser.implicitly_wait(5)

body = browser.find_element_by_id('datatbody')

rows = browser.find_elements_by_class_name('datatr')
print(len(rows))

url = 'http://zb.zhaobiao.cn/bidding_v_41683673.html?q=%B0%EC%B0%B8%C7%F8'

cookie_jar = RequestsCookieJar()
cookie_jar.set("JSESSIONID", "7B06A61760047C9AD057E30045C30F7A", domain="zb.zhaobiao.cn")
cookie_jar.set("__jsluid_h", "0a7da778c4707c1e4d0e0a0cb8c395b0", domain="zb.zhaobiao.cn")
cookie_jar.set("reg_referer", "aHR0cDovL3Muemhhb2JpYW8uY24vcz9zZWFyY2h0eXBlPXNqJmZpZWxkPXN1cGVyJnF1ZXJ5d29yZD0lRDIlQkIlQ0MlRTUlQkIlQUYlQjIlQzklQkMlQUYlQzklRTglQjElQjg=", domain="zb.zhaobiao.cn")

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
 
res = requests.get(url, cookies=cookie_jar, headers=headers)
soup=BeautifulSoup(res.text,'lxml')
#print(soup)

aa = soup.find('a', class_='w-docDown')
print(aa['href'])
