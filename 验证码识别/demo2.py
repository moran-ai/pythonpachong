# encoding:gbk
import requests
import pytesseract
from bs4 import BeautifulSoup
from fake_useragent import  UserAgent
from PIL import  Image
from io import BytesIO
from lxml import etree

headers = {'User-Agent': str(UserAgent().random)}
session = requests.session()
#
# # 登录页获取验证码信息
# denglu_url = 'https://www.proginn.com/'
# denglu_response = session.get(denglu_url, headers=headers)
# denglu_response.encoding = denglu_response.apparent_encoding
# denglu_rep = denglu_response.text
# # print(denglu_rep)
#
# # denglu_soup = BeautifulSoup(denglu_response.content, 'lxml')
# # denglu_soup = etree.HTML(denglu_rep)
# # image_xpath = "//div[@id='J_CaptchaField']/a[@id='J_Captcha']/img/@src"
# # image_url = denglu_soup.xpath(image_xpath)
#
# # print(image_url)
# # image_url = 'https://www.proginn.com' + denglu_soup.find('img')['src']
# image_url = 'https://www.proginn.com/api/captcha/image?_6705451'
# # print(image_url)
#
# image_data = session.get(image_url, headers=headers)
# image = image_data.content
# # print(image)
#
# filename = 'chenxu.jpg'
# with open(filename, 'wb') as f:
#     f.write(image)
#
# # 验证码识别
# # 将图像转为Image实例
# img = Image.open(BytesIO(image))
#
# # 转为灰度图  1:二值图像   L:灰度图
# img = img.convert('L')
#
# # 将验证码转为文本
# security_code = pytesseract.image_to_string(img)
# print("识别出的验证码为:" + security_code)
# img.close()
#
# # 模拟登录
# name = input("请输入用户名：")
# password = input("请输入密码：")
# yzm = input("请输入验证码: ")
# url = 'https://www.proginn.com/api/passport/login'
# data = {
# 'name': name,
# 'password':password,
# 'url':'',
# 'yzm':yzm,
# 'randomID':'7654b8e2-37c4-4209-a772-b23c7e7af552'
# }
# response = session.post(url, data=data, headers=headers)
# response.encoding = response.apparent_encoding
# # print("状态码：" + str(response.status_code))
# print("历史记录:" + str(response.history))

# 验证登录成功
sucess_url = 'https://www.proginn.com/cat/'
sucess_response = session.get(sucess_url, headers=headers)
sucess_rep = sucess_response.text
# print(sucess_rep)

# 解析数据
# sucess_soup = BeautifulSoup(sucess_response.text, 'lxml')
# sucess_name = sucess_soup.select('div.ui dropdown right top pointing active visible > a > span.nickname dib item xh-highlight')
sucess_tree = etree.HTML(sucess_rep)
sucess_xpath = "//span[@class='nickname dib item']/text()"
sucess_name = sucess_tree.xpath(sucess_xpath)
print(sucess_name)

