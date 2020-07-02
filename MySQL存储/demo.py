import requests
from lxml import etree
import uuid

def stripText(textlist):
    """
    将文本转为字符串，并去掉其中的\n,\t,\r,/等字符

    :param textlist:
    :return:
    """
    star_list = ""
    for item in textlist:
        item_str = item.strip().replace('\n','').replace('\t', '').replace('\r','').replace('/', '').replace('-','').replace(' ', '')
        # item_str = item.strip()  当参数为空时，默认删除字符串两端的空白符(包括'\n','\t','\r','')
        if item_str != '':
            if star_list != '':
                star_list = star_list + ',' + item_str
            else:
                star_list = item_str
    return star_list

# url = 'http://csga.changsha.gov.cn/jjzd/csjj_index/topic_4169_1.shtml'
headers = {
'Cookie':'HWWAFSESID=1f6c773df74049b8a1; HWWAFSESTIME=1585618250580; ASP.NET_SessionId=wnmkkr4lswp4p0sr3kxjqs5u',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
all_content = []
base_url = 'http://csga.changsha.gov.cn/jjzd/csjj_index/topic_4169_'
end_page = input('请输入尾页：')
for page in range(1, int(end_page)+1):
    url = base_url + str(page) + '.shtml'
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    rep = response.text

    # with open('交通'+str(page)+'.html', 'w', encoding='utf-8') as f:
    #     f.write(rep)
    tree = etree.HTML(rep)
    item_xpath = "//div[@id='newsdata']/div[@class='info_list_top']/a[@class='morePointer']/@href"
    item_list = tree.xpath(item_xpath)
    # print(item_list)

    for item in item_list:
        new_url = item
        new_response = requests.get(new_url, headers)
        new_response.encoding = new_response.apparent_encoding
        new_rep = new_response.text
        # print(new_rep)
        new_tree = etree.HTML(new_rep)
        "//table/tbody/tr[2]/td[@class='et12']"
        count = new_tree.xpath("count(//table/tbody/tr)")
        # print(count)

        for i in range(2, int(count)):
            item_dic = {}

            item_dic["id"] = str(uuid.uuid1())
            # 违法时间
            time = stripText(new_tree.xpath("//table/tbody/tr["+str(i)+"]/td[2]//text()"))
            # print(time)
            item_dic['time'] = time

            # 违法地址
            addr = stripText(new_tree.xpath("//table/tbody/tr[" + str(i) + "]/td[3]//text()"))
            # print(addr)
            item_dic['addr'] = addr

            # 车牌号
            car_number = stripText(new_tree.xpath("//table/tbody/tr[" + str(i) + "]/td[4]//text()"))
            # print(car_number)
            item_dic['car_number'] = car_number

            # 车辆类型
            car_type = stripText(new_tree.xpath("//table/tbody/tr[" + str(i) + "]/td[5]//text()"))
            # print(car_type)
            item_dic['car_type'] = car_type

            # 违法行为
            act = stripText(new_tree.xpath("//table/tbody/tr[" + str(i) + "]/td[6]//text()"))
            # print(act)
            item_dic['act'] = act

            # 处罚标准
            strandrd = stripText(new_tree.xpath("//table/tbody/tr[" + str(i) + "]/td[7]//text()"))
            # print(strandrd)
            item_dic['strandrd'] = strandrd
            all_content.append(item_dic)
            # print(item_dic['id'])
# print(all_content)
import pymysql
# db = pymysql.connect(host="127.0.0.1",user="root", password="itcast", db="jiaotong")
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='itcast',
                     db='jiaotong')
cursor = db.cursor()

# 创建数据表
biao = """
create table student(
id int not null,
time varchar(64),
addr varchar(64),
car_number varchar(64),
car_type varchar(64),
act varchar(64),
strandrd varchar(64),
charset="utf8mb4")
"""
table = "student"
# data = {'time': '2019年12月8日', 'addr': '浏阳大道与环府路（政务中心）交叉路口', 'car_number': '湘AB8F61', 'car_type': '小型轿车', 'act': '16250_驾驶机动车违反道路交通信号灯通行的', 'strandrd': '记6分罚200'}
data = all_content[0]
# print(data)
cols = ",".join('`{}`'.format(k) for k in data.keys())
# print(cols)

cols_value = ",".join('%({})s'.format(k) for k in data.keys())
# print(cols_value)

# # 插入数据
# sql = "insert into " + table + "(%s) values(%s)"
# # print(sql)
# res_sql = sql % (cols, cols_value)

# 插入数据
try:
    with db.cursor() as cursor:
        # 插入数据
        sql = "insert into " + table + "(%s) values(%s)"
        res_sql = sql % (cols, cols_value)
        cursor.executemany(res_sql, all_content)
        db.commit()
finally:
    db.close()


# 查询数据
try:
    with db.cursor() as cursor:
        sql = "select * from student;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for data in result:
            ids = data[0]
            times = data[1]
            addrs = data[2]
            car_numbers = data[3]
            car_types = data[4]
            acts = data[5]
            strandrds = data[6]
            print("id=%s, time=%s, addr=%s, car_number=%s, car_type=%s, act=%s, strandrd=%s" %
                  (ids, times, addrs, car_numbers, car_types, acts, strandrds))
            db.commit()
except:
    print('查询错误')

db.close()

# print(res_sql)
# cursor.executemany(res_sql, all_content)
# db.commit()
# # # cursor.close()
# # db.close()
