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

# 登录页获取验证码信息
denglu_url = 'https://www.proginn.com/'
denglu_response = session.get(denglu_url, headers=headers)
denglu_response.encoding = denglu_response.apparent_encoding
# denglu_rep = denglu_response.text
# print(denglu_rep)

denglu_soup = BeautifulSoup(denglu_response.content, 'lxml')
# denglu_soup = etree.HTML(denglu_rep)
# image_xpath = "//div[@id='J_CaptchaField']/a[@id='J_Captcha']/img/@src"
# image_url = denglu_soup.xpath(image_xpath)
# print(image_url)
# image_url = 'https://www.proginn.com' + denglu_soup.find('img')['src']
image_url = 'https://www.proginn.com/api/captcha/image?_6705451'
# print(image_url)

image_data = session.get(image_url, headers=headers)
image = image_data.content
# print(image)

filename = 'chenxu.jpg'
with open(filename, 'wb') as f:
    f.write(image)

