'''
美食节 各地小吃爬虫
主页url:  http://www.meishij.net/
排行榜url： http://top.meishi.cc/lanmu.php?cid=78
'''

# 导入相关库
import requests
from bs4 import BeautifulSoup


# 排行榜入口url
Top_food_url = 'https://www.meishij.net/china-food/caixi/'

# 家常菜谱入口url
Home_food_url = 'https://www.meishij.net/china-food/caixi/?&page=2'

# 中华菜系入口url
China_food_url = 'http://top.meishi.cc/lanmu.php?cid=2'

# 外国菜入口url
Foreign_food_url = 'http://top.meishi.cc/lanmu.php?cid=10'


def get_html_text(url):
    '''获取html文本'''
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'


def parse_city_id(url):
    '''解析对应的城市排行榜连接'''

    res = []
    html = get_html_text(url)
    # 做一个简单的判断
    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        # 定位到 全国各地特色小吃排行榜分类,<div>
        cityids = soup.find_all(class_='listtyle1')
        for city in cityids:
            #print(city['href'])
            #print(city['title'])
            image = city.a.img
            #print(image['src'])
            res.append({'name': city.a['title'], 'url': image['src']})
        return res
    else:
        print('error !!!!')



def main():
    '''程序入口'''
    # 构造所有起始url列表
    url_list = []
    for i in range(2, 56):
        url_list.append(Top_food_url + '?&page=' + str(i))
    
    # 找到所有城市排行榜的url
    for url in url_list:
        # 找到该分类下的所有cid
        res = parse_city_id(url)
        print(res)    

main()