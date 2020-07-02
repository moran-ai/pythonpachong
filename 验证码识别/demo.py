# encoding:gbk
import requests
import pytesseract
from bs4 import BeautifulSoup
from PIL import Image
from fake_useragent import UserAgent
from io import BytesIO

headers = {'User-Agent': str(UserAgent().random)}
session = requests.session()

# 登录页获取图片链接、__VIEWSTATE和__VIEWSTATEGENERATOR
# 登录页url
denglu_url = 'https://so.gushiwen.org/user/login.aspx?from=http%3a%2f%2fso.gushiwen.org%2fuser%2fcollect.aspx'
denglu_response = session.get(denglu_url, headers=headers)
denglu_response.encoding = denglu_response.apparent_encoding
denglu_rep = denglu_response.text

# 数据解析
denglu_soup = BeautifulSoup(denglu_rep, 'lxml')

# 验证码图片链接
img_url = "https://so.gushiwen.org"+denglu_soup.find('img', id='imgCode')['src']

# 获取__VIEWSTATE和__VIEWSTATEGENERATOR参数
__VIEWSTATE = denglu_soup.find('input', id='__VIEWSTATE')['value']
__VIEWSTATEGENERATOR = denglu_soup.find('input', id='__VIEWSTATEGENERATOR')['value']
# print(img_url)
# print(__VIEWSTATE)
# print(__VIEWSTATEGENERATOR)

# 发送请求获取验证码图片，并下载到本地
image_data = session.get(img_url, headers=headers)
# # 获取验证码内容
image = image_data.content
# print(image)
# 保存
filename = 'image_verify.jpg'
with open(filename, 'wb') as f:
    f.write(image)

# 验证码识别
# 将图像转为Image实例
img = Image.open(BytesIO(image))

# 转为灰度图  1:二值图像   L:灰度图
img = img.convert('L')

# 将验证码转为文本
security_code = pytesseract.image_to_string(img)
print("识别出的验证码为:" + security_code)
img.close()

# 模拟古诗文网登录
name = input("请输入用户名：")
pe = input("请输入密码：")
code = input("请输入验证码：")
url = 'https://so.gushiwen.org/user/login.aspx?from='
data = {
'__VIEWSTATE': __VIEWSTATE,
'__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
'from': 'http://so.gushiwen.org/user/collect.aspx',
'email': name,
'pwd': pe,
'code': code,
'denglu': '登录'
}
response = session.post(url, data=data, headers=headers)
response.encoding = response.apparent_encoding
rep = response.content
print("状态码：" + str(response.status_code))
print('历史记录:' + str(response.history))

# 验证登录成功
verify_url = 'https://so.gushiwen.org/user/collect.aspx'
verify_response = session.get(verify_url, headers=headers)

# 解析数据,获得账户显示的后六位
verify_soup = BeautifulSoup(verify_response.text, 'lxml')
verify_name = verify_soup.select('div.shisoncont div.line')[3].span.text
print("验证您的账户为：" + verify_name)

