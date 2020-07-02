#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:Ruci
# datetime:2020/3/12 15:06
# software: PyCharm


import requests,tqdm,re,os
from lxml import etree
from bs4 import BeautifulSoup

# ---- tqdm 包安装，未安装，修改main()函数的tqdm方法。只需要删除tqdm即可



header={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}

def Home(content,page='1'):
    '''
    被搜索的所有栏目
    :param content:被搜索参数
    :param page: 页码
    :return: 源代码
    '''
    url='https://so.csdn.net/so/search/s.do?p=%s&q=%s'%(page,content)
        # 'https://so.csdn.net/so/search/s.do?p=1&q=python3'
    # print(url)
    response=requests.get(url,headers=header).content.decode("utf-8")
    return response

def resolver_Home(response):
    '''
    解析网页，只爬取博客。(不爬取下载，讨论内容)
    :param response:html
    :return:页面内url信息
    '''
    tree=etree.HTML(response)
    urls=tree.xpath("//dl[@class='search-list J_search']/dt//a/@href")
    bs=tree.xpath("//dl[@class='search-list J_search']/dt//span/text()")
    #这句代码的作用？
    urls=[urls[i*2] for i in range(len(bs)) if bs[i]=='博客']
    return urls

def get_content(url):
    '''
    单个页面信息
    :param url:
    :return: 响应
    '''
    response=requests.get(url,headers=header).content.decode()
    # print(response)
    return response

def parse_content(html):
    '''
    html文件解析
    :param html:
    :return: 标题，内容
    '''
    tree=etree.HTML(html)
    try:
        title=tree.xpath("//h1[@class='title-article']//text()")[0]
    except:
        title='未检测到标题'
    # print(title)
    content=tree.xpath("//div[@id='content_views']//text()")
    content=[t.strip('\n \t') for t in content]
    content='\n'.join(content[i] for i in range(len(content)) if content[i]!='')
    return title,content

def save_file(title,content,wt):
    '''
    保存文件。
    文件tree://logs/wt(搜索内容)/title(博客标题).txt
    :param title: 博客标题
    :param content: 内容
    :param wt: 搜索内容
    :return:
    '''
    if(os.path.exists('logs')==0):
        os.mkdir('logs')
    if(os.path.exists('logs/%s'%(wt))==0):
        os.mkdir('logs/%s'%(wt))
    title=title.replace('\\',' ').replace('/',' ').replace(':',' ').replace('*',' ').replace('?',' ') \
        .replace('"', ' ').replace('<',' ').replace('>',' ').replace('|',' ')
    with open('logs/%s/%s.txt'%(wt,title),'w',encoding='utf-8') as f:
        f.write(content)

def main(content,page):
    for i in tqdm.tqdm(range(1,page+1)):
        wt=content
        html=Home(wt,i)
        urls=resolver_Home(html)
        for url in urls:
            html=get_content(url)
            title,content=parse_content(html)
            save_file(title,content,wt)

if __name__=='__main__':
    a=input("搜索内容:")
    b=int(input("爬取多少页:"))
    main(a,b)
    print('爬取成功！')
