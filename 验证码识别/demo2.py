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
# # ��¼ҳ��ȡ��֤����Ϣ
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
# # ��֤��ʶ��
# # ��ͼ��תΪImageʵ��
# img = Image.open(BytesIO(image))
#
# # תΪ�Ҷ�ͼ  1:��ֵͼ��   L:�Ҷ�ͼ
# img = img.convert('L')
#
# # ����֤��תΪ�ı�
# security_code = pytesseract.image_to_string(img)
# print("ʶ�������֤��Ϊ:" + security_code)
# img.close()
#
# # ģ���¼
# name = input("�������û�����")
# password = input("���������룺")
# yzm = input("��������֤��: ")
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
# # print("״̬�룺" + str(response.status_code))
# print("��ʷ��¼:" + str(response.history))

# ��֤��¼�ɹ�
sucess_url = 'https://www.proginn.com/cat/'
sucess_response = session.get(sucess_url, headers=headers)
sucess_rep = sucess_response.text
# print(sucess_rep)

# ��������
# sucess_soup = BeautifulSoup(sucess_response.text, 'lxml')
# sucess_name = sucess_soup.select('div.ui dropdown right top pointing active visible > a > span.nickname dib item xh-highlight')
sucess_tree = etree.HTML(sucess_rep)
sucess_xpath = "//span[@class='nickname dib item']/text()"
sucess_name = sucess_tree.xpath(sucess_xpath)
print(sucess_name)

