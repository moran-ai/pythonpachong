# encoding:gbk
import requests
import threading
import os
import psutil
import time
import asyncio
import aiohttp
from fake_useragent import UserAgent
from lxml import etree

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

async def downMP4(video_url ,video_name):
    """
    ����Э�̶���
    :param video_url:
    :param video_name:
    :return:
    """
    thread = threading.currentThread()
    process = psutil.Process(os.getpid())
    print('��ǰ�߳�Ϊ��%s, ��ǰ���߳�idΪ��%s, ��ǰ�ĵĽ���Ϊ��%s, ��ǰ�Ľ���idΪ��%s'
          %(thread.getName(), thread.ident, process.name(), process.pid))

    # �趨���ؿ�ʼʱ��
    start_time = time.time()

    # �첽������Ƶ
    video_name = stripText(video_name).replace(' ', '').replace(',', '').replace('��', '').replace('��', '')
    video_url = video_url

    async with aiohttp.ClientSession() as session:
        async with await session.get(url=video_url, headers=headers) as video_resposne:
            # ��ȡ�������ļ�
            video_rep = await video_resposne.read()
            # ��ӡ״̬��
            print(video_resposne.status)
            with open(video_name + '.mp4', 'wb') as f:
                f.write(video_rep)

    finsh_time = time.time() - start_time
    # ���ؽ���ʱ��
    print(video_name + '.mp4�����غ�ʱ��{}'.format(finsh_time) + '�룡')

def main():
    url = 'https://www.shicool.com/video.html'
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    print(response.status_code)
    rep = response.text
    with open('�ӿ�.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    tree = etree.HTML(rep)
    # ÿ����Ƶ��ַ
    xpath_video = '//div[2]/div[1]/div/a/div[1]/img/@data-url'
    item_list_video = tree.xpath(xpath_video)

    # ÿ����Ƶ����
    xpath_video_name = '//div[2]/div[1]/div/a/div[2]/text()'
    item_list_name = tree.xpath(xpath_video_name)

    # �趨�첽��ȡ��ʼʱ��
    start_time = time.time()

    # ����ʱ��ѭ��
    loop = asyncio.get_event_loop()
    downMP4Task = []
    for i in range(len(item_list_video[:6])):
        # ����Э�̶���
        downMP4Proxy = downMP4(item_list_video[i], item_list_name[i])
        
        # ��װЭ�̶���
        future = asyncio.ensure_future(downMP4Proxy)
        print(future)
        downMP4Task.append(future)

    # ����ע��,��������
    loop.run_until_complete(asyncio.wait(downMP4Task))
    loop.close()

    # �첽��ȡ����ʱ��
    finsh_time = time.time() - start_time
    print("�ܹ���ʱ��" + str(finsh_time) + '�룡')

if __name__ == "__main__":
    main()
