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

headers = {
    'User-Agent': str(UserAgent().random)
}

async def downMP4(video_url, video_name):
    thread = threading.currentThread()
    process = psutil.Process(os.getpid())
    print('当前线程为：%s, 当前线程id为：%s, 当前进程为：%s, 当前进程id为：%s'
          %(thread.getName(), thread.ident, process.name(), process.pid))

    # 设置下载开始时间
    start_time = time.time()
    # 下载视频
    video_name = stripText(video_name).replace('<strong>', '').replace('</strong>', '').replace(',', '')
    video_url = 'http:' + video_url
    async with aiohttp.ClientSession() as session:
        async with await session.get(url=video_url, headers=headers) as video_response:
            video_rep = await video_response.read()
            print(video_response.status)
            with open(video_name + '.mp4', 'wb') as f:
                f.write(video_rep)

    # 设定下载结束时间
    finsh_time = time.time() - start_time
    print(video_name + '.mp4，下载耗时：{}'.format(finsh_time) + '秒！')

def main():
    url = 'https://ibaotu.com/tupian/gongjiangjingshen/7-0-0-0-0-0-0.html?format_type=0'
    response = requests.get(url, headers)
    response.encoding = response.apparent_encoding
    rep = response.text
    with open('工匠.html', 'w', encoding='utf-8') as f:
        f.write(rep)

    # 构建xpath解析对象
    tree = etree.HTML(rep)

    # 解析每个视频的url
    video_xpath_page = '//div[2]/ul/li/div/div/a/div[1]/video/@src'
    item_list_video = tree.xpath(video_xpath_page)

    # 解析每个视频的名称
    video_xpath_name = '//div[2]/ul/li/div/div/a/div[2]/img/@alt'
    item_list_name = tree.xpath(video_xpath_name)

    start_time = time.time()

    # 创建事件循环
    loop = asyncio.get_event_loop()

    downMP4Task = []
    for i in range(len(item_list_video[:8])):
        # 创建协程对象
        downMP4Proxy = downMP4(item_list_video[i], item_list_name[i])

        # 封装协程对象
        future = asyncio.ensure_future(downMP4Proxy)
        downMP4Task.append(future)

    # 进行注册,并且运行
    loop.run_until_complete(asyncio.wait(downMP4Task))
    loop.close()

    finsh_time = time.time() - start_time
    print("总共耗时：" + str(finsh_time) + '秒！')

if __name__ =="__main__":
    main()