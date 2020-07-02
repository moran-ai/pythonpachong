import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from lxml import etree

base_url = 'http://www.dili360.com/Bbs/column/23576/'
headers = {
'Host': 'www.dili360.com',
'Referer': 'http://www.dili360.com/Bbs/column/23576/4.htm',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
}
all_content = []
end_page = input('请输入尾页:')
for page in range(1, int(end_page)+1):
    url = base_url + str(page) + '.htm'
    response = requests.get(url,  headers=headers)
    response.encoding ='utf-8'
    rep = response.text
    # print(rep)
    # filename = '地理' + str(page) + '.htm'
    # with open(filename, 'w', encoding='utf-8') as f:
    #     f.write(rep)

    soup = BeautifulSoup(rep, 'lxml')

    detail = soup.select('ul.article-list li div.detail')
    # print(detail)

    # 存储链接和页码
    url_data = {
        'url': url,
        'page': page
    }
    all_content.append(url_data)
    # 组合数据
    for i in range(len(detail)):
        # 标题
        title = detail[i].h3.text

        # 时间和作者
        time_author = detail[i].find('p', class_='tips').text.strip().replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '').replace('\xa0', '')

        # 内容
        content = detail[i].find('p', class_='desc').text
        # print(content)

        c = {
            'id': (i+1),
            'title': title,
            'time_author': time_author,
            'content': content
        }
        all_content.append(c)
# print(all_content)

client = MongoClient()

# 创建数据库
db = client.dl

# 创建数据库集合
column = db.dli

# 插入数据
column.insert_many(all_content)

# 查询一条数据
# find_one = column.find_one({'page': 1})
# print(find_one)

# 查询所有数据
# find_all = column.find()
# for p in find_all:
#     print(p)
#
# # 查询id为1的所有数据
# find_all = column.find({'id': 1})
# for p in find_all:
#     print(p)
#
# # 查询id大于5
# find_all = column.find({
#     'id': {'$gt': 5}
# })
# for p in find_all:
#     print(p)
#
# # 多条件查询
# find_all = column.find({
#     '$and':[
#         {'id': {'$gt': 5}},
#         {'title': '走进大凉山'}
#     ]
# })
# print(type(find_all))
# for data in find_all:
#     print(data)

# # 更新数据
# update_one = column.update_one(
#     {'page': 1},
#     {'$set':{'url':'http://www.dili360.com/Bbs/column/update'}}
# )
# data1 = column.find_one({'page': 1})
# print(data1)
#
# # 更新多条数据
# update_all = column.update_many(
#     {'id': 1},
#     {'$set': {'time_author': '未知'}}
# )
# data1 = column.find({'id': 1})
# for data in data1:
#     print(data)
#
# # 删除一条数据
# column.delete_one({'id': 1})
# all = column.find()
# for a in all:
#     print(a)
#
# # 删除多条数据
# column.delete_many({'id': 2})
# all = column.find()
# for a in all:
#     print(a)

