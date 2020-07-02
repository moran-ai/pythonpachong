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

async def downMP4(video_url ,video_name):
    """
    创建协程对象
    :param video_url:
    :param video_name:
    :return:
    """
    thread = threading.currentThread()
    process = psutil.Process(os.getpid())
    print('当前线程为：%s, 当前的线程id为：%s, 当前的的进程为：%s, 当前的进程id为：%s'
          %(thread.getName(), thread.ident, process.name(), process.pid))

    # 设定下载开始时间
    start_time = time.time()

    # 异步下载视频
    video_name = stripText(video_name).replace(' ', '').replace(',', '').replace('【', '').replace('】', '')
    video_url = video_url

    async with aiohttp.ClientSession() as session:
        async with await session.get(url=video_url, headers=headers) as video_resposne:
            # 读取二进制文件
            video_rep = await video_resposne.read()
            # 打印状态码
            print(video_resposne.status)
            with open(video_name + '.mp4', 'wb') as f:
                f.write(video_rep)

    finsh_time = time.time() - start_time
    # 下载结束时间
    print(video_name + '.mp4，下载耗时：{}'.format(finsh_time) + '秒！')

def main():
    url = 'https://www.shicool.com/video.html'
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    print(response.status_code)
    rep = response.text
    with open('视库.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    tree = etree.HTML(rep)
    # 每个视频网址
    xpath_video = '//div[2]/div[1]/div/a/div[1]/img/@data-url'
    item_list_video = tree.xpath(xpath_video)

    # 每个视频名称
    xpath_video_name = '//div[2]/div[1]/div/a/div[2]/text()'
    item_list_name = tree.xpath(xpath_video_name)

    # 设定异步爬取开始时间
    start_time = time.time()

    # 创建时间循环
    loop = asyncio.get_event_loop()
    downMP4Task = []
    for i in range(len(item_list_video[:6])):
        # 创建协程对象
        downMP4Proxy = downMP4(item_list_video[i], item_list_name[i])
        
        # 封装协程对象
        future = asyncio.ensure_future(downMP4Proxy)
        print(future)
        downMP4Task.append(future)

    # 进行注册,并且运行
    loop.run_until_complete(asyncio.wait(downMP4Task))
    loop.close()

    # 异步爬取结束时间
    finsh_time = time.time() - start_time
    print("总共耗时：" + str(finsh_time) + '秒！')

if __name__ == "__main__":
    main()
