import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
from requests.cookies import RequestsCookieJar


import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#设置数据库链接
import cx_Oracle
conn_str = 'tiger/tiger@192.168.1.152:1521/caiji'
connection_oracle = cx_Oracle.Connection(conn_str)
cursor_oracle = connection_oracle.cursor()



# 建立浏览器对象 ，通过Phantomjs
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('log-level=3')
browser = webdriver.Chrome(chrome_options=chrome_options)
cookie_jar = RequestsCookieJar()

#设置正文查看的cookie
cookie_jar.set("JSESSIONID", "CF708C900D5111EAFC19E1B826CB6025:FG=1", domain="zb.zhaobiao.cn")
cookie_jar.set("__jsluid_h", "0a7da778c4707c1e4d0e0a0cb8c395b0", domain="zb.zhaobiao.cn")
cookie_jar.set("reg_referer", "aHR0cDovLzE5Mi4xNjguMS4xNTI6ODA4MS8=", domain="zb.zhaobiao.cn")

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}


def query_content(url) :
	global headers
	global cookie_jar
	res = requests.get(url, headers=headers, cookies=cookie_jar)
	try:
		soup=BeautifulSoup(res.text,'lxml')
		#print(soup)
		text = soup.find('div', class_='zw_hide')
		# print(text.text)
		if text is not None:
			aa = text.text
			return aa[0:2000]
	except Exception as e:
		return ''



if __name__ == "__main__":


	keyword_list = [
	# '执法办案信息采集',\
	# '人员综合信息采集', \
	# '人员信息标准化采集', \
	# '信息综合采集', \
	# '办案区信息采集设备', \
	# '人员信息快速录入系统', \
	# '标准化基础信息采集', \
	# '刑侦一体化采集', \
	# '一体化采集', \
	# '综合采集', \
	# '信息采集一体机', \
	# '办案区', \
	'一体化采集设备'
	]

	list_url = 'http://s.zhaobiao.cn/s?searchtype=sj&queryword='

	for keyword in keyword_list :
		print(keyword)
		# 访问url要编码
		url = list_url + quote(keyword.encode('gb2312'))
		print(url)
		browser.get(url)

		#设置搜索界面的cookie
		browser.add_cookie({'name': 'JSESSIONID', 'value': '1C3E8B03FA3A2580B9FA5348BD472EAB', 'domain':'s.zhaobiao.cn', 'path': '/', 'expires': None})
		browser.add_cookie({'name': '__jsl_clearance', 'value': '1563259172.576|0|zfb7Ro94pbltZ7r5%2FRmwI%2FDfAjI%3D', 'domain':'s.zhaobiao.cn', 'path': '/', 'expires': None})
		browser.add_cookie({'name': '__jsluid_h', 'value': '6197c0f0f4296d06fc194b8dba0f1ab5', 'domain':'s.zhaobiao.cn', 'path': '/', 'expires': None})
		browser.add_cookie({'name': 'bdshare_firstime', 'value': '1562898372900', 'domain':'s.zhaobiao.cn', 'path': '/', 'expires': None})
		browser.add_cookie({'name': 'reg_referer', 'value': 'aHR0cDovL3Muemhhb2JpYW8uY24vcz9zZWFyY2h0eXBlPXNqJmZpZWxkPXN1cGVyJnF1ZXJ5d29yZD0lQjAlRUMlQjAlQjglQzclRjglMDk', 'domain':'s.zhaobiao.cn', 'path': '/', 'expires': None})

		browser.get(url)
		# 等待一定时间，让js脚本加载完毕
		browser.implicitly_wait(5)

		body = browser.find_element_by_id('datatbody')

		rows = browser.find_elements_by_class_name('datatr')
		print(len(rows))
		for row in rows:
			try:
				aa = row.find_element_by_tag_name('a')
			except Exception as e:
				# 搜索不到了
				cursor_oracle.callproc('insertzhaobiao', ('', '','','',keyword,''))
			else:
				if aa :
					title = row.find_element_by_tag_name('span')
					#print(title)
					# 找到地区、时间
					td = browser.find_element_by_xpath("//tbody[@id='datatbody']").find_elements_by_tag_name('td')
					region = td[2].text
					date = td[3].text
					print(region)
					print(date)
					#获取链接
					link = aa.get_attribute('href')
					print(link)
					print(title.text)
					#访问链接获取内容

					res = requests.get(link, headers=headers, cookies=cookie_jar)
					soup=BeautifulSoup(res.text,'lxml')
					# print(soup)
					download_url = 'http://zb.zhaobiao.cn'
					try:
						download = soup.find('a', class_='w-docDown')
						# print(download)
						if download is not None:
							download_url = download_url + download['href']
							print(download_url)
						else :
							download_url = ''
					except Exception as e:
						download_url = ''

					content = query_content(link)
					cursor_oracle.execute("select * from zhaobiao where title = '" + title.text + "'")
					cur_row = cursor_oracle.fetchone()
					if cur_row is None:
						cursor_oracle.callproc('insertzhaobiao', (title.text, region, date, content, keyword, link, download_url))
		connection_oracle.commit()
	cursor_oracle.close()
	connection_oracle.close()	