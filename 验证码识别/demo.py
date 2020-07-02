# encoding:gbk
import requests
import pytesseract
from bs4 import BeautifulSoup
from PIL import Image
from fake_useragent import UserAgent
from io import BytesIO

headers = {'User-Agent': str(UserAgent().random)}
session = requests.session()

# ��¼ҳ��ȡͼƬ���ӡ�__VIEWSTATE��__VIEWSTATEGENERATOR
# ��¼ҳurl
denglu_url = 'https://so.gushiwen.org/user/login.aspx?from=http%3a%2f%2fso.gushiwen.org%2fuser%2fcollect.aspx'
denglu_response = session.get(denglu_url, headers=headers)
denglu_response.encoding = denglu_response.apparent_encoding
denglu_rep = denglu_response.text

# ���ݽ���
denglu_soup = BeautifulSoup(denglu_rep, 'lxml')

# ��֤��ͼƬ����
img_url = "https://so.gushiwen.org"+denglu_soup.find('img', id='imgCode')['src']

# ��ȡ__VIEWSTATE��__VIEWSTATEGENERATOR����
__VIEWSTATE = denglu_soup.find('input', id='__VIEWSTATE')['value']
__VIEWSTATEGENERATOR = denglu_soup.find('input', id='__VIEWSTATEGENERATOR')['value']
# print(img_url)
# print(__VIEWSTATE)
# print(__VIEWSTATEGENERATOR)

# ���������ȡ��֤��ͼƬ�������ص�����
image_data = session.get(img_url, headers=headers)
# # ��ȡ��֤������
image = image_data.content
# print(image)
# ����
filename = 'image_verify.jpg'
with open(filename, 'wb') as f:
    f.write(image)

# ��֤��ʶ��
# ��ͼ��תΪImageʵ��
img = Image.open(BytesIO(image))

# תΪ�Ҷ�ͼ  1:��ֵͼ��   L:�Ҷ�ͼ
img = img.convert('L')

# ����֤��תΪ�ı�
security_code = pytesseract.image_to_string(img)
print("ʶ�������֤��Ϊ:" + security_code)
img.close()

# ģ���ʫ������¼
name = input("�������û�����")
pe = input("���������룺")
code = input("��������֤�룺")
url = 'https://so.gushiwen.org/user/login.aspx?from='
data = {
'__VIEWSTATE': __VIEWSTATE,
'__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
'from': 'http://so.gushiwen.org/user/collect.aspx',
'email': name,
'pwd': pe,
'code': code,
'denglu': '��¼'
}
response = session.post(url, data=data, headers=headers)
response.encoding = response.apparent_encoding
rep = response.content
print("״̬�룺" + str(response.status_code))
print('��ʷ��¼:' + str(response.history))

# ��֤��¼�ɹ�
verify_url = 'https://so.gushiwen.org/user/collect.aspx'
verify_response = session.get(verify_url, headers=headers)

# ��������,����˻���ʾ�ĺ���λ
verify_soup = BeautifulSoup(verify_response.text, 'lxml')
verify_name = verify_soup.select('div.shisoncont div.line')[3].span.text
print("��֤�����˻�Ϊ��" + verify_name)

