# coding:gbk
import re
import os
import requests
from bs4 import BeautifulSoup
def getHtml(url):
    r=requests.get(url,timeout=10)
    r.raise_for_status()
    r.encoding=r.apparent_encoding#��ֹ����
    return r.text
def savePic(link,name,id):
    url='https://pvp.qq.com/web201605/'+link
    html=getHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    print("���ڻ�ȡ{}������Ƥ������......".format(name),end='')
    cloName=soup.select('.pic-pf ul')[0].attrs['data-imgname']#Ѱ��Ƥ���ַ���
    count=cloName.count('&')#�ҵ�Ƥ������
    cloName=cloName.replace('&','')#ȥ&
    for i in range(10):#ȥ����
        cloName=cloName.replace(str(i),'')
    cloList=cloName.split('|')#�õ�Ƥ�������б�
    print("--->�ɹ�!")
    localPath='E:\picture\\tu'+name+'\\'#����ÿ��Ӣ�۵��ļ���
    if not os.path.exists(localPath):  # �½��ļ���,�ж��Ƿ����
        os.mkdir(localPath)
    basepic_link='https://game.gtimg.cn/images/yxzj/img201606/heroimg/'
    for i in range(1,count+1):
        pic = str(id) + '/' + str(id) + '-mobileskin-' + str(i) + '.jpg'
        pic_url=basepic_link+pic#�õ����յ�Ƥ��ͼƬ
        try:
            pic_re = requests.get(pic_url, timeout=10)
            print("��������{}-{}".format(name,cloList[i-1]),end='')
            open(localPath + cloList[i-1] + '.jpg', 'wb').write(pic_re.content)  # ����Ƥ��һһ��Ӧ���浽����
            print("--->�ɹ�!")
        except requests.exceptions.ConnectionError:
            print('�����쳣�����!��ǰͼƬ�޷�����')
    print("\r����{0}��Ӣ��Ƥ���������!".format(name))
def getLink(html):
    print("���ڲ�������Ӣ������......")
    soup=BeautifulSoup(html,'html.parser')
    heroList=soup.find_all('a',href=re.compile('herodetail/\d{3}.shtml'))#�������ͼƬ����
    print("��ȡӢ�����ӳɹ�!")
    for each in heroList:
        link=each.get('href')#��ȡӢ����������
        name=each.select('img')[0].get('alt')#��ȡӢ������
        _id=link[11:14]#���Ӣ�����
        savePic(link,name,_id)
    print("����Ӣ�۵�Ƥ���������!")
def main():
    url='https://pvp.qq.com/web201605/herolist.shtml'#��ҳ��
    html = getHtml(url)
    getLink(html)
    print("�������!")
main()
