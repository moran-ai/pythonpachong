# encoding:gbk
import requests
import time
# �߳�ģ��
import threading
# ����ģ��
import psutil
import os
import asyncio
import aiohttp
from fake_useragent import UserAgent
from lxml import etree
# �̳߳ذ�
from concurrent.futures import ThreadPoolExecutor
# ���̳ذ�
from concurrent.futures import ProcessPoolExecutor

headers = {
    'User-Agent': str(UserAgent().random)
}

def stripText(textlist):
    """
    ���ı�תΪ�ַ�������ȥ�����е�\n,\t,\r,/���ַ�

    :param textlist:
    :return:
    """
    star_list = ""
    for item in textlist:
        item_str = item.strip().replace('\n','').replace('\t', '').replace('\r','').replace('-','')
        # item_str = item.strip()  ������Ϊ��ʱ��Ĭ��ɾ���ַ������˵Ŀհ׷�(����'\n','\t','\r','')
        if item_str != '':
            if star_list != '':
                star_list = star_list + ',' + item_str
            else:
                star_list = item_str
    return star_list

def downMP4(item):
    # ��ʼʱ��
    start_time = time.time()
    video_page_url = 'http://699pic.com' + item
    video_page_response = requests.get(url=video_page_url, headers=headers)
    video_page_response.encoding =  video_page_response.apparent_encoding
    video_page_rep =  video_page_response.text
    print( video_page_response.status_code)
    tree_video = etree.HTML(video_page_rep)
    video_xapth_src = "//div/video/source/@src"
    # ��Ƶ��url
    video_url = 'http:'+ stripText(tree_video.xpath(video_xapth_src))
    print(video_url)

    # ��Ƶ����
    video_name_xpath = '//div/div/div/h1/text()'
    video_name = stripText(tree_video.xpath(video_name_xpath))

    # ��õ�ǰ�߳�
    thred = threading.current_thread()
    # ��õ�ǰ����
    process = psutil.Process(os.getpid())
    print('��ǰ�߳�����Ϊ:%s, IDΪ:%s, ��������Ϊ:%s, IDΪ%s'
          % (thred.getName(), thred.ident, process.name(), process.pid))

    # �������󣬻����Ƶ�ļ�
    video_response = requests.get(url=video_url, headers=headers)
    MP4_rep = video_response.content
    print(video_response.status_code)

    # �洢��Ƶ�ļ�
    with open(video_name+'.MP4', 'wb') as f:
        f.write(MP4_rep)
    # ���ʱ��
    finshTime = time.time() - start_time
    return video_name+'.MP4 ��ʱΪ��' + str(finshTime) + '��'

def call_back(res):
    """
    :param res: ��ǰ�̵߳Ĳ���,downMP4�Ĳ���
    :return: ���� return video_name+'.MP4 ��ʱΪ��' + str(finshTime) + '��'
    """
    result = res.result()  # ��ǰ�̵߳ķ���ֵ
    print(result)

def parsePafe():
    url = 'http://699pic.com/media/video-1142643.html'
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    rep = response.text
    print(response.status_code)
    with open('Ӣ��.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    # ����xpath��������
    tree = etree.HTML(rep)
    video_xpath_page = "//div[@class='search-video-wrap']/div[@class='video-list clearfix']/ul/li/a[1]/@href"
    # ���е���Ƶ��Ϣ
    item_list = tree.xpath(video_xpath_page)[:6]
    print(item_list)
    start_time = time.time()

    # ���߳�
    # for item in item_list:
    #     result = downMP4(item)
    #     print(result)

    # ���߳�д��1
    # # �����̳߳�
    # max_workers ����߳���
    # excutor = ThreadPoolExecutor(max_workers=4)
    #
    # for item in item_list:
    #     excutor.submit(downMP4, item).add_done_callback(call_back)
    # # �رն��߳�
    # excutor.shutdown(True)

    # ���߳�д��2
    with ThreadPoolExecutor(max_workers=4) as excutor:
        # �ύ�߳�
        futures = excutor.map(downMP4, item_list)
    for future in futures:
        print(future)

    # ���̳�
    # д��1
    # excutor = ProcessPoolExecutor(max_workers=4)
    # for item in item_list:
    #     excutor.submit(downMP4, item).add_done_callback(call_back)
    # # �رն����
    # excutor.shutdown(True)

    # ���̳�
    # д��2
    # with ProcessPoolExecutor(max_workers=4) as excutor:
    #     # �ύ����
    #     futures = excutor.map(downMP4, item_list)
    # for future in futures:
    #     print(future)
    #
    # �ܵ����ʱ��
    finshTime = time.time() - start_time
    print( '������ʱ��Ϊ��' + str(finshTime) + '��')

if __name__ == "__main__":
    parsePafe()
