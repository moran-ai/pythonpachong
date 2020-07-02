# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import pymongo

class mongospiderPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        获取setting设置的数据库参数
        :param crawler:
        :return:
        """
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        """
        连接数据库，创建数据库
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """
        创建集合，并插入数据
        :param item:
        :param spider:
        :return:
        """
        self.db[spider.name].insert(dict(item))
        print('数据库中集合的名字' + spider.name)
        return item

    def close_spider(self, spider):
        """
        关闭数据库
        :param spider:
        :return:
        """
        self.client.close()

class DianshijuspiderPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        # 获得路径下的文件名
        file_name = url.split('/')[-1]
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
            raise DropItem('下载失败！')
        return item

    def get_media_requests(self, item, info):
        """
        对每个图片的url发送请求
        :param item:
        :param info:
        :return:
        """
        yield Request(url=item['url'], dont_filter=False)