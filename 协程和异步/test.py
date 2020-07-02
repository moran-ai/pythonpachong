# encoding:gbk
import requests
import threading
import time
import psutil
import os
import asyncio
import aiohttp
from fake_useragent import UserAgent
from lxml import etree


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

headers = {
    'User-Agent': str(UserAgent().random)
}

async def downMP4(video_url, video_name):
    thread = threading.currentThread()
    process = psutil.Process(os.getpid())
    print('��ǰ�߳�Ϊ��%s, ��ǰ�߳�idΪ��%s, ��ǰ����Ϊ��%s, ��ǰ����idΪ��%s'
          %(thread.getName(), thread.ident, process.name(), process.pid))

    # �������ؿ�ʼʱ��
    start_time = time.time()
    # ������Ƶ
    video_name = stripText(video_name).replace('<strong>', '').replace('</strong>', '').replace(',', '')
    video_url = 'http:' + video_url
    async with aiohttp.ClientSession() as session:
        async with await session.get(url=video_url, headers=headers) as video_response:
            video_rep = await video_response.read()
            print(video_response.status)
            with open(video_name + '.mp4', 'wb') as f:
                f.write(video_rep)

    # �趨���ؽ���ʱ��
    finsh_time = time.time() - start_time
    print(video_name + '.mp4�����غ�ʱ��{}'.format(finsh_time) + '�룡')

def main():
    url = 'https://ibaotu.com/tupian/gongjiangjingshen/7-0-0-0-0-0-0.html?format_type=0'
    response = requests.get(url, headers)
    response.encoding = response.apparent_encoding
    rep = response.text
    with open('����.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    # ����xpath��������
    tree = etree.HTML(rep)

    # ����ÿ����Ƶ��url
    video_xpath_page = '//div[2]/ul/li/div/div/a/div[1]/video/@src'
    item_list_video = tree.xpath(video_xpath_page)

    # ����ÿ����Ƶ������
    video_xpath_name = '//div[2]/ul/li/div/div/a/div[2]/img/@alt'
    item_list_name = tree.xpath(video_xpath_name)

    start_time = time.time()

    # �����¼�ѭ��
    loop = asyncio.get_event_loop()

    downMP4Task = []
    for i in range(len(item_list_video[:8])):
        # ����Э�̶���
        downMP4Proxy = downMP4(item_list_video[i], item_list_name[i])

        # ��װЭ�̶���
        future = asyncio.ensure_future(downMP4Proxy)
        downMP4Task.append(future)

    # ����ע��,��������
    loop.run_until_complete(asyncio.wait(downMP4Task))
    loop.close()

    finsh_time = time.time() - start_time
    print("�ܹ���ʱ��" + str(finsh_time) + '�룡')

if __name__ =="__main__":
    main()