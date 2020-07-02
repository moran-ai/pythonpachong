import requests
import csv
import pandas as pd
import json


headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
"Cookie":"AD_RS_COOKIE=20080918; _trs_uv=k856vfl4_6_9d0d; _trs_ua_s_1=k856vfl4_6_i5s"
}

base_url="https://public.creditchina.gov.cn/private-api/typeNameAndCountSearch"
end_page = input("请输入结束页：")

for page in range(1, int(end_page)+1):
    params = {
        'keyword': '',
        'searchState': '1',
        'type': '重点关注',
        'page': page,
        'pageSize': '10',
        '_': '1585110189752',
    }
    url = base_url
    # 获取总的数据
    response = requests.get(url, headers=headers, params=params)
    response.encoding='utf-8'
    rep = response.json()
    # print(rep)
    items = rep['data']['list']
    # print(name, count, tyshxydm, zzjgdm, entity_type)

    # # 获取每一个数据的内容
    # url1 = 'https://public.creditchina.gov.cn/private-api/typeSourceSearch'
    # for item in items:
    #     keyword = item['name']
    #     params1 = {
    #         'source': '',
    #         'type': '重点关注',
    #         'searchState': '1',
    #         'scenes': 'defaultscenario',
    #         'keyword': keyword,
    #         'page': '1',
    #         'pageSize': '10',
    #     }
    #     res = requests.get(url1, headers=headers, params=params1)
    #     res.encoding = 'utf-8'
    #     resp = res.json()

    # 存储为csv文件
    with open("chengxinchina.csv", 'w', newline='') as f:
        for item in items:

            writer = csv.writer(f)
            writer.writerow(item.values())

        # df = pd.DataFrame(data=resp)
        # df.to_csv('cn.csv', encoding='utf-8')
        # print(df)


"""
# encoding:gbk
import requests
import json
import csv


# 发送请求
def request(url, header, param):
    response = requests.get(url, headers=header, params=param)
    response.encoding = 'utf-8'
    html = response.json()

    return html


# 保存csv
def save_csv(item_dic):
    with open('xinyong.csv', 'a', encoding='utf-8', newline='') as file:
        f = csv.writer(file)
        f.writerow(item_dic.values())


# 解析数据
def analysis(html):
    item = html['data']['list']
    item_dic = {}
    for i in item:
        item_dic['主题类型'] = i['name']
        item_dic['统一社会信用代码'] = str(i['tyshxydm']) + '\t'
        item_dic['记入类型(重点关注名单)'] = i['count']
        # 保存
        save_csv(item_dic)


def main():
    url = "https://public.creditchina.gov.cn/private-api/typeNameAndCountSearch"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Cookie": "AD_RS_COOKIE=20080918; _trs_uv=k856vfl4_6_9d0d; _trs_ua_s_1=k856vfl4_6_i5s"
    }
    title = ['name', 'tyshxydm', 'count']
    end_page = input('输入结束叶:')
    filename = 'xinyong.csv'
    for page in range(1, int(end_page) + 1):
        param = {
            'keyword': '',
            'searchState': '1',
            'entityType': '1,2,3,7',
            'type': '重点关注',
            'page': page,
            'pageSize': '10',
            '_': '1585110189752',
        }
        html = request(url, header, param)
        analysis(html)


if __name__ == '__main__':
    main()

"""