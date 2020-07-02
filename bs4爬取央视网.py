# encoding:gbk
import requests
from bs4 import BeautifulSoup

# 获取url
url = "http://www.cctv.cn/2019/07/18/ARTINRdc1b6csFvNooPcX01i190718.shtml"

# 构造请求头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Connection':'close'
}

# 发起请求
response= requests.get(url, headers)
rep = response.content.decode('utf-8')

# 构建bs4的对象
soup = BeautifulSoup(rep, 'lxml')

# 解析网页标题的内容
title = soup.title.text
# print(str(title))

# 解析发布时间
time = soup.i.text
# print(str(time))

# 解析文章标题
h1 = soup.h1.text
# print(str(h1))

# 进行文章内容的解析
main_contents = soup.find('div', class_='content_box').find_all('p')
# print(str(main_contents))

# contents = ""
# for p in main_contents:
#     contents += p.text
# # print(contents)
#
# content = {
#     "网页标题":title,
#     "发布时间":time,
#     "文章标题":h1,
#     "文章内容":contents
# }
#
# # 保存
# with open('央视.txt', 'w', encoding='utf-8') as f:
#     f.write(str(content))
