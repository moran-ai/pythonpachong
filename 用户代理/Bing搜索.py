# encoding:gbk
import requests
from fake_useragent import UserAgent
from lxml import etree

headers = {
    'User-Agent': str(UserAgent().random)
}

url = 'https://cn.bing.com/search'
params = {
    'q': 'ip',
    'qs': 'n',
    'form': 'QBLH',
    'sp': '-1',
    'pq': 'ip',
    'sc': '8-2',
    'sk': '',
    'cvid': '635F7C1040674DA5836F74DBD6474323'
}
response = requests.get(url, params=params, headers=headers)
rep = response.content.decode('utf-8')

with open('Bing.html', 'w', encoding='utf-8') as f:
    f.write(rep)

# tree = etree.HTML(rep)
# ip_xpath = "//ul[@class='b_vList b_divsec']/li/div[@class='b_xlText']//text()"
# ip = tree.xpath(ip_xpath)
# print(ip)
