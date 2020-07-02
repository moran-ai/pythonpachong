#引入库文件
import requests
import csv
from lxml import etree
#pandas库
import pandas as pd
import json

def stripText(textList):
    '''
    将文本列表转化或字符串，并去掉其中包括的\n \t \r /-等字符
    :param textList: 文本列表
    :return: 字符串
    '''
    str_list=""
    for item in textList:
        item_str=item.strip().replace('\n',"").replace('\r',"").replace('\t',"").replace('/',"")
        #item_str=item.strip()当参数为空时，默认删除字符串两端的空白符（包括'\n','\r','\t','')
        if item_str!='':
            if str_list !='':
                str_list=str_list+","+item_str
            else:
                str_list=item_str
        return str_list

#U-A
header={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}

#url
# url = "https://www.creditchina.gov.cn/xinyongfuwu/zhongdianguanzhushixinmingdan/"
base_url = "https://public.creditchina.gov.cn/private-api/typeNameAndCountSearch"
end_page = input("请输入要爬取的结束页：")

all_content = []
for p in range(1,int(end_page)+1):
    params = {
        'keyword':'',
        'searchState':'1',
        # 'entityType':'1, 2, 3, 7',
        'type':'重点关注',
        'page':p,
        'pageSize':'10',
        '_':'1585136202916'
    }

    #发送HTTP请求
    response=requests.get(url=base_url,headers=header,params=params)
    response.encoding = "utf-8"
    #获得网站响应的数据
    html = response.json()
    # print(html)
    # print(html['data']['list'])

    new_url = "https://public.creditchina.gov.cn/private-api/typeSourceSearch"
    for item in html['data']['list']:
        # print(item['name'])
        keyword = item['name']
        new_params = {
            'source':'',
            'type':'重点关注',
            'searchState':'1',
            'entityType':'1',
            'scenes':'defaultscenario',
            'keyword':keyword,
            'page':'1',
            'pageSize':'10'
        }
        # 再次发送HTTP请求
        new_response = requests.get(url=new_url, headers=header, params=new_params)
        new_response.encoding = "utf-8"
        # 获得网站响应的数据
        new_html = new_response.json()
        # print(new_html['data'])
        # print(new_html['data']['list'])

        for i in new_html['data']['list']:
            # print(i['entity'])
            all_content.append(i['entity'])
            print(all_content)

#使用csv库写入csv文件
with open("chengxin_信用中国.csv","w",newline="") as fp:
    for item in all_content:
        writer = csv.writer(fp)
        writer.writerow(item.values())
