# encoding:gbk
import requests
from fake_useragent import UserAgent
from lxml import etree
from bs4 import BeautifulSoup
import random
import pandas as pd

"""
http://www.66ip.cn/2.html

https://www.xicidaili.com/nn/

http://www.goubanjia.com/

"""

def stripText(textlist):
    """
    ���ı�תΪ�ַ�������ȥ�����е�\n,\t,\r,/���ַ�

    :param textlist:
    :return:
    """
    star_list = ""
    for item in textlist:
        item_str = item.strip().replace('\n','').replace('\t', '').replace('\r','').replace('/', '').replace('-','')
        # item_str = item.strip()  ������Ϊ��ʱ��Ĭ��ɾ���ַ������˵Ŀհ׷�(����'\n','\t','\r','')
        if item_str != '':
            if star_list != '':
                star_list = star_list + ',' + item_str
            else:
                star_list = item_str
    return star_list

headers = {
    'User-Agent': str(UserAgent().random)
}
base_url = 'http://www.66ip.cn/'
# response = requests.get(url, headers=headers)

all_content = []
end_page = input('������βҳ��')
for page in range(1, int(end_page)+1):
    if page ==1:
        url = base_url + 'index' + '.html'
    else:
        page = str(page)
        url = base_url + page + '.html'

    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    rep = response.text
    # print(rep)

    tree = etree.HTML(rep)
    item_xpath = "//div[@class='containerbox boxindex']/div[1]/table/tr/td"
    item_list = tree.xpath(item_xpath)
    # print(item_list)
    for item in item_list:
        item_dic = {}
        # ip��ַ
        ip_address_xpath = ".//div[@class='containerbox boxindex']/tr/td[1]/text()"
        ip_address = stripText(item.xpath(ip_address_xpath))
        print(ip_address)
        item_dic['ip��ַ'] = ip_address
        #
        # # �˿ں�
        # duankou_xpath = "//div[@class='containerbox boxindex']/div[1]/table/tr/td[2]//text()"
        # duankou = stripText(item.xpath(duankou_xpath))
        # # print(duankou)
        # item_dic['�˿ں�'] = duankou
        #
        # # ����λ��
        # address_xpath = "//div[@class='containerbox boxindex']/div[1]/table/tr/td[3]//text()"
        # address = stripText(item.xpath(address_xpath))
        # # print(address)
        # item_dic['����λ��'] = address
        #
        # # ��������
        # type_xpath = "//div[@class='containerbox boxindex']/div[1]/table/tr/td[4]//text()"
        # type = stripText(item.xpath(type_xpath))
        # # print(type)
        # item_dic['��������'] = type
        #
        # # ��֤ʱ��
        # time_xpath = "//div[@class='containerbox boxindex']/div[1]/table/tr/td[5]//text()"
        # time = stripText(item.xpath(time_xpath))
        # # print(time)
        # item_dic['��֤ʱ��'] = time
        # all_content.append(item_dic)
# print(all_content)
# �洢Ϊcsv�ļ�
# df = pd.DataFrame(data=all_content, columns=["ip��ַ", "�˿ں�", "����λ��", "��������", "��֤ʱ��"])
# df.to_csv('ip.csv', encoding='utf-8')
# print(df)