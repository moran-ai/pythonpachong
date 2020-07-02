#引入库文件
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
from pymongo import MongoClient

import pymysql
import uuid

import csv
import pandas as pd
#1.构建基础url
word=input("请输入搜索关键字：")
base_url="https://search.51job.com/list/000000,000000,0000,00,9,99,"+word+",2,"
end_url=".html"
#2.构造U-A
header={
    "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
}
#3.构造param
param={
    'lang':'c',
    'postchannel':'0000',
    'workyear':'99',
    'cotype':'99',
    'degreefrom':'99',
    'jobterm':'99',
    'companysize':'99',
    'providesalary':'99',
    'lonlat':'0,0',
    'radius':'-1',
    'ord_field':'0',
    'confirmdate':'9',
    'dibiaoid':'0',
    'specialarea':'00',
}
#4.循环获取搜索页内容，并持久化
end_page=input("请输入结束页：")
for page in range(1,int(end_page)+1):
    #构造完整URL
    url=base_url+str(page)+end_url
    #发送HTTP请求
    response=requests.get(url,params=param,headers=header)
    #获得响应数据
    html=response.content.decode("GBK")

    #5.数据解析：获取职位信息
    #bs4  xpath
    #soup=BeautifulSoup(html,'lxml')
    html=etree.HTML(html)
    #div 类名el
    el=html.xpath('//div[@id="resultList"]/div[@class="el"]')
    #存储数据
    content=[]
    #循环获取
    for i in range(len(el)):
        #title_content=title[i].attrs['title']
        title_content=el[i].xpath('.//p/span/a/@title')
        #company_content=company[i].text
        company_content = el[i].xpath('.//span[@class="t2"]/a/text()')
        #address_content=address[i+1].text
        address_content = el[i].xpath('.//span[@class="t3"]/text()')
        #salary_content=salary[i+1].text
        salary_content = el[i].xpath('.//span[@class="t4"]/text()')
        #time_content=time[i+1].text
        time_content=el[i].xpath('.//span[@class="t5"]/text()')
        #id_content=[]
        #id_content.append(uuid.uuid1())
        #构造一组数据
        c={
            'id':str(uuid.uuid1()),
            'title':title_content,
            'company':company_content,
            'address':address_content,
            'salary':salary_content,
            'time':time_content
        }
        content.append(c)
print(str(content))
#存储
#mysql数据库连接
connect = pymysql.connect(
            user = 'root',
            password = 'itcast',
            db = 'qiancheng',
            host = '127.0.0.1',
            port = 3306,
            charset = 'utf8'
            )
cursor = connect.cursor()#获得游标
#循环存储
for i in range(len(content)):
    cols=",".join('`{}`'.format(k) for k in content[i].keys())
    print(cols)
    cols_value=",".join('%({})s'.format(k) for k in content[i].keys())
    print(cols_value)
    sql = "insert into qs (%s) values (%s)"
    parm = sql % (cols, cols_value)
    print(parm)
    #使用execute()方法执行SQL语句
    cursor.execute(parm,content[i])
##增
##插入一条
#sql = "insert into infos(id,title,company,address,salary,time) values (%s,%s,%s,%s,%s,%s)"
#effect_row = cursor.execute(sql,(str(uuid.uuid1()),'(新增)HTML5游戏开发','深圳网易游戏开发公司','深圳-南山区','1-1.8万','04-02'))
##同时插入多条数据
#cursor.executemany(sql,[(str(uuid.uuid1()),'(新增1)HTML5游戏开发','深圳网易游戏开发公司','深圳-南山区','1-1.8万','04-02'),
#                        (str(uuid.uuid1()),'(新增2)HTML5游戏开发','深圳网易游戏开发公司','深圳-南山区','1-1.8万','04-02')])
#
##改
#sql = "update infos set title = %s where  time = '04-01'"
#effect_row=cursor.execute(sql,'已更新')
#
#
##删
#sql = "delete from infos where title = '已更新'"
#effect_row = cursor.execute(sql)

#提交数据
connect.commit()

#查询
#fetchone():获取下一行数据，第一次为首行；
sql = "SELECT * FROM infos"
cursor.execute(sql)
res1 = cursor.fetchone() #第一次执行
print(res1)
res2 = cursor.fetchone() #第二次执行
print(res2)
#fetchall():获取所有行数据源
res_all = cursor.fetchall()
print(str(res_all))
#移动游标：第一个值为移动的行数，整数为向下移动，负数为向上移动，
# mode指定了是相对当前位置移动，还是相对于首行移动
#mode='relative' 相对当前位置移动   mode='absolute'相对绝对位置移动
cursor.scroll(3,mode='absolute')
#fetchmany(4):获取下4行数
res_f = cursor.fetchmany(4)
print(res_f)
cursor.close()
connect.close()







