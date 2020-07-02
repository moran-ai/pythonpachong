# encoding:gbk
import requests
import pytesseract
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from PIL import Image
from io import BytesIO

headers = {'User-Agent': str(UserAgent().random)}
session = requests.session()

# 登录页获取验证码链接
denglu_url = 'https://www.chinabidding.cn/cblcn/member.login/captcha?t=1586305628132&randomID=4b87856e-f10e-4c6a-aa6b-e94b647bab6a'
denglu_response = session.get(denglu_url, headers=headers)
denglu_response.encoding = denglu_response.apparent_encoding
denglu_rep = denglu_response.text
print(denglu_rep)
denglu_soup = BeautifulSoup(denglu_rep, 'lxml')
#
# image_url = 'https://www.chinabidding.cn/cblcn/member.login/captcha?t=1586305628132'
# # print(image_url)

# image_data = session.get(image_url, headers=headers)
# image = image_data.content
# print(image)

