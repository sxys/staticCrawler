import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
from requests.cookies import RequestsCookieJar
import time
from PIL import Image
from aip import AipOcr


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

chrome_options.add_argument("--incognito"); 
browser = webdriver.Chrome(chrome_options=chrome_options)

url = 'http://www.zhaobiao.cn/'

# cookie_jar.set("__jsluid_h", "84b3ffd7d91b5925bbba6fdc339b73c6", domain="zb.zhaobiao.cn")
# cookie_jar.set("reg_referer", "aHR0cDovL3Muemhhb2JpYW8uY24vcz9zZWFyY2h0eXBlPXNqJmZpZWxkPXN1cGVyJnF1ZXJ5d29yZD0lQjklQUIlQjAlQjIlQkUlRDY=", domain="zb.zhaobiao.cn")


# 获取验证码图片
def save_image():
	browser.maximize_window() #  最大化浏览器
	browser.get(url)

	# 获取元素的尺寸
	time.sleep(7)
	yzm = browser.find_element_by_id('randimg')
	# yzm.click()
	size =  yzm.size
	print(size)
	# 获取元素的坐标
	location  =  yzm.location
	print(location)
	# 截取全屏
	browser.save_screenshot('1.png')
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

#读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 图片OCR识别验证码
def ocr_img():
	APP_ID = '16826437'
	API_KEY = '5BxNTz1Y17FK025kLVOhtMr9'
	SECRET_KEY = 'DNFhALdrHyNK22hcLgqPUI0Sr43XgX8d'
	client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

	image = get_file_content('img.png')
	res = client.basicAccurate(image);

	print(res)
	words = res['words_result']
	if(len(words) > 0):
		word = words[0]['words']
		yzm = word.replace(' ', '')
		print(yzm)
		return yzm
	else :
		return ''	

#登录获取cookie
def get_cookies(yzm):
	cookie_dict = {}
	try:
		topLoginUserId = browser.find_element_by_xpath("//*[@id=\"topLoginUserId\"]")
		topLoginPassword = browser.find_element_by_id('topLoginPassword')
		topLoginRand = browser.find_element_by_id('topLoginRand')
		submit = browser.find_element_by_class_name('top-login')


		topLoginUserId.clear()
		topLoginUserId.send_keys('gulinxing123')
		# time.sleep(2)

		topLoginPassword.clear()
		topLoginPassword.send_keys('Ltkj2019')

		topLoginRand.clear()
		topLoginRand.send_keys(yzm)

		submit.click()

		
		time.sleep(5)
		cookie_list = browser.get_cookies()
		print(cookie_list)
		return cookie_list
	except Exception as e:
		print('cannot get cookies')
		print(e)
		return []



def query_content(url,cookie_jar) :
	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
	}

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

#插入数据
def insertDB(dataList):
	for data_row in dataList:
		cursor_oracle.execute("select * from zhaobiao where title = '" + data_row['title'] + "'")
		cur_row = cursor_oracle.fetchone()
		if cur_row is None:
			cursor_oracle.callproc('insertzhaobiao', (data_row['title'], data_row['region'], data_row['date'], data_row['content'], data_row['keyword'], data_row['link'], data_row['download_url'], data_row['gg_type']))
		connection_oracle.commit()
	cursor_oracle.close()
	connection_oracle.close()

#开始采集
def getCrawlerData(keyword_list, cookie_list):
	list_url = 'http://s.zhaobiao.cn/s?searchtype=sj&queryword='

	cookie_jar = RequestsCookieJar()

	#设置正文查看的cookie
	cookie_dict = {}
	for cookie in cookie_list:
		cookie_dict[cookie['name']]=cookie['value']
	if 'JSESSIONID' in cookie_dict :	
		cookie_jar.set("JSESSIONID", cookie_dict['JSESSIONID'], domain="zb.zhaobiao.cn")
	
	dataList = []
	for keyword in keyword_list :
		print(keyword)
		# 访问url要编码
		url = list_url + quote(keyword.encode('gb2312'))
		print(url)
		browser.get(url)

		#设置搜索界面的cookie
		for cookie in cookie_list:
			if 'expiry' in cookie:
				del cookie['expiry']

			if 'httpOnly' in cookie:
				del cookie['httpOnly']

			if 'secure' in cookie:	
				del cookie['secure']
			browser.add_cookie(cookie)
		# browser.add_cookie({'name': 'Cookies_token', 'value': cookie_obj['Cookies_token'], 'domain':'.zhaobiao.cn', 'path': '/', 'expires': None})
		# browser.add_cookie({'name': 'Hm_lpvt_956837707a3009cb8b2b4f89a9280996', 'value': '1564044384', 'domain':'.zhaobiao.cn', 'path': '/', 'expires': None})
		# browser.add_cookie({'name': 'Hm_lvt_956837707a3009cb8b2b4f89a9280996', 'value': '1564044375', 'domain':'.zhaobiao.cn', 'path': '/', 'expires': None})

		browser.get(url)
		# 等待一定时间，让js脚本加载完毕
		browser.implicitly_wait(5)
		try:

			body = browser.find_element_by_id('datatbody')

			rows = browser.find_elements_by_class_name('datatr')
		except Exception as e:
			continue
			
		print('total rows:' + str(len(rows)))
		for row in rows:
			try:
				aa = row.find_element_by_tag_name('a')
			except Exception as e:
				# 搜索不到了
				print(e)
				#cursor_oracle.callproc('insertzhaobiao', ('', '','','',keyword,'', '', ''))
			else:
				if aa :
					title = row.find_element_by_tag_name('span')
					#print(title)
					# 找到地区、时间
					td = browser.find_element_by_xpath("//tbody[@id='datatbody']").find_elements_by_tag_name('td')
					gg_type = td[0].text
					region = td[2].text
					date = td[3].text
					print(region)
					print(date)
					#获取链接
					link = aa.get_attribute('href')
					print(link)
					print(title.text)
					#访问链接获取内容

					headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
					}
	
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

					content = query_content(link,cookie_jar)
					data_row = {}
					data_row['title'] = title.text
					data_row['region'] = region
					data_row['date'] = date
					data_row['content'] = content
					data_row['keyword'] = keyword
					data_row['link'] = link
					data_row['download_url'] = download_url
					data_row['gg_type'] = gg_type

					dataList.append(data_row)
	return dataList		



if __name__ == "__main__":
	#试10次，验证码通过就跳出
	cookie_list = []
	
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

	for num in range(10,20):
		save_image()
		yzm = ocr_img()
		if len(yzm) == 4:
			print('================')
			cookie_list = get_cookies(yzm)
			if(len(cookie_list) > 0):

				dataList = getCrawlerData(keyword_list, cookie_list)
				insertDB(dataList)
				
				break



