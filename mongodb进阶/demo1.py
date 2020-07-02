import requests
from lxml import etree
from pymongo import MongoClient

# 格式处理
def stripText(textlist):
    """
    将文本转为字符串，并去掉其中的\n,\t,\r,/等字符

    :param textlist:
    :return:
    """
    star_list = ""
    for item in textlist:
        item_str = item.strip().replace('\n','').replace('\t', '').replace('\r','').replace('/', '').replace('-','')
        # item_str = item.strip()  当参数为空时，默认删除字符串两端的空白符(包括'\n','\t','\r','')
        if item_str != '':
            if star_list != '':
                star_list = star_list + ',' + item_str
            else:
                star_list = item_str
    return star_list

url = 'https://segmentfault.com/api/timelines/recommend'
headers = {
'cookie':'ga=GA1.2.125993912.1574411818; Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1574411819,1574411959; __gads=ID=8ed2a7b2ead1cca7:T=1581756420:S=ALNI_MYc3ZQ-9ODP9MC3CGEVhHbbq2iPrw; PHPSESSID=web2~9l1aetr9pu1uercmkh9a7da06v; _gid=GA1.2.1898003754.1585390467; _gat_gtag_UA_918487_8=1',
'referer':'https://segmentfault.com/',
'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
'x-requested-with':'XMLHttpRequest',
'Connection':'close'
}

all_content = []
all_content1 = []
end_page = input('请输入尾页：')
for page in range(1, int(end_page)+1):
    params = {
        'page': str(page),
        '_': 'd18d32757c2d83650295715a48e9f965'
    }
    response = requests.get(url, params=params, headers=headers)
    response.encoding = 'utf-8'
    rep = response.json()

    url_data = {
        'url': url,
        'page': page
    }
    all_content.append(url_data)
    data = rep['data']
    for d in data:
        line = d['url']
        for i in range(len(line)):
            new_url = 'https://segmentfault.com' + line
            response_1 = requests.get(new_url, headers=headers)
            response_1.encoding = 'utf-8'
            rep_1 = response_1.text
            item_dic = {}
            tree = etree.HTML(rep_1)

            # 标题
            name_xpath = "//h1[@id='sf-article_title']/a/text()"
            name = stripText(tree.xpath(name_xpath))
            item_dic['name'] = name

            # 作者
            author_xpath = "//strong[@class='align-self-center']/text()"
            author = stripText(tree.xpath(author_xpath))
            item_dic['autor'] = author

            # 时间
            time_xpath = "//div[@class='font-size-14']/span[@class='text-secondary ml-2']/text()"
            time = stripText(tree.xpath(time_xpath))
            item_dic['time'] = time
            # 内容
            content_xpath = "//article[@class='article fmt article-content']//text()"
            content = stripText(tree.xpath(content_xpath))
            item_dic['content'] = content
            all_content.append(item_dic)
            all_content.append(i+1)
print(all_content)
        # for i in all_content:
        #     print(i)

        # data = {
        #     'id': d['id'],
        #     'url': url_data['url'],
        #     'page': url_data['page'],
        #     'name': name,
        #     'author': author,
        #     'time': time,
        #     'content': content
#         # }
# client = MongoClient()
# #
# # # 创建数据库
# # db = client.Segs
# #
# # # 访问数据库集合
# # column = db.infos

# 插入数据
# column.insert_many(all_content)

# 查询一条数据
# find_one = column.find_one({'page': 2})
# print(find_one)

# 查询所有数据
# find_all = column.find()
# for d in find_all:
#     print(d)


# 更新数据
# update_one = column.update_one(
#     {'page': 1},
#     {'$set': {'url': 'https://segmentfault.com/api/timelines/recommend/update_one'}}
# )
# data1 = column.find_one({'page': 1})
# print(data1)

# 更新多条数据
# update_all = column.update_many(
#     {'page': 1},
#     {'$set': {'time': '未知'}}
# )
# data1 = column.find({'page': 1})
# for d in data1:
#     print(d)
