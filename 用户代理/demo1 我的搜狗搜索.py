# encoding:gbk
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from lxml import etree

headers = {
    'User-Agent': str(UserAgent().random)
}
url = 'https://www.sogou.com/web'

params = {
'query': 'ip'
}

# proxy代理ip
# proxy = {
#     'https': '121.237.149.96:3000'
# }

response = requests.get(url, params=params, headers=headers)
rep = response.content.decode('utf-8')
# print(rep)
with open('搜狗1.html', 'w', encoding='utf-8') as f:
    f.write(rep)

# 解析数据
# soup = BeautifulSoup(rep, 'lxml')
# ip = soup.find('div', id='ipsearchresult').text.replace(' ', '')
# print(ip)
tree = etree.HTML(rep)
ip_xpath = "//div[@id='ipsearchresult']//text()"
ip = tree.xpath(ip_xpath)
# ip
print(ip[0])
# 来源
print(ip[1].replace(' ', ''))

