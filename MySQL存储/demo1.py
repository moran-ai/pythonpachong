import requests
from lxml import etree
import random
from bs4 import BeautifulSoup

# base_url = 'https://ah.122.gov.cn'
# url = base_url + '/#/viopub'
base_url = 'http://csga.changsha.gov.cn/jjzd/csjj_index/topic_4169_'
headers = [
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
                'Opera/8.0 (Windows NT 5.1; U; en)',
                'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
            ]
headers = {
    'User-Agent': random.choice(headers)
}
# print(rep)
# with open('jiao.html', 'w', encoding='utf-8') as f:
#     f.write(rep)
all_content = []
end_page = input("请输入尾页：")
for page in range(1, int(end_page)+1):
    url = base_url + str(page) + '.shtml'
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    rep = response.text
    # print(rep)

    soup = BeautifulSoup(rep, 'lxml')

    # 获取每个内容
    all = soup.select('div.list_content_box a.morePointer')
    # print(all)

    # for i in range(len(all)):
    #     # 违法时间
    #     time = all[i].select('a')
    #     print(time)
