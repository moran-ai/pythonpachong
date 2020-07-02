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

# 构建bs4对象
soup = BeautifulSoup(response, 'lxml')
# print(soup)

# 标题
title = soup.h1.text
# print(title)

# 时间
time = soup.select('div.function > span.info > i')[0].text
times = time[6:]
print(times)

# 来源
source = time[:5]
# print(source)

# 内容
substance = soup.find('div', class_='content_box').find_all('p')
# print(substance)

content = ''
for value in substance:
    content += value.text.strip()
# print(content)

# 组合数据
data = {
    'title': title,
    'time': times,
    'source': source,
    'content': content
}

# mongodb数据库连接
# 连接数据库
# (1) 无参数形式连接
# client = MongoClient()

# (2)有参数
# client = MongoClient('localhost', 27017)

# (3) url方式连接
# client = MongoClient('mongodb://localhost:27017/')
#
# # 创建或访问数据库
# # (1)以'.'的形式
# # db = client.test_database
# # (2) 以数据字典的形式
# db = client['test_database']

# 创建或访问数据集合
# (1)以'.'的形式,如果有集合article，就直接访问，没有先创建再访问
# column = db.article
# # (2)以数据字典的形式
# column = db['article']
#
# # 插入数据
# result = column.insert_one(data)
# print(result)
