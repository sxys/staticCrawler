import requests
from aip import AipOcr
 

APP_ID = '16826437'
API_KEY = '5BxNTz1Y17FK025kLVOhtMr9'
SECRET_KEY = 'DNFhALdrHyNK22hcLgqPUI0Sr43XgX8d'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

url = 'http://www.zhaobiao.cn/common/img.jsp?n=l&ms=0.5615986593613058'

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

download_yzm = get_file_content('E:\\download\\yzm.png')

res=client.basicGeneral(download_yzm);
print(res)
words = res['words_result']
word = words[0]['words']
yzm = word.replace(' ', '')
print(yzm)
