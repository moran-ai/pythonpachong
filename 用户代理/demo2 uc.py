# encoding:gbk
import requests
from fake_useragent import UserAgent
from lxml import etree

url = 'https://so.m.sm.cn/s'
headers = {
    'User-Agent': str(UserAgent().random)
}

params = {
    'q': 'ip'
}

proxy = {
    'https': 'https://110.73.11.171:8123'
}

try:
    response = requests.get(url, params=params,headers=headers, proxies=proxy)
    rep = response.content.decode('utf-8')

    # with open('UC.html', 'w', encoding='utf-8') as f:
    #     f.write(rep)

    tree = etree.HTML(rep)
    ip_xpath = "//div[@id='number-ip-info']/div[@class='self-des']/p/text()"
    ip = tree.xpath(ip_xpath)
    # ip
    print(ip[0])
    # 地址
    print(ip[1])
except requests.exceptions.ProxyError as e:
    print("当前代理异常")
except:
    print("当前请求异常")
