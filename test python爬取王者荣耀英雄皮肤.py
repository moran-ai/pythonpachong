# coding:gbk
import re
import os
import requests
from bs4 import BeautifulSoup
def getHtml(url):
    r=requests.get(url,timeout=10)
    r.raise_for_status()
    r.encoding=r.apparent_encoding#防止乱码
    return r.text
def savePic(link,name,id):
    url='https://pvp.qq.com/web201605/'+link
    html=getHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    print("正在获取{}的所有皮肤链接......".format(name),end='')
    cloName=soup.select('.pic-pf ul')[0].attrs['data-imgname']#寻找皮肤字符串
    count=cloName.count('&')#找到皮肤数量
    cloName=cloName.replace('&','')#去&
    for i in range(10):#去数字
        cloName=cloName.replace(str(i),'')
    cloList=cloName.split('|')#得到皮肤名字列表
    print("--->成功!")
    localPath='E:\picture\\tu'+name+'\\'#创建每个英雄的文件夹
    if not os.path.exists(localPath):  # 新建文件夹,判断是否存在
        os.mkdir(localPath)
    basepic_link='https://game.gtimg.cn/images/yxzj/img201606/heroimg/'
    for i in range(1,count+1):
        pic = str(id) + '/' + str(id) + '-mobileskin-' + str(i) + '.jpg'
        pic_url=basepic_link+pic#得到最终的皮肤图片
        try:
            pic_re = requests.get(pic_url, timeout=10)
            print("正在下载{}-{}".format(name,cloList[i-1]),end='')
            open(localPath + cloList[i-1] + '.jpg', 'wb').write(pic_re.content)  # 名字皮肤一一对应保存到本地
            print("--->成功!")
        except requests.exceptions.ConnectionError:
            print('数据异常或错误!当前图片无法下载')
    print("\r所有{0}的英雄皮肤下载完成!".format(name))
def getLink(html):
    print("正在查找所有英雄链接......")
    soup=BeautifulSoup(html,'html.parser')
    heroList=soup.find_all('a',href=re.compile('herodetail/\d{3}.shtml'))#正则查找图片链接
    print("获取英雄链接成功!")
    for each in heroList:
        link=each.get('href')#获取英雄所在链接
        name=each.select('img')[0].get('alt')#获取英雄名字
        _id=link[11:14]#获得英雄序号
        savePic(link,name,_id)
    print("所有英雄的皮肤下载完成!")
def main():
    url='https://pvp.qq.com/web201605/herolist.shtml'#主页面
    html = getHtml(url)
    getLink(html)
    print("下载完成!")
main()
