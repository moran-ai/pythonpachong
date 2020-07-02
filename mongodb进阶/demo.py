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
end_page = input('��������ص�ҳ�棺')
for page in range(1, int(end_page)+1):
    url = base_url + str(page)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    rep = response.text
    # filename = str(page) + '.html'
    # with open(filename, 'w', encoding='utf-8') as f:
    #     f.write(rep)
    # ���ݽ���
    soup = BeautifulSoup(rep, 'lxml')

    # ��ȡÿһ����ǩ������
    article = soup.select('div.content article.excerpt-text')

    # �洢���Ӻ�ҳ��
    url_data = {
        'url': url,
        'page': page
    }
    all_content.append(url_data)
    # �������
    for i in range(len(article)):
        # ����
        title = article[i].h2.text

        # ʱ��
        time = article[i].time.text

        # ����
        author = article[i].find('span', class_='author').text

        # �����ֶ�
        comment = article[i].find('a', class_='pc').text

        # ժҪ
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

# �������ݿ�
client = MongoClient()

# �������ݿ�
db = client.mog_data

# �������ݿ�
column = db.mog

# ��������
# column.insert_many(all_content)

# ��ѯһ������
# find_one = column.find_one({'page': 1})
# print(find_one)

# # ��ѯ��������
# find_all = column.find()
# print(find_all)
# ��ѯ����������������
# find_all = column.find({'id': 1})
# print(find_all)
#
# # ��ѯid����7   $gt
# # find_all = column.find({
# #     'id': {'$gt': 7}
# # })
#
# # ��ѯidС��7   $lt
# # find_all = column.find({
# #     'id': {'$lt': 7}
# # })
#
# ��������ѯ $and  $or
# find_all = column.find({
#     '$and':[
#         {'id': {'$gt': 7}},
#         {'time': '2020-01-22'}
#     ]
# })
# print(type(find_all))
# for data in find_all:
#     print(data)

# # ����
# # ����һ������
# update_one = column.update_one(
#     {'page': 1},
#     {'$set': {'url': 'https://mongoing.com/page/1-update'}}
# )
#
# data1 = column.find_one({'page': 1})
# # print(data1)
#
# # ���¶�������
# update_all = column.update_many(
#     {'id': 1},
#     {'$set': {'time': 'δ֪'}}
# )
# data2 = column.find({'id': 1})
# # for data in data2:
# #     print(data)
#
# # ɾ��
# # ɾ��һ����¼
# # column.delete_one({'id': 1})
# # all = column.find()
#
# # ɾ��������¼
# column.delete_many({'id': 2})
# all = column.find()
# for data in all:
#     print(data)

