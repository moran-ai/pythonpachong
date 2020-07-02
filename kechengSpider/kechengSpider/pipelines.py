# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import os

class KechengspiderPipeline(object):
    def __init__(self):
        self.file = open('kecheng.csv', 'w', encoding='utf-8')
        self.file.write('课程图片地址,课程名称,课程介绍,课程观看人数\n')

    def open_spider(self, spider):
        print("*************** 爬虫开始了！***************")

    def process_item(self, item, spider):
        item = dict(item)
        self.file.write('{}, {}, {}, {}\n'
                        .format(item['url'], item['title'], item['free'],item['num_vis']))
        # self.file.write(str(item))
        return item

    def close_spider(self, spider):
        print('*************** 爬虫结束了！****************')
        self.file.close()

class bendikechengPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        # 获得路径下的文件名
        file_name = 'images/' + os.path.basename(url)
        print(file_name)
        return file_name

    def item_completed(self, results, item, info):
        """
        判断图片是否下载成功
        :param results:
        :param item:
        :param info:
        :return:
        """
        # x为字典数据, ok表示下载成功
        image_paths = [x['path'] for ok, x in results if ok]
        print(str(image_paths))
        if not image_paths:
            raise Exception('下载失败！')
        else:
            return item

    def get_media_requests(self, item, info):
        """
        对每个图片的url发送请求
        :param item:
        :param info:
        :return:
        """
        yield Request(url=item['url'], dont_filter=False)

