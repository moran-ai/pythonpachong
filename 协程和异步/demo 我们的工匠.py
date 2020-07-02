# encoding:gbk
import requests
import threading
from fake_useragent import UserAgent
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import time
import psutil
import os

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

def downMP4(video_url, video_name):
    thread = threading.currentThread()
    process = psutil.Process(os.getpid())
    print('��ǰ�߳�Ϊ:%s,��ǰ�߳�IDΪ%s, ��ǰ����Ϊ:%s,��ǰ����idΪ��%s'
          % (thread.getName(), thread.ident, process.name(), process.pid))


    start_time = time.time()
    # ������Ƶ
    video_url = 'http:' + video_url
    video_response = requests.get(url=video_url, headers=headers)
    video_name = stripText(video_name).replace('<strong>', '').replace('</strong>', '').replace(',', '')
    video_rep = video_response.content
    with open(video_name+'.mp4', 'wb') as f:
        f.write(video_rep)
    finsh_time = time.time() - start_time
    print(video_name + '.mp4,���غ�ʱ:{}'.format(finsh_time) + '�룡')


"""
�ص�����
def call_back(res):
    result = res.result()
    print(result)"""


def main():
    url = 'https://ibaotu.com/tupian/gongjiangjingshen/7-0-0-0-0-0-0.html?format_type=0'
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    print(response.status_code)
    rep = response.text
    with open('����.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    # ����xpath����
    tree = etree.HTML(rep)
    xpath_video_page = '//div[2]/ul/li/div/div/a/div[1]/video/@src'
    item_list_video = tree.xpath(xpath_video_page)

    xpath_video_name = '//div[2]/ul/li/div/div/a/div[2]/img/@alt'
    item_list_name = tree.xpath(xpath_video_name)

    start_time = time.time()

    # # �����߳�
    # with ThreadPoolExecutor(4) as executor:
    #     for i in range(len(item_list_video)):
    #         executor.submit(downMP4, item_list_video[i], item_list_name[i])

    finsh_time = time.time() - start_time
    print("�ܹ���ʱ��" + str(finsh_time) + '�룡')
if __name__ =="__main__":
    main()