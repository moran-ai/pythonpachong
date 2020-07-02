import requests
import re
import os
import time
class D(object):
    def __init__(self):
        self.url='https://www.kuaidaili.com/free/inha/'
    def getIP(self,page):
        '''
        :param page: 页数
        :return:
        爬取ip代理
        '''
        head={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
        }
        with open('logs/dl.txt', 'w', encoding='utf-8') as f:
            for i in range(1,page+1):
                url='https://www.kuaidaili.com/free/inha/%d/'%(i)
                print(url)
                time.sleep(2)
                response=requests.get(url=url,headers=head).content.decode()
                # print(response)
                par=r'<td data-title="IP">(.*?)</td>.*?<td data-title="PORT">(.*?)</td>'
                p=re.compile(par,re.S)
                html=p.findall(response)
                print(html)
                if(os.path.exists('logs')==0):
                    os.mkdir('logs')
                for t in html:
                    f.write(t[0]+' '+t[1]+'\n')
            print("爬取成功！")

    def codeIP(self,path='logs/goodcode.txt'):
        '''
        严重ip代理是否可用
        :param path: 保存ip代理路径
        :return:
        '''
        head={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
        }
        with open('logs/dl.txt','r',encoding='utf-8') as f:
            file=f.readlines()
        if (os.path.exists('logs') == 0):
            os.mkdir('logs')
        with open(path,"w",encoding='utf-8') as f:
            for t in file:
                tmp=t.replace('\n','').split(' ')
                ip={"http":"%s:%s"%(tmp[0],tmp[1])}
                url= "https://www.baidu.com/"
                print(ip['http'])
                try:
                    r=requests.get(url,headers=head,proxies=ip)
                    # print(r.status_code)
                    if(r.status_code==200):
                        f.write(tmp[0] + ' ' + tmp[1] + '\n')
                except:
                    print('ip异常')
        print('完成验证')

t=D()
# t.getIP(5)
t.codeIP('logs/dl.txt')
