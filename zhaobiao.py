import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote

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


def query_content(url) :
	headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
	'Cookie': 'JSESSIONID=787CA1E28CDA1873834E995CB6B0C5BC'
	}

	res = requests.get(url, headers=headers)

	soup=BeautifulSoup(res.text,'lxml')
	#print(soup)
	text = soup.find('div', class_='zw_hide')
	#print(text)
	return text.text



if __name__ == "__main__":


	keyword_list = [
	'执法办案信息采集', \
	'人员综合信息采集', \
	'人员信息标准化采集', \
	'信息综合采集', \
	'办案区信息采集设备', \
	'人员信息快速录入系统', \
	'标准化基础信息采集', \
	'刑侦一体化采集', \
	'一体化采集', \
	'综合采集', \
	'信息采集一体机', \
	'办案区', \
	'一体化采集设备'
	]

	list_url = 'http://s.zhaobiao.cn/s?searchtype=sj&queryword='

	for keyword in keyword_list :
		print(keyword)
		# 访问url要编码
		url = list_url + quote(keyword.encode('gb2312'))
		print(url)
		browser.get(url)

		# 等待一定时间，让js脚本加载完毕
		browser.implicitly_wait(5)

		body = browser.find_element_by_id('datatbody')

		rows = body.find_elements_by_class_name('datatr')
		for row in rows:
			try:
				aa = row.find_element_by_tag_name('a')
			except Exception as e:
				# 搜索不到了
				cursor_oracle.callproc('insertzhaobiao', ('', '','','',keyword,''))
			else:
				if aa :
					title = row.find_element_by_tag_name('span')
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
					content = query_content(link)
					cursor_oracle.callproc('insertzhaobiao', (title.text, region, date, content[0:2000], keyword, link))
		connection_oracle.commit()
	cursor_oracle.close()
	connection_oracle.close()