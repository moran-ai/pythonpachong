# encoding:gbk
import requests
from fake_useragent import UserAgent

url = 'https://accounts.douban.com/j/mobile/login/basic'

# python第三方库自动生成请求头
headers = {'User-Agent': str(UserAgent().random)}

data = {
'ck':'',
'name': '18974498571',
'password': 'cai201314',
'remember': 'false',
'ticket': ''
}
session = requests.session()
response = session.post(url, data=data, headers=headers)
response.encoding = response.apparent_encoding
print(response.status_code)
rep = response.text

# with open('douban.html', 'w', encoding='utf-8') as f:
#     f.write(rep)

new_url = 'https://www.douban.com/'
response_new = session.get(new_url, headers=headers)
response_new.encoding = response_new.apparent_encoding
print(response_new.status_code)
rep_new = response_new.text

with open('douban_new.html', 'w', encoding='utf-8') as f:
    f.write(rep_new)
