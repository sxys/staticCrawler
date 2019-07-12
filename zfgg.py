from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
browser = webdriver.Chrome(chrome_options=chrome_options)

titles = []





#获取每个公告的内容
def get_each_announcement(link):
	global browser
	browser.get(link)
	browser.implicitly_wait(3)
	disaplay = browser.find_element_by_id('displayGG')
	disaplay.click()
	browser.implicitly_wait(1)

	content = browser.find_element_by_class_name('vF_detail_content')
	
	return content.text[0:2000]


#获取每个列表的点击URL
def get_visit_links(url):
	print(url)
	global browser
	# 访问url
	browser.get(url)

	# 等待一定时间，让js脚本加载完毕
	browser.implicitly_wait(3)


	# 找到list
	ul = browser.find_element_by_class_name('c_list_bid')
	results = ul.find_elements_by_tag_name('li')

	links = []

	for result in results:
		aa = result.find_element_by_tag_name('a')
		global titles
		titles.append(aa.text)
		# print(aa.text)
		link = aa.get_attribute('href')
		links.append(link)

	return links




if __name__ == "__main__":
    url = 'http://www.ccgp.gov.cn/cggg/dfgg/'
    url_list = []
    url_list.append(url)

    for index in range(1, 24):
    	url_list.append(url + 'index_' + str(index) + ".htm")

    i = 0

    for url in url_list :
    	print(url)
    	links = get_visit_links(url)
    	for link in links :
    		print(link)
    		content = get_each_announcement(link)
    		cursor_oracle.execute("select * from zfgg where url = '" + link + "'")
    		row = cursor_oracle.fetchone()
    		#print(row)
    		#已经存在了，就不加了
    		if row is None:
    			cursor_oracle.callproc('insertgg', ('dfgg', titles[i], content, link))
    		i = i + 1

    connection_oracle.commit()
    cursor_oracle.close()
    connection_oracle.close()


