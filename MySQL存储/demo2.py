# encoding:gbk
import requests
from lxml import etree
import random
import pymysql
import uuid

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

base_url = 'http://www.stats.gov.cn/tjfw/sxqygs/gsxx/index'
end_page = input("请输入尾页:")

all_content = []
for page in range(1, int(end_page)+1):
    if page == 1:
        url = base_url + '.html'
    else:
        page = str(page)
        url = base_url + "_" + page + '.html'

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    rep = response.text
    # print(rep)

    tree = etree.HTML(rep)
    item_xpath = "//ul[@class='center_list_contlist']/li/a/@href"
    item_list = tree.xpath(item_xpath)
    # print(item_list)

    for item in item_list:
        item_dict = {}
        # 获得页面内容
        detail_url = "http://www.stats.gov.cn/tjfw/sxqygs/gsxx/" + item
        detail_response = requests.get(detail_url, headers=headers)
        detail_response.encoding = 'utf-8'
        detail_rep = detail_response.text

        item_dict["id"] = str(uuid.uuid1())
        # 企业名称
        detail_tree = etree.HTML(detail_rep)
        name = stripText(detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[1]/td[2]/p[@class='MsoNormal']//text()"))
        # print(name)
        item_dict["name"] = name

        # 企业地址
        addr = stripText(detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[2]/td[2]/p[@class='MsoNormal']//text()"))
        # print(addr)
        item_dict["addr"] = addr

        # 企业统一社会信用代码
        letter = stripText(detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[3]/td[2]/p[@class='MsoNormal']//text()")).strip()
        # print(letter)
        item_dict["letter"] = letter +'\t'

        # 法定代表人姓名
        deputy = stripText(detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[5]/td[2]/p[@class='MsoNormal']//text()"))
        # print(deputy)
        item_dict["deputy"] = deputy

        # 行政处罚决定书文号
        punish = stripText(detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[6]/td[2]/p[@class='MsoNormal']//text()"))
        # print(punish)
        item_dict["punish"] = punish

        # 违法事实
        law = stripText(detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[7]/td[2]/p[@class='MsoNormal']//text()"))
        # print(law)
        item_dict["law"] = law

        # 处罚类别1
        genre = stripText(detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[8]/td[2]/p[@class='MsoNormal']//text()"))
        # print(genre)
        item_dict["genre"] = genre

        # 处罚类别2
        genre2 = stripText(detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[9]/td[2]/p[@class='MsoNormal']//text()"))
        # print(genre2)
        item_dict["genre2"] = genre2

        # 处罚依据
        basis = stripText(detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[10]/td[2]/p[@class='MsoNormal']//text()"))
        # print(basis)
        item_dict["basis"] = basis

        # 处罚内容
        subtance = stripText(detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[11]/td[2]/p[@class='MsoNormal']//text()"))
        # print(subtance)
        item_dict["subtance"] = subtance

        # 处罚机关
        gear = stripText(
            detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[12]/td[2]/p[@class='MsoNormal']//text()"))
        # print(gear)
        item_dict["gear"] = gear

        # 处罚决定日期
        date = stripText(
            detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[13]/td[2]/p[@class='MsoNormal']//text()")).strip()
        # print(date)
        item_dict["date"] = date

        # 公示期限
        time = stripText(
            detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[14]/td[2]/p[@class='MsoNormal']//text()")).strip()
        # print(time)
        item_dict["time"] = time + '\t'

        # 当前状态
        status = stripText(
            detail_tree.xpath("//table[@class='MsoNormalTable']/tbody/tr[15]/td[2]/p[@class='MsoNormal']//text()"))
        # print(status)
        item_dict["status"] = status

        all_content.append(item_dict)
# print(all_content)
#
# # 连接数据库
db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='itcast',
    db='tongji',
    charset='utf8'
)
#
cursor = db.cursor()

# 创建数据表
biao = cursor.execute("""
create table sh(
id char(64),
name varchar(64),
addr varchar(64),
letter varchar(64),
deputy varchar(64),
punish varchar(64),
law varchar(64),
genre varchar(64),
genre2 varchar(64),
basis varchar(64),
subtance varchar(64),
gear varchar(64),
date varchar(64),
time varchar(64),
status varchar(64)
)
""")
table = 'sh'
data = all_content[0]
# print(data)
cols = ",".join('`{}`'.format(k) for k in data.keys())
# print(cols)

cols_value = ",".join('%({})s'.format(k) for k in data.keys())
# # print(cols_value)
# try:
#     with db.cursor() as cursor:
#         # 插入数据
#         sql = "insert into " + table + "(%s) values(%s)"
#         res_sql = sql % (cols, cols_value)
#         # print(res_sql)
#         cursor.executemany(res_sql, all_content)
#         db.commit()
# # finally:
# #     db.close()
# except:
#     print("插入数据出错")
# db.close()


# 查看数据
try:
    with db.cursor() as cursor:
        # 查询语句
        sql = 'select * from sh;'
        cursor.execute(sql)
        result = cursor.fetchall()
        for data in result:
            ids = data[0]
            names = data[1]
            addrs = data[2]
            letters = data[3]
            deputys = data[4]
            punishs = data[5]
            laws = data[6]
            genres = data[7]
            genre2s = data[8]
            basiss = data[9]
            subtances = data[10]
            gears = data[11]
            dates = data[12]
            times = data[13]
            statuss = data[14]
            # 拼接数据
            print("id=%s, names=%s, addr=%s, letters=%s, deputys=%s, punishs=%s, laws=%s, genress=%s, genre2ss=%s,"
                  "basisss=%s, subtancess=%s, gearss=%s, dates=%s, times=%s, statuss=%s" %
                  (ids, names, addrs, letters, deputys, punishs, laws, genres, genre2s, basiss,
                    subtances, gears, dates,times, statuss))
            db.commit()
except:
    print("查询错误")

db.close()

