# encoding:gbk
import requests
import threading
from fake_useragent import UserAgent
from lxml import etree
import time
import psutil
import os
import asyncio
import aiohttp

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

# ʹ��Э��async�Է������д���
async def downMP4(video_url, video_name):
    thread = threading.currentThread()
    process = psutil.Process(os.getpid())
    print('��ǰ�߳�Ϊ:%s,��ǰ�߳�IDΪ%s, ��ǰ����Ϊ:%s,��ǰ����idΪ��%s'
          % (thread.getName(), thread.ident, process.name(), process.pid))

    # time.sleep(1)
    # �첽����
    # await asyncio.sleep(1)

    start_time = time.time()
    # ������Ƶ
    video_name = stripText(video_name).replace('<strong>', '').replace('</strong>', '').replace(',', '')
    video_url = 'http:' + video_url

    # �첽
    async with aiohttp.ClientSession() as session:
        async with await session.get(url=video_url, headers=headers) as video_response:
            video_rep = await video_response.read()
            print(video_response.status)
            with open(video_name + '.mp4', 'wb') as f:
                f.write(video_rep)

    finsh_time = time.time() - start_time
    print(video_name + '.mp4,���غ�ʱ:{}'.format(finsh_time) + '�룡')


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
    # print(item_list_video, item_list_name)

    start_time = time.time()

    # # �����߳�
    # with ThreadPoolExecutor(4) as executor:
    #     for i in range(len(item_list_video)):
    #         executor.submit(downMP4, item_list_video[i], item_list_name[i])



    # Э��
    # Э��ѭ����
    loop = asyncio.get_event_loop()
    downMP4Task = []
    for i in range(len(item_list_video)):
        # ����Э�̶���
        downMP4Proxy = downMP4(item_list_video[i], item_list_name[i])

        # ��װЭ�̶���
        future = asyncio.ensure_future(downMP4Proxy)
        print(future)
        downMP4Task.append(future)

    # ����ע��,��������
    loop.run_until_complete(asyncio.wait(downMP4Task))
    loop.close()

    finsh_time = time.time() - start_time
    print("�ܹ���ʱ��" + str(finsh_time) + '�룡')
if __name__ =="__main__":
    main()