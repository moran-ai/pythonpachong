# encoding:gbk
import requests
import time
# 线程模块
import threading
# 进程模块
import psutil
import os
import asyncio
import aiohttp
from fake_useragent import UserAgent
from lxml import etree
# 线程池包
from concurrent.futures import ThreadPoolExecutor
# 进程池包
from concurrent.futures import ProcessPoolExecutor

headers = {
    'User-Agent': str(UserAgent().random)
}

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
    # 开始时间
    start_time = time.time()
    video_page_url = 'http://699pic.com' + item
    video_page_response = requests.get(url=video_page_url, headers=headers)
    video_page_response.encoding =  video_page_response.apparent_encoding
    video_page_rep =  video_page_response.text
    print( video_page_response.status_code)
    tree_video = etree.HTML(video_page_rep)
    video_xapth_src = "//div/video/source/@src"
    # 视频的url
    video_url = 'http:'+ stripText(tree_video.xpath(video_xapth_src))
    print(video_url)

    # 视频名称
    video_name_xpath = '//div/div/div/h1/text()'
    video_name = stripText(tree_video.xpath(video_name_xpath))

    # 获得当前线程
    thred = threading.current_thread()
    # 获得当前进程
    process = psutil.Process(os.getpid())
    print('当前线程名称为:%s, ID为:%s, 进程名称为:%s, ID为%s'
          % (thred.getName(), thred.ident, process.name(), process.pid))

    # 发起请求，获得视频文件
    video_response = requests.get(url=video_url, headers=headers)
    MP4_rep = video_response.content
    print(video_response.status_code)

    # 存储视频文件
    with open(video_name+'.MP4', 'wb') as f:
        f.write(MP4_rep)
    # 完成时间
    finshTime = time.time() - start_time
    return video_name+'.MP4 用时为：' + str(finshTime) + '秒'

def call_back(res):
    """
    :param res: 当前线程的参数,downMP4的参数
    :return: 返回 return video_name+'.MP4 用时为：' + str(finshTime) + '秒'
    """
    result = res.result()  # 当前线程的返回值
    print(result)

def parsePafe():
    url = 'http://699pic.com/media/video-1142643.html'
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    rep = response.text
    print(response.status_code)
    with open('英雄.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    # 构建xpath解析对象
    tree = etree.HTML(rep)
    video_xpath_page = "//div[@class='search-video-wrap']/div[@class='video-list clearfix']/ul/li/a[1]/@href"
    # 所有的视频信息
    item_list = tree.xpath(video_xpath_page)[:6]
    print(item_list)
    start_time = time.time()

    # 单线程
    # for item in item_list:
    #     result = downMP4(item)
    #     print(result)

    # 多线程写法1
    # # 创建线程池
    # max_workers 最大线程数
    # excutor = ThreadPoolExecutor(max_workers=4)
    #
    # for item in item_list:
    #     excutor.submit(downMP4, item).add_done_callback(call_back)
    # # 关闭多线程
    # excutor.shutdown(True)

    # 多线程写法2
    with ThreadPoolExecutor(max_workers=4) as excutor:
        # 提交线程
        futures = excutor.map(downMP4, item_list)
    for future in futures:
        print(future)

    # 进程池
    # 写法1
    # excutor = ProcessPoolExecutor(max_workers=4)
    # for item in item_list:
    #     excutor.submit(downMP4, item).add_done_callback(call_back)
    # # 关闭多进程
    # excutor.shutdown(True)

    # 进程池
    # 写法2
    # with ProcessPoolExecutor(max_workers=4) as excutor:
    #     # 提交进程
    #     futures = excutor.map(downMP4, item_list)
    # for future in futures:
    #     print(future)
    #
    # 总的完成时间
    finshTime = time.time() - start_time
    print( '下载总时长为：' + str(finshTime) + '秒')

if __name__ == "__main__":
    parsePafe()
