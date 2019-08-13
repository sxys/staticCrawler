import requests
from bs4 import BeautifulSoup

from requests.cookies import RequestsCookieJar

# cookie_list = [{'domain': 'zhaobiao.cn', 'expiry': 1564729504.229401, 'httpOnly': False, 'name': 'Cookies_Key', 'path': '/', 'secure': False, 'value': '""'}, \
#  {'domain': 'zhaobiao.cn', 'expiry': 1564729504.229319, 'httpOnly': False, 'name': 'Cookies_Userid', 'path': '/', 'secure': False, 'value': '""'}, \
#  {'domain': 'zhaobiao.cn', 'httpOnly': False, 'name': 'Hm_lpvt_956837707a3009cb8b2b4f89a9280996', 'path': '/', 'secure': False, 'value': '1564124805'}, \
#  {'domain': 'zhaobiao.cn', 'expiry': 1595660804, 'httpOnly': False, 'name': 'Hm_lvt_956837707a3009cb8b2b4f89a9280996', 'path': '/', 'secure': False, 'value': '1564124788'},\
#  {'domain': 'www.zhaobiao.cn', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/', 'secure': False, 'value': '97209B77216642D1C54075D1E9924775'}, \
#  {'domain': 'zhaobiao.cn', 'httpOnly': False, 'name': 'Cookies_token', 'path': '/', 'secure': False, 'value': '857ae6a0-23c8-49f3-a37e-52201c2df72c'}, \
#  {'domain': 'www.zhaobiao.cn', 'expiry': 1595660781.321463, 'httpOnly': True, 'name': '__jsluid_h', 'path': '/', 'secure': False, 'value': 'ff1d4bf3afb8d6f5b11027e1793a7ede'}, \
#  {'domain': 'www.zhaobiao.cn', 'httpOnly': False, 'name': 'reg_referer', 'path': '/', 'secure': False, 'value': '"aHR0cDovL3d3dy56aGFvYmlhby5jbi8="'}, \
#  {'domain': 'www.zhaobiao.cn', 'expiry': 1564128380, 'httpOnly': False, 'name': '__jsl_clearance', 'path': '/', 'secure': False, 'value': '1564124780.137|0|9WHU5iIIkTXLDrV1hrxHmp24ni0%3D'}]



#cookie = {'JSESSIONID': '97209B77216642D1C54075D1E9924775', '__jsl_clearance': '1564124780.137|0|9WHU5iIIkTXLDrV1hrxHmp24ni0%3D', '__jsluid_h': 'ff1d4bf3afb8d6f5b11027e1793a7ede', 'reg_referer': '"aHR0cDovL3d3dy56aGFvYmlhby5jbi8="', 'Cookies_Key': '""', 'Cookies_Userid': '""', 'Cookies_token': '857ae6a0-23c8-49f3-a37e-52201c2df72c', 'Hm_lpvt_956837707a3009cb8b2b4f89a9280996': '1564124805', 'Hm_lvt_956837707a3009cb8b2b4f89a9280996': '1564124788'}

url = 'http://www.zhaobiao.cn/'

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

# s=requests.session()
# print('------------------')
# print(cookie_jar.get_dict())

cookie_jar = RequestsCookieJar()

# for cookie in cookie_list:
	# cookie_jar.set(cookie['name'], cookie['value'], domain=cookie['domain'])
cookie_jar.set('JSESSIONID', '8C081EE50B37FE5C758917D04B1E0AB9', domain='zb.zhaobiao.cn')
cookie_jar.set('Cookies_token', 'e45cabf5-aac7-4f8a-a9df-5f99ff75cbfd', domain='zhaobiao.cn')
cookie_jar.set('Hm_lpvt_956837707a3009cb8b2b4f89a9280996', '1564360395', domain='zhaobiao.cn')
cookie_jar.set('Hm_lvt_956837707a3009cb8b2b4f89a9280996', '1564360379', domain='zhaobiao.cn')

print(cookie_jar)
res = requests.get(url, headers=headers)
try:
	soup=BeautifulSoup(res.text,'lxml')
	print(soup)
	# text = soup.find('div', class_='zw_hide')
	# print(text)
	# if text is not None:
		# aa = text.text
except Exception as e:
	print(e)
