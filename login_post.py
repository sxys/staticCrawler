import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from aip import AipOcr
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('log-level=3')
chrome_options.add_argument("--incognito"); 
# browser = webdriver.Chrome(chrome_options=chrome_options)

url = 'http://www.zhaobiao.cn/'

b = webdriver.Chrome(chrome_options=chrome_options)
b.maximize_window() #  最大化浏览器
# wait = WebDriverWait(b, 10) 
b.get(url)

# 获取验证码图片
def save_image():
	global b
	# 获取元素的尺寸
	time.sleep(5)
	yzm = b.find_element_by_id('randimg')
	yzm.click()
	size =  yzm.size
	print(size)
	# 获取元素的坐标
	location  =  yzm.location
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


#读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 图片OCR识别
def ocr_img():
	APP_ID = '16826437'
	API_KEY = '5BxNTz1Y17FK025kLVOhtMr9'
	SECRET_KEY = 'DNFhALdrHyNK22hcLgqPUI0Sr43XgX8d'
	client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

	image = get_file_content('img.png')

	res = client.basicAccurate(image);

	print(res)
	words = res['words_result']
	if(len(words)):
		word = words[0]['words']
		yzm = word.replace(' ', '')
		print(yzm)
		return yzm
	else:
		return ''	

# 调用登录接口
def login(yzm):
	headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
	data = {
	    'loginUserId':'gulinxing123',   
	    'loginType':'userId',
	    'yzm':yzm,
	    'loginPassword':'Ltkj2019'
	}
	url ='http://www.zhaobiao.cn/ssologin.do?method=checkUserTopAjax'
	session = requests.Session()
	response = session.post(url,headers = headers,data = data)
	
	cookies = response.cookies
	print(cookies)
	

def login_with_selnium(yzm):
	global b
	topLoginUserId = b.find_element_by_xpath("//*[@id=\"topLoginUserId\"]")
	topLoginPassword = b.find_element_by_id('topLoginPassword')
	topLoginRand = b.find_element_by_id('topLoginRand')

	topLoginUserId.clear()
	topLoginUserId.send_keys('gulinxing123')
	# time.sleep(2)

	topLoginPassword.clear()
	topLoginPassword.send_keys('Ltkj2019')

	topLoginRand.clear()
	topLoginRand.send_keys(yzm)

	# b.save_screenshot('2.png')
	# js = 'getTopRand();'
	# b.execute_script(js)

	# b.save_screenshot('3.png')
	submit = b.find_element_by_class_name('top-login')
	submit.click()

	
	time.sleep(5)
	# b.save_screenshot('3.png')
	cookie_list = b.get_cookies()
	print(cookie_list)
	cookie_dict = {}
	for cookie in cookie_list:
	    cookie_dict[cookie['name']]=cookie['value']
	print(cookie_dict)
	# print(cookies)
	# filehandler = open("cookies.obj","wb")
	# pickle.dump(cookies,filehandler)
	# # search = b.find_element_by_id('search-text')
	# search.send_keys('执法办案信息采集')
	# b.find_element_by_class_name('ss').click()



# 获取cookies



if __name__ == "__main__":
	save_image()
	yzm = ocr_img()
	if len(yzm) == 4:
		login_with_selnium(yzm)
		# login(yzm)