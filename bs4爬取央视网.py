# encoding:gbk
import requests
from bs4 import BeautifulSoup

# ��ȡurl
url = "http://www.cctv.cn/2019/07/18/ARTINRdc1b6csFvNooPcX01i190718.shtml"

# ��������ͷ
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Connection':'close'
}

# ��������
response= requests.get(url, headers)
rep = response.content.decode('utf-8')

# ����bs4�Ķ���
soup = BeautifulSoup(rep, 'lxml')

# ������ҳ���������
title = soup.title.text
# print(str(title))

# ��������ʱ��
time = soup.i.text
# print(str(time))

# �������±���
h1 = soup.h1.text
# print(str(h1))

# �����������ݵĽ���
main_contents = soup.find('div', class_='content_box').find_all('p')
# print(str(main_contents))

# contents = ""
# for p in main_contents:
#     contents += p.text
# # print(contents)
#
# content = {
#     "��ҳ����":title,
#     "����ʱ��":time,
#     "���±���":h1,
#     "��������":contents
# }
#
# # ����
# with open('����.txt', 'w', encoding='utf-8') as f:
#     f.write(str(content))
