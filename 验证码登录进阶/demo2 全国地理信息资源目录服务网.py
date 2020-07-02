# encoding:gbk
import requests
from fake_useragent import UserAgent

headers = {
    'User-Agent': str(UserAgent().random)
}
session = requests.session()

# 验证码地址
img_url = 'http://www.webmap.cn/user.do?method=checkCode'
img_response = session.get(img_url, headers=headers)
img_response.encoding = img_response.apparent_encoding
img_rep = img_response.content

with open('Code.jpg', 'wb') as f:
    f.write(img_rep)

checkCode = input("请输入验证码: ")
url = 'http://www.webmap.cn/user.do?method=userLogin'
data = {
'userName': 'qzhb',
'userPwd': 'cai201314',
'checkCode': checkCode
}

response = session.post(url, data=data, headers=headers)
response.encoding = response.apparent_encoding
rep = response.text
print(response.status_code)

with open('地理信息服务.html', 'w', encoding='utf-8') as f:
    f.write(rep)
