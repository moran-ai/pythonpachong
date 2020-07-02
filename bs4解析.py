import requests
from bs4 import BeautifulSoup

# 获取url
url = "https://juejin.im/post/5e6518946fb9a07c820fbaaf"

# 构造请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Connection': 'close'
}

# 发起请求
response = requests.get(url, headers=headers)
rep = response.text
# print(rep)

# 构建bs4对象
soup = BeautifulSoup(rep, 'lxml')

# 网页标题
title = soup.title.text
# print(str(title))

# 文章时间 time标签 datetime属性值
time = soup.time.attrs['datetime']
# print(str(time))

# 文章标题
article_title = soup.find('h1', class_='article-title').text
# print(str(article_title))

# 文章内容
main_contents = soup.find('div', class_='article-content').find_all('p', limit=6)
# print(str(article_content))

article_p = ""
for p in main_contents:
    article_p += p.text
# print(article_p)

content ={
    "网页标题":title,
    "发布时间":time,
    "文章标题":article_title,
    "文章内容":article_p
}
with open('jiujin.txt', 'w', encoding='utf-8') as f:
    f.write(str(content))

