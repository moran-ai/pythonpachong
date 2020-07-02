# encoding:gbk
import requests
import time
import threading
import psutil
import os
from fake_useragent import UserAgent
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

def head():
    headers = {
        'User-Agent': str(UserAgent().random)
    }
    return headers

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

def tishi():
    choices = input("�밴�����˳�����:1.���߳� 2.���߳� 3.�����:")
    return choices

def downMP4(item):
    # ��ʼʱ��
    start_time = time.time()

    # ��ϸҳurl
    video_page_url = 'http://699pic.com' + item
    video_page_response = requests.get(url=video_page_url, headers=head())
    video_page_response.encoding =  video_page_response.apparent_encoding
    video_page_rep =  video_page_response.text

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
    video_response = requests.get(url=video_url, headers=head())
    MP4_rep = video_response.content

    # �洢��Ƶ�ļ�
    with open(video_name+'.MP4', 'wb') as f:
        f.write(MP4_rep)
    # ���ʱ��
    finshTime = time.time() - start_time
    return video_name+'.MP4 ��ʱΪ��' + str(finshTime) + '��'

def main():
    url = 'http://699pic.com/media/video-1142643.html'
    response = requests.get(url, headers=head())
    response.encoding = response.apparent_encoding
    rep = response.text

    with open('Ӣ��.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    # ����xpath��������
    tree = etree.HTML(rep)
    video_xpath_page = "//div[@class='search-video-wrap']/div[@class='video-list clearfix']/ul/li/a[1]/@href"
    # ���е���Ƶ��Ϣ
    item_list = tree.xpath(video_xpath_page)[:6]

    start_time = time.time()

    while True:
        choises = tishi()
        if choises == '1':
            print('����ʹ�õ��߳�')
            print('*'*80)
            for item in item_list:
                result = downMP4(item)
                print(result)

            # �ܵ����ʱ��
            finshTime = time.time() - start_time
            print( '������ʱ��Ϊ��' + str(finshTime) + '��')
            print('���߳���ȡ��ϣ�')
            print('*'*80)
            choises = tishi()

        if choises == '2':
            print('����ʹ�ö��߳�')
            print('-'*80)
            with ThreadPoolExecutor(max_workers=4) as excutor:
                # �ύ�߳�
                futures = excutor.map(downMP4, item_list)
            for future in futures:
                print(future)

            # �ܵ����ʱ��
            finshTime = time.time() - start_time
            print( '������ʱ��Ϊ��' + str(finshTime) + '��')
            print('���߳���ȡ��ϣ�')
            print('-'*80)
            choises = tishi()

        if choises == '3':
            print('����ʹ�ö����')
            print('='*80)
            with ProcessPoolExecutor(max_workers=4) as excutor:
                # �ύ����
                futures = excutor.map(downMP4, item_list)
            for future in futures:
                print(future)

            # �ܵ����ʱ��
            finshTime = time.time() - start_time
            print( '������ʱ��Ϊ��' + str(finshTime) + '��')
            print('�������ȡ��ϣ�')
            print('='*80)
        print('�����߳���ȡ��ϣ�')

        break
if __name__ == "__main__":
    main()
