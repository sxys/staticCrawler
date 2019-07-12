import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# 建立浏览器对象 ，通过Phantomjs
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('log-level=3')
browser = webdriver.Chrome(chrome_options=chrome_options)


def query_content(url) :
	headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
	'Cookie': 'JSESSIONID=43BE1CC8BE38485E7ED0AA2B3E60A068'
	}

	res = requests.get(url, headers=headers)

	soup=BeautifulSoup(res.text,'html.parser')
	# print(soup)
	text = soup.find('div', class_='zw_hide')
	#print(text)
	return text



if __name__ == "__main__":


	#'执法办案信息采集', '人员综合信息采集','人员信息标准化采集', '信息综合采集', '办案区信息采集设备', '人员信息快速录入系统', 	'标准化基础信息采集', '刑侦一体化采集', '一体化采集', '综合采集', '信息采集一体机', '办案区', '一体化采集设备'
	keyword_list = [
	#'%D6%B4%B7%A8%B0%EC%B0%B8%D0%C5%CF%A2%B2%C9%BC%AF', \
	#'%C8%CB%D4%B1%D7%DB%BA%CF%D0%C5%CF%A2%B2%C9%BC%AF', \
	#'%C8%CB%D4%B1%D0%C5%CF%A2%B1%EA%D7%BC%BB%AF%B2%C9%BC%AF', \
	'%D0%C5%CF%A2%D7%DB%BA%CF%B2%C9%BC%AF'
	]

	list_url = 'http://s.zhaobiao.cn/s?searchtype=sj&queryword='

	for keyword in keyword_list :
		# 访问url
		browser.get(list_url + keyword)

		# 等待一定时间，让js脚本加载完毕
		browser.implicitly_wait(8)

		body = browser.find_element_by_id('datatbody')

		rows = body.find_elements_by_class_name('datatr')
		for row in rows:
			aa = row.find_element_by_tag_name('a')
			title = row.find_element_by_tag_name('span')
			if aa :
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
