# encoding:gbk
import requests
import time
import psutil
import os
import threading
from fake_useragent import UserAgent
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

def head():
    """
    随机生成请求头
    :return:
    """
    headers = {
        'User-Agent': str(UserAgent().random)
    }
    return headers

def tishi():
    choices = input('请按照序号顺序进行: 1.单线程  2.多线程  3.多进程:')
    return choices

def stripText(textlist):
    """
    将文本转为字符串，并去掉其中的\n,\t,\r,/等字符

    :param textlist:
    :return:
    """
    star_list = ""
    for item in textlist:
        item_str = item.strip().replace('\n','').replace('\t', '').replace('\r','').replace('-','')
        # item_str = item.strip()  当参数为空时，默认删除字符串两端的空白符(包括'\n','\t','\r','')
        if item_str != '':
            if star_list != '':
                star_list = star_list + ',' + item_str
            else:
                star_list = item_str
    return star_list

def downMP4(item):
    """
    下载视频到本地
    :param item: 爬取网页的url
    :return:
    """
    # 设置下载开始时间
    start_time = time.time()

    # 构造详细页url
    video_page_url = item

    # 详细页发送请求
    video_page_response = requests.get(url=video_page_url, headers=head())
    video_page_response.encoding = video_page_response.apparent_encoding
    video_page_rep = video_page_response.text

    # 构建详细页解析对象
    tree_video = etree.HTML(video_page_rep)
    video_xapth_src = "//div/video/@src"

    # 解析视频链接
    video_url = stripText(tree_video.xpath(video_xapth_src))
    print(video_url)

    # 解析视频名称
    video_name_xpath = '//div/div/div/h1/text()'
    video_name = stripText(tree_video.xpath(video_name_xpath))

    # 获得当前线程
    thred = threading.current_thread()

    # 获得当前进程
    process = psutil.Process(os.getpid())

    # 打印进程与线程的名称和id
    print('当前线程名称为:%s, ID为:%s, 进程名称为:%s, ID为%s'
          % (thred.getName(), thred.ident, process.name(), process.pid))

    # 发起请求，获得视频文件
    video_response = requests.get(url=video_url, headers=head())
    MP4_rep = video_response.content

    # 存储视频文件
    with open(video_name + '.MP4', 'wb') as f:
        f.write(MP4_rep)

    # 设置下载完成时间
    finshtime = time.time() - start_time
    return video_name + '.MP4 用时为：' + str(finshtime) + '秒'

def main():
    """
    获取主页面信息，进行线程爬取
    :return:
    """
    # 主页面url
    url = 'http://www.aoao365.com/ys/hshy'
    # 主页面发送请求
    response = requests.get(url, headers=head())
    response.encoding = response.apparent_encoding
    rep = response.text
    with open('微视频.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    # 构建主页面解析对象
    tree = etree.HTML(rep)

    # 主页面所有视频信息xpath
    video_page_xpath = "//div[@class='layui-col-xs6 layui-col-sm6 layui-col-md3']/div[@class='video_con']/a/@href"

    # 获得前6个视频的xpath信息
    item_list = tree.xpath(video_page_xpath)[:6]
    # 设置线程开始时间
    start_time = time.time()

    while True:
        choices = tishi()
        if choices == '1':
            print('正在使用单线程')
            print('*'*80)
            for item in item_list:
                result = downMP4(item)
                print(result)
            finshTime = time.time() - start_time
            print('下载总时长为：' + str(finshTime) + '秒')
            print('单线程爬取完成！')
            print('*'*80)
            choices = tishi()

        if choices == '2':
            print('正在使用多线程')
            print('-'*80)
            with ThreadPoolExecutor(max_workers=4) as excutor:
                # 提交线程
                futures = excutor.map(downMP4, item_list)
            for future in futures:
                print(future)
            finshTime = time.time() - start_time
            print('下载总时长为：' + str(finshTime) + '秒')
            print('多线程爬取完成！')
            print('-'*80)
            choices = tishi()

        if choices == '3':
            print('正在使用多进程')
            print('='*80)
            with ProcessPoolExecutor(max_workers=4) as excutor:
                # 提交进程
                futures = excutor.map(downMP4, item_list)
            for future in futures:
                print(future)

            # 设置线程完成时间
            finshTime = time.time() - start_time
            print('下载总时长为：' + str(finshTime) + '秒')
            print('多进程爬取完成！')
            print('='*80)
        print('三种线程爬取完毕！')

        break
if __name__ =="__main__":
    main()