# encoding:gbk
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

url = "http://www.cctv.cn/2019/06/24/ARTIiLQHzTueKwiGP7PvzMMh190624.shtml"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
}

rep = requests.get(url, headers=headers)
rep.encoding = "utf-8"
response = rep.text
# print(response)

# ����bs4����
soup = BeautifulSoup(response, 'lxml')
# print(soup)

# ����
title = soup.h1.text
# print(title)

# ʱ��
time = soup.select('div.function > span.info > i')[0].text
times = time[6:]
print(times)

# ��Դ
source = time[:5]
# print(source)

# ����
substance = soup.find('div', class_='content_box').find_all('p')
# print(substance)

content = ''
for value in substance:
    content += value.text.strip()
# print(content)

# �������
data = {
    'title': title,
    'time': times,
    'source': source,
    'content': content
}

# mongodb���ݿ�����
# �������ݿ�
# (1) �޲�����ʽ����
# client = MongoClient()

# (2)�в���
# client = MongoClient('localhost', 27017)

# (3) url��ʽ����
# client = MongoClient('mongodb://localhost:27017/')
#
# # ������������ݿ�
# # (1)��'.'����ʽ
# # db = client.test_database
# # (2) �������ֵ����ʽ
# db = client['test_database']

# ������������ݼ���
# (1)��'.'����ʽ,����м���article����ֱ�ӷ��ʣ�û���ȴ����ٷ���
# column = db.article
# # (2)�������ֵ����ʽ
# column = db['article']
#
# # ��������
# result = column.insert_one(data)
# print(result)
