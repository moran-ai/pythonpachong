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
    �����������ͷ
    :return:
    """
    headers = {
        'User-Agent': str(UserAgent().random)
    }
    return headers

def tishi():
    choices = input('�밴�����˳�����: 1.���߳�  2.���߳�  3.�����:')
    return choices

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
    """
    ������Ƶ������
    :param item: ��ȡ��ҳ��url
    :return:
    """
    # �������ؿ�ʼʱ��
    start_time = time.time()

    # ������ϸҳurl
    video_page_url = item

    # ��ϸҳ��������
    video_page_response = requests.get(url=video_page_url, headers=head())
    video_page_response.encoding = video_page_response.apparent_encoding
    video_page_rep = video_page_response.text

    # ������ϸҳ��������
    tree_video = etree.HTML(video_page_rep)
    video_xapth_src = "//div/video/@src"

    # ������Ƶ����
    video_url = stripText(tree_video.xpath(video_xapth_src))
    print(video_url)

    # ������Ƶ����
    video_name_xpath = '//div/div/div/h1/text()'
    video_name = stripText(tree_video.xpath(video_name_xpath))

    # ��õ�ǰ�߳�
    thred = threading.current_thread()

    # ��õ�ǰ����
    process = psutil.Process(os.getpid())

    # ��ӡ�������̵߳����ƺ�id
    print('��ǰ�߳�����Ϊ:%s, IDΪ:%s, ��������Ϊ:%s, IDΪ%s'
          % (thred.getName(), thred.ident, process.name(), process.pid))

    # �������󣬻����Ƶ�ļ�
    video_response = requests.get(url=video_url, headers=head())
    MP4_rep = video_response.content

    # �洢��Ƶ�ļ�
    with open(video_name + '.MP4', 'wb') as f:
        f.write(MP4_rep)

    # �����������ʱ��
    finshtime = time.time() - start_time
    return video_name + '.MP4 ��ʱΪ��' + str(finshtime) + '��'

def main():
    """
    ��ȡ��ҳ����Ϣ�������߳���ȡ
    :return:
    """
    # ��ҳ��url
    url = 'http://www.aoao365.com/ys/hshy'
    # ��ҳ�淢������
    response = requests.get(url, headers=head())
    response.encoding = response.apparent_encoding
    rep = response.text
    with open('΢��Ƶ.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    # ������ҳ���������
    tree = etree.HTML(rep)

    # ��ҳ��������Ƶ��Ϣxpath
    video_page_xpath = "//div[@class='layui-col-xs6 layui-col-sm6 layui-col-md3']/div[@class='video_con']/a/@href"

    # ���ǰ6����Ƶ��xpath��Ϣ
    item_list = tree.xpath(video_page_xpath)[:6]
    # �����߳̿�ʼʱ��
    start_time = time.time()

    while True:
        choices = tishi()
        if choices == '1':
            print('����ʹ�õ��߳�')
            print('*'*80)
            for item in item_list:
                result = downMP4(item)
                print(result)
            finshTime = time.time() - start_time
            print('������ʱ��Ϊ��' + str(finshTime) + '��')
            print('���߳���ȡ��ɣ�')
            print('*'*80)
            choices = tishi()

        if choices == '2':
            print('����ʹ�ö��߳�')
            print('-'*80)
            with ThreadPoolExecutor(max_workers=4) as excutor:
                # �ύ�߳�
                futures = excutor.map(downMP4, item_list)
            for future in futures:
                print(future)
            finshTime = time.time() - start_time
            print('������ʱ��Ϊ��' + str(finshTime) + '��')
            print('���߳���ȡ��ɣ�')
            print('-'*80)
            choices = tishi()

        if choices == '3':
            print('����ʹ�ö����')
            print('='*80)
            with ProcessPoolExecutor(max_workers=4) as excutor:
                # �ύ����
                futures = excutor.map(downMP4, item_list)
            for future in futures:
                print(future)

            # �����߳����ʱ��
            finshTime = time.time() - start_time
            print('������ʱ��Ϊ��' + str(finshTime) + '��')
            print('�������ȡ��ɣ�')
            print('='*80)
        print('�����߳���ȡ��ϣ�')

        break
if __name__ =="__main__":
    main()