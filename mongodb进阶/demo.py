# encoding:gbk
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

base_url = 'https://mongoing.com/page/'
headers = {
'referer':'https://mongoing.com/',
'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
'x-requested-with':'XMLHttpRequest'
}

all_content = []
end_page = input('请输入加载的页面：')
for page in range(1, int(end_page)+1):
    url = base_url + str(page)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    rep = response.text
    # filename = str(page) + '.html'
    # with open(filename, 'w', encoding='utf-8') as f:
    #     f.write(rep)
    # 数据解析
    soup = BeautifulSoup(rep, 'lxml')

    # 获取每一个标签的内容
    article = soup.select('div.content article.excerpt-text')

    # 存储链接和页码
    url_data = {
        'url': url,
        'page': page
    }
    all_content.append(url_data)
    # 组合数据
    for i in range(len(article)):
        # 标题
        title = article[i].h2.text

        # 时间
        time = article[i].time.text

        # 作者
        author = article[i].find('span', class_='author').text

        # 评论字段
        comment = article[i].find('a', class_='pc').text

        # 摘要
        note = article[i].find('p', class_='note').text

        c = {
            'id': (i+1),
            'title': title,
            'time': time,
            'author': author,
            'comment': comment,
            'note': note
        }
        all_content.append(c)
# print(str(all_content))

# 连接数据库
client = MongoClient()

# 创建数据库
db = client.mog_data

# 访问数据库
column = db.mog

# 插入数据
# column.insert_many(all_content)

# 查询一条数据
# find_one = column.find_one({'page': 1})
# print(find_one)

# # 查询所有数据
# find_all = column.find()
# print(find_all)
# 查询带条件的所有数据
# find_all = column.find({'id': 1})
# print(find_all)
#
# # 查询id大于7   $gt
# # find_all = column.find({
# #     'id': {'$gt': 7}
# # })
#
# # 查询id小于7   $lt
# # find_all = column.find({
# #     'id': {'$lt': 7}
# # })
#
# 多条件查询 $and  $or
# find_all = column.find({
#     '$and':[
#         {'id': {'$gt': 7}},
#         {'time': '2020-01-22'}
#     ]
# })
# print(type(find_all))
# for data in find_all:
#     print(data)

# # 更新
# # 更新一条数据
# update_one = column.update_one(
#     {'page': 1},
#     {'$set': {'url': 'https://mongoing.com/page/1-update'}}
# )
#
# data1 = column.find_one({'page': 1})
# # print(data1)
#
# # 更新多条数据
# update_all = column.update_many(
#     {'id': 1},
#     {'$set': {'time': '未知'}}
# )
# data2 = column.find({'id': 1})
# # for data in data2:
# #     print(data)
#
# # 删除
# # 删除一条记录
# # column.delete_one({'id': 1})
# # all = column.find()
#
# # 删除多条记录
# column.delete_many({'id': 2})
# all = column.find()
# for data in all:
#     print(data)

