# encoding:gbk
import requests
import psutil
import os
import threading
import time
from fake_useragent import UserAgent
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
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

    # 详细页url
    video_page_url = item
    video_page_response = requests.get(url=video_page_url, headers=headers)
    video_page_response.encoding = video_page_response.apparent_encoding
    video_page_rep = video_page_response.text
    print(video_page_response.status_code)
    tree_video = etree.HTML(video_page_rep)
    video_xapth_src = "//div/video/@src"

    # 视频的url
    video_url = stripText(tree_video.xpath(video_xapth_src))
    print(video_url)

    # 视频名称
    video_name_xpath = '//div/div/div/h1/text()'
    video_name = stripText(tree_video.xpath(video_name_xpath))
    # print(video_name)

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
    with open(video_name + '.MP4', 'wb') as f:
        f.write(MP4_rep)

    # 完成时间
    finshtime = time.time() - start_time
    return video_name + '.MP4 用时为：' + str(finshtime) + '秒'

def main():
    url = 'http://www.aoao365.com/ys/hshy'
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    # print(response.status_code)
    rep = response.text
    with open('微视频.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    # 构建xpath解析对象
    tree = etree.HTML(rep)
    video_page_xpath = "//div[@class='layui-col-xs6 layui-col-sm6 layui-col-md3']/div[@class='video_con']/a/@href"
    # 所有的视频信息
    item_list = tree.xpath(video_page_xpath)[:6]
    # print(item_list)
    start_time = time.time()

    # 单个线程
    print('这是单进程')
    print('*'*100)
    for item in item_list:
        result = downMP4(item)
        print(result)
    finshTime = time.time() - start_time
    print('下载总时长为：' + str(finshTime) + '秒')

    # 多线程
    # print('这是多线程')
    # print('-'*100)
    # with ThreadPoolExecutor(max_workers=4) as excutor:
    #     # 提交线程
    #     futures = excutor.map(downMP4, item_list)
    # for future in futures:
    #     print(future)
    # finshTime = time.time() - start_time
    # print('下载总时长为：' + str(finshTime) + '秒')

    # 多进程
    # print('这是多进程')
    # print('='*100)
    # with ProcessPoolExecutor(max_workers=4) as excutor:
    #     # 提交进程
    #     futures = excutor.map(downMP4, item_list)
    # for future in futures:
    #     print(future)
    # # 总的完成时间
    # finshTime = time.time() - start_time
    # print('下载总时长为：' + str(finshTime) + '秒')

if __name__ =="__main__":
    main()
