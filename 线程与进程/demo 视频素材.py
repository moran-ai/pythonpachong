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

    # ��ϸҳurl
    video_page_url = item
    video_page_response = requests.get(url=video_page_url, headers=headers)
    video_page_response.encoding = video_page_response.apparent_encoding
    video_page_rep = video_page_response.text
    print(video_page_response.status_code)
    tree_video = etree.HTML(video_page_rep)
    video_xapth_src = "//div/video/@src"

    # ��Ƶ��url
    video_url = stripText(tree_video.xpath(video_xapth_src))
    print(video_url)

    # ��Ƶ����
    video_name_xpath = '//div/div/div/h1/text()'
    video_name = stripText(tree_video.xpath(video_name_xpath))
    # print(video_name)

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
    with open(video_name + '.MP4', 'wb') as f:
        f.write(MP4_rep)

    # ���ʱ��
    finshtime = time.time() - start_time
    return video_name + '.MP4 ��ʱΪ��' + str(finshtime) + '��'

def main():
    url = 'http://www.aoao365.com/ys/hshy'
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    # print(response.status_code)
    rep = response.text
    with open('΢��Ƶ.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    # ����xpath��������
    tree = etree.HTML(rep)
    video_page_xpath = "//div[@class='layui-col-xs6 layui-col-sm6 layui-col-md3']/div[@class='video_con']/a/@href"
    # ���е���Ƶ��Ϣ
    item_list = tree.xpath(video_page_xpath)[:6]
    # print(item_list)
    start_time = time.time()

    # �����߳�
    print('���ǵ�����')
    print('*'*100)
    for item in item_list:
        result = downMP4(item)
        print(result)
    finshTime = time.time() - start_time
    print('������ʱ��Ϊ��' + str(finshTime) + '��')

    # ���߳�
    # print('���Ƕ��߳�')
    # print('-'*100)
    # with ThreadPoolExecutor(max_workers=4) as excutor:
    #     # �ύ�߳�
    #     futures = excutor.map(downMP4, item_list)
    # for future in futures:
    #     print(future)
    # finshTime = time.time() - start_time
    # print('������ʱ��Ϊ��' + str(finshTime) + '��')

    # �����
    # print('���Ƕ����')
    # print('='*100)
    # with ProcessPoolExecutor(max_workers=4) as excutor:
    #     # �ύ����
    #     futures = excutor.map(downMP4, item_list)
    # for future in futures:
    #     print(future)
    # # �ܵ����ʱ��
    # finshTime = time.time() - start_time
    # print('������ʱ��Ϊ��' + str(finshTime) + '��')

if __name__ =="__main__":
    main()
